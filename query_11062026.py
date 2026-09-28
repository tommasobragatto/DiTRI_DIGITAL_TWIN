"""
Esempio di script per interrogare il database digital_twin
e leggere i risultati salvati dalla simulazione del Digital Twin.
"""

import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta, timezone

DB_DSN = "host=localhost dbname=digital_twin user=postgres password=superuser"

MAIN_SIM_ID = "main"


def get_connection():
    return psycopg2.connect(DB_DSN)


def get_last_instance(conn, simulation_id: str = MAIN_SIM_ID):
    """Restituisce l'ultima istanza (snapshot) salvata per la simulazione."""
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT id, ts, type
            FROM digital_twin_instance
            WHERE simulation_id = %s
            ORDER BY ts DESC
            LIMIT 1
            """,
            (simulation_id,),
        )
        return cur.fetchone()


def get_metrics_for_instance(conn, instance_id: str, value_type: str = None):
    """
    Restituisce tutte le metriche di una certa istanza.
    Se value_type è specificato (es. 'vm_pu'), filtra solo quel tipo.
    """
    query = """
        SELECT value_type, value, ts, ref_id, ref_type, is_simulated
        FROM digital_twin_metrics
        WHERE dtw_instance_id = %s
    """
    params = [instance_id]

    if value_type:
        query += " AND value_type = %s"
        params.append(value_type)

    query += " ORDER BY ref_type, ref_id"

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(query, params)
        return cur.fetchall()


def get_voltage_history(conn, bus_ref_id: str, hours: int = 1):
    """
    Esempio: andamento storico della tensione (vm_pu) di un bus
    nelle ultime N ore.
    """
    since = datetime.now(timezone.utc) - timedelta(hours=hours)

    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT ts, value
            FROM digital_twin_metrics
            WHERE ref_id = %s
              AND ref_type = 'bus'
              AND value_type = 'vm_pu'
              AND ts >= %s
            ORDER BY ts ASC
            """,
            (bus_ref_id, since),
        )
        return cur.fetchall()


def get_ga_kpi_trend(conn, simulation_id: str = MAIN_SIM_ID, limit: int = 20):
    """
    Esempio: ultimi N valori di fitness/tempo di esecuzione del GA,
    uniti tramite l'istanza a cui appartengono.
    """
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """
            SELECT i.ts, m.value_type, m.value
            FROM digital_twin_metrics m
            JOIN digital_twin_instance i ON i.id = m.dtw_instance_id
            WHERE i.simulation_id = %s
              AND m.value_type IN ('ga_best_fitness', 'ga_execution_time_s')
            ORDER BY i.ts DESC
            LIMIT %s
            """,
            (simulation_id, limit * 2),  # *2 perché ci sono 2 metriche per istanza
        )
        return cur.fetchall()


def main():
    conn = get_connection()

    # 1. Ultima istanza salvata
    last_instance = get_last_instance(conn)
    if not last_instance:
        print("Nessuna istanza trovata.")
        return

    print(f"Ultima istanza: {last_instance['id']} (ts={last_instance['ts']})")

    # 2. Tutte le tensioni dei bus per quell'istanza
    voltages = get_metrics_for_instance(conn, last_instance["id"], value_type="vm_pu")
    print("\nTensioni bus (vm_pu):")
    for row in voltages:
        print(f"  {row['ref_id']:>10} -> {row['value']:.4f}  (ts={row['ts']})")

    # 3. Storico tensione di un bus specifico (es. bus-1) nell'ultima ora
    history = get_voltage_history(conn, "bus-1", hours=1)
    print(f"\nStorico vm_pu per bus-1 (ultime {len(history)} misure):")
    for row in history:
        print(f"  {row['ts']} -> {row['value']:.4f}")

    # 4. Trend KPI del GA
    kpis = get_ga_kpi_trend(conn, limit=10)
    print("\nUltimi KPI GA:")
    for row in kpis:
        print(f"  {row['ts']} | {row['value_type']:<22} = {row['value']}")

    conn.close()


if __name__ == "__main__":
    main()