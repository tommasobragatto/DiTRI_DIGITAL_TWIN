"""
Digital Twin Simulation — refactored
=====================================
Changes from original:
  - Removed all .txt / .csv file I/O
  - All results (GA metrics, state estimation, power values, voltages)
    are persisted into the `digital_twin` PostgreSQL database
    (digital_twin_simulations / digital_twin_instance / digital_twin_metrics)
  - One simulation run = one digital_twin_instance row tied to `main`
  - Helper functions isolate DB operations from simulation logic
"""

import pandapower as pp
import time
import json
import uuid
import logging

import pygad
import numpy
import psycopg2
import psycopg2.extras
import paho.mqtt.client as mqtt
from datetime import datetime, timezone

import network_function

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
DB_DSN = "host=localhost dbname=digital_twin user=postgres password=superuser"

BROKER   = "185.131.248.7"
PORT     = 1883
MQTT_USER     = "wisegrid"
MQTT_PASSWORD = "wisegrid"

MAIN_SIM_ID = "main"

ATTIVO_FLESSIBILITA = False   # set True to enable flexibility study
MAX_TIME = 5                  # loop duration cap (seconds, kept for reference)

# Genetic Algorithm hyper-parameters
NUM_GENERATIONS      = 50
NUM_PARENTS_MATING   = 4
SOL_PER_POP          = 10
NUM_GENES            = 12
MUTATION_PERCENT     = 50
STOP_CRITERIA        = "reach_4"   # tolerance ~0.25 V

# Buses we care about
CARICO = [
    "Headquarters", "Slow", "Mazzocchio", "Celi",
    "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV",
]
PROSSIMI_KWH_STORED = [15, 5, 2.5, 8, 33, 35, 35]

# SE (state-estimation) load / node ids
CARICHI_SE  = ["1", "2", "3", "4"]
NODI_NOTI   = ["1", "6"]

# ---------------------------------------------------------------------------
# Database helpers
# ---------------------------------------------------------------------------

def get_db_connection() -> psycopg2.extensions.connection:
    return psycopg2.connect(DB_DSN)


def ensure_main_simulation(conn) -> None:
    """
    Create the 'main' simulation row if it doesn't already exist.
    In production the backend owns this row; this guard is for local dev.
    """
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id FROM digital_twin_simulations WHERE id = %s",
            (MAIN_SIM_ID,),
        )
        if cur.fetchone() is None:
            cur.execute(
                """
                INSERT INTO digital_twin_simulations (id, graph, status)
                VALUES (%s, %s, %s)
                """,
                (MAIN_SIM_ID, json.dumps({}), "running"),
            )
    conn.commit()


def create_instance(conn, ts: datetime) -> str:
    """
    Insert a new digital_twin_instance snapshot for `main` and return its id.
    """
    instance_id = str(uuid.uuid4())
    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO digital_twin_instance (id, ts, simulation_id, type)
            VALUES (%s, %s, %s, %s)
            """,
            (instance_id, ts, MAIN_SIM_ID, "state_estimation"),
        )
    conn.commit()
    return instance_id


def bulk_insert_metrics(conn, instance_id: str, rows: list[dict]) -> None:
    """
    Insert multiple metric rows into digital_twin_metrics in one shot.

    Each dict in `rows` must have:
        value_type, value, ts, ref_id, ref_type, is_simulated
    """
    if not rows:
        return
    with conn.cursor() as cur:
        psycopg2.extras.execute_batch(
            cur,
            """
            INSERT INTO digital_twin_metrics
                (value_type, value, ts, ref_id, ref_type, is_simulated, dtw_instance_id)
            VALUES
                (%(value_type)s, %(value)s, %(ts)s,
                 %(ref_id)s, %(ref_type)s, %(is_simulated)s, %(dtw_instance_id)s)
            """,
            [{**r, "dtw_instance_id": instance_id} for r in rows],
        )
    conn.commit()


# ---------------------------------------------------------------------------
# Metric builders
# ---------------------------------------------------------------------------

def _metric(value_type: str, value: float, ref_id: str, ref_type: str,
            ts: datetime, is_simulated: bool = True) -> dict:
    return {
        "value_type":   value_type,
        "value":        float(value),
        "ts":           ts,
        "ref_id":       ref_id,
        "ref_type":     ref_type,
        "is_simulated": is_simulated,
    }


def collect_network_metrics(net, ts: datetime) -> list[dict]:
    """
    Harvest bus voltages, load powers, and line loadings from a solved network.
    """
    metrics: list[dict] = []

    # Bus voltages
    for bus_idx, row in net.res_bus.iterrows():
        bus_id = f"bus-{bus_idx}"
        metrics.append(_metric("vm_pu",  row["vm_pu"],  bus_id, "bus", ts))
        metrics.append(_metric("va_degree", row["va_degree"], bus_id, "bus", ts))

    # Load powers
    for load_idx, row in net.res_load.iterrows():
        load_id = f"load-{load_idx}"
        metrics.append(_metric("p_mw",   row["p_mw"],   load_id, "load", ts))
        metrics.append(_metric("q_mvar", row["q_mvar"], load_id, "load", ts))

    # Line loadings
    for line_idx, row in net.res_line.iterrows():
        line_id = f"line-{line_idx}"
        metrics.append(_metric("loading_percent", row["loading_percent"], line_id, "line", ts))
        metrics.append(_metric("p_from_mw",       row["p_from_mw"],       line_id, "line", ts))

    return metrics


def collect_ga_kpi_metrics(execution_time: float, fitness: float,
                            ts: datetime) -> list[dict]:
    """
    KPI rows that replace the old KPI_GA_Execution_Time.csv.txt
    and GA_Fitness.csv.txt files.
    """
    return [
        _metric("ga_execution_time_s", execution_time, "ga-optimizer", "kpi", ts),
        _metric("ga_best_fitness",     fitness,         "ga-optimizer", "kpi", ts),
        _metric("ga_voltage_error",    1.0 / fitness,   "ga-optimizer", "kpi", ts),
    ]


def collect_se_power_metrics(net, solution: numpy.ndarray,
                              ts: datetime) -> list[dict]:
    """
    Estimated P/Q for each SE load — replaces potenza_SE.txt.
    """
    metrics: list[dict] = []
    for i, load_id in enumerate(CARICHI_SE[:-1]):   # same slice as original
        p = float(solution[2 * i]) / 1000
        q = float(solution[2 * i + 1]) / 1000
        metrics.append(_metric("p_mw",   p, f"load-{load_id}", "load", ts))
        metrics.append(_metric("q_mvar", q, f"load-{load_id}", "load", ts))
    return metrics


def collect_voltage_error_metrics(misure: list[float],
                                   tensioni_calc: list[float],
                                   ts: datetime) -> list[dict]:
    """
    Measured-vs-estimated voltage deltas — replaces MQTT Voltage_Error publish
    and the old stdout prints.
    """
    metrics: list[dict] = []
    for i, node_id in enumerate(NODI_NOTI[:-1]):
        bus_id = f"bus-{node_id}"
        error  = float(misure[i]) - tensioni_calc[i]
        metrics.append(_metric("vm_pu",       tensioni_calc[i], bus_id, "bus", ts))
        metrics.append(_metric("vm_pu_error", error,            bus_id, "bus", ts))
    return metrics


# ---------------------------------------------------------------------------
# State estimation (GA)
# ---------------------------------------------------------------------------

def build_gene_space() -> list:
    """
    Gene search space — unchanged from the original.
    Average load values used as centre-points for each gene range.
    """
    vP9, vP10, vP11 = 21.41749, 3.92556, 12.76311
    vQ9, vQ10, vQ11 =  6.44643, 0.79711,  0.59104

    return [
        numpy.linspace(vP10 - 5,  vP10 + 5,  20),
        numpy.linspace(vQ10 - 2.5, vQ10 + 2.5, 10),
        numpy.linspace(vP11 - 10, vP11 + 10, 20),
        numpy.linspace(vQ11 - 5,  vQ11 + 5,  10),
        numpy.linspace(vP9  - 16, vP9  + 16, 20),
        numpy.linspace(vQ9  - 8,  vQ9  + 8,  10),
        numpy.linspace(vP11 - 10, vP11 + 10, 20),
        numpy.linspace(vQ11 - 5,  vQ11 + 5,  10),
        numpy.linspace(0.9,  1.1, 10),
    ]


def make_fitness_func(net, misure: list[float]):
    """
    Closure that captures the pandapower network and voltage measurements.
    """
    def fitness_func(ga_instance, solution, solution_idx):
        for i in range(len(CARICHI_SE) - 1):
            net.load.p_mw.at[float(CARICHI_SE[i])]   = float(solution[2 * i])     / 1000
            net.load.q_mvar.at[float(CARICHI_SE[i])] = float(solution[2 * i + 1]) / 1000
        net.ext_grid.vm_pu[0] = float(solution[2 * len(CARICHI_SE)])
        pp.runpp(net, numba=False)

        tensioni_calc, delta = [], []
        for i in range(len(NODI_NOTI) - 1):
            tensione = net.res_bus.vm_pu.at[float(NODI_NOTI[i])]
            tensioni_calc.append(tensione)
            delta.append(float(misure[i]) * 50 - tensioni_calc[i])

        return len(NODI_NOTI) / numpy.dot(delta, delta)

    return fitness_func


def run_state_estimation(net, misure: list[float],
                          initial_population: list) -> tuple:
    """
    Run the GA-based state estimator.
    Returns (solution, solution_fitness, ga_exec_seconds, updated_initial_pop).
    """
    ga = pygad.GA(
        num_generations        = NUM_GENERATIONS,
        num_parents_mating     = NUM_PARENTS_MATING,
        fitness_func           = make_fitness_func(net, misure),
        sol_per_pop            = SOL_PER_POP,
        stop_criteria          = STOP_CRITERIA,
        num_genes              = NUM_GENES,
        gene_space             = build_gene_space(),
        parent_selection_type  = "sss",
        keep_parents           = 1,
        crossover_type         = "single_point",
        mutation_type          = "random",
        mutation_percent_genes = MUTATION_PERCENT,
        initial_population     = initial_population,
    )

    t0 = time.time()
    ga.run()
    exec_time = time.time() - t0

    solution, fitness, _ = ga.best_solution()
    warm_start = [solution] * 5   # warm-start for next iteration

    return solution, fitness, exec_time, warm_start


# ---------------------------------------------------------------------------
# MQTT setup
# ---------------------------------------------------------------------------

def build_mqtt_client() -> mqtt.Client:
    client = mqtt.Client()
    client.username_pw_set(MQTT_USER, password=MQTT_PASSWORD)
    # client.connect(BROKER, PORT, 60)   # uncomment when broker is reachable
    return client


def publish_se_results(client: mqtt.Client, solution: numpy.ndarray,
                        net, misure: list[float], ts_iso: str) -> None:
    """
    Publish estimated P/Q and voltage errors over MQTT (unchanged logic).
    """
    payload_base = {"d": None, "dt": 4, "ts": ts_iso, "q": 192}

    for i, load_id in enumerate(CARICHI_SE[:-1]):
        net.load.p_mw.at[float(load_id)]   = float(solution[2 * i])     / 1000
        net.load.q_mvar.at[float(load_id)] = float(solution[2 * i + 1]) / 1000
        pp.runpp(net, numba=False)

        payload_base["d"]  = solution[2 * i];   payload_base["ts"] = ts_iso
        client.publish(f"A2MQTT/{load_id}/Power_P_1_7_0/Cv",
                       json.dumps(payload_base))

        payload_base["d"]  = solution[2 * i + 1]
        client.publish(f"A2MQTT/{load_id}/Power_Q_3_7_0/Cv",
                       json.dumps(payload_base))

    tensioni_calc = []
    for i, node_id in enumerate(NODI_NOTI[:-1]):
        t = net.res_bus.vm_pu.at[float(node_id)]
        tensioni_calc.append(t)

        payload_base["d"] = float(misure[i]) - t
        client.publish(f"A2MQTT/{node_id}/Voltage_Error_U_32_7_0/Cv",
                       json.dumps(payload_base))

        payload_base["d"] = t
        client.publish(f"A2MQTT/{node_id}/Voltage_Calc_U_32_7_0/Cv",
                       json.dumps(payload_base))


# ---------------------------------------------------------------------------
# JSON meter loaders
# ---------------------------------------------------------------------------

def load_meters() -> dict:
    """
    Read all W*_P/Q/V JSON files.  Returns a dict keyed by signal name.
    """
    signals = {}
    for meter in ["W3", "W4", "W5", "W6"]:
        for kind in ["P", "Q", "V"]:
            key = f"{meter}_{kind}"
            with open(f"{key}.json") as fh:
                signals[key] = json.loads(fh.read())
    return signals


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def main():
    net    = network_function.asm_feeder_network()
    client = build_mqtt_client()

    initial_population = [[1] * 9 for _ in range(5)]

    if ATTIVO_FLESSIBILITA:
        soglia = [-12, 26, 53, 43, 120, 152, 172, 265]
        log.info("Flexibility thresholds: %s", soglia)

    conn = get_db_connection()
    ensure_main_simulation(conn)

    log.info("Starting main loop …")

    while True:
        loop_start = time.time()

        # ── 1. Read meters ──────────────────────────────────────────────
        signals = load_meters()

        ts_now = datetime.now(timezone.utc)

        # ── 2. Push known measurements into the network ─────────────────
        net.load.p_mw.at[0]   = signals["W4_P"]["d"] / 1_000_000
        net.load.q_mvar.at[0] = signals["W4_Q"]["d"] / 1_000_000
        net.load.p_mw.at[5]   = signals["W6_P"]["d"] / 1_000_000
        net.load.q_mvar.at[5] = signals["W6_Q"]["d"] / 1_000_000
        net.ext_grid.vm_pu[0] = 1.1   # TODO: integrate PMU

        misure = [signals["W4_V"]["d"], signals["W6_V"]["d"]]

        # ── 3. State estimation (GA) ─────────────────────────────────────
        solution, fitness, exec_time, initial_population = run_state_estimation(
            net, misure, initial_population
        )

        ts_iso = ts_now.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
        log.info("GA done | fitness=%.4f | time=%.2fs", fitness, exec_time)

        # ── 4. Apply best solution and run final power flow ──────────────
        for i, load_id in enumerate(CARICHI_SE[:-1]):
            net.load.p_mw.at[float(load_id)]   = float(solution[2 * i])     / 1000
            net.load.q_mvar.at[float(load_id)] = float(solution[2 * i + 1]) / 1000
        pp.runpp(net, numba=False)

        # ── 5. Compute voltage errors ────────────────────────────────────
        tensioni_calc = [
            net.res_bus.vm_pu.at[float(n)]
            for n in NODI_NOTI[:-1]
        ]

        # ── 6. Persist everything to DB ──────────────────────────────────
        instance_id = create_instance(conn, ts_now)

        metrics: list[dict] = []
        metrics += collect_ga_kpi_metrics(exec_time, fitness, ts_now)
        metrics += collect_se_power_metrics(net, solution, ts_now)
        metrics += collect_voltage_error_metrics(misure, tensioni_calc, ts_now)
        metrics += collect_network_metrics(net, ts_now)

        bulk_insert_metrics(conn, instance_id, metrics)
        log.info("Persisted %d metric rows (instance %s)", len(metrics), instance_id)

        # ── 7. Publish over MQTT ─────────────────────────────────────────
        publish_se_results(client, solution, net, misure, ts_iso)

        loop_elapsed = time.time() - loop_start
        log.info("Loop iteration completed in %.2fs", loop_elapsed)


if __name__ == "__main__":
    main()
