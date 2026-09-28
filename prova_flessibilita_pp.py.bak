import py_dss_interface
import os
import pathlib
import time
import json
import subprocess
import pygad
import numpy
from ottimo_flessibilita import threshold_flexibility
import paho.mqtt.client as mqtt
from datetime import datetime

broker= "185.131.248.7"  #Broker address
port = 1883                         #Broker port
user = "wisegrid"                    #Connection username
password = "wisegrid"            #Connection password
client = mqtt.Client()
client.username_pw_set(user, password=password)
client.connect(broker, port, 60)
json_object = {"d": 4,
      "dt": 4,
      "ts": 4,
      "q": 192}

attivo_flessibilita=False   # put False if you don't want to do flexibility study
MAX_TIME=5                # Duration enforced manually
script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("Run_DT.dss")

#dss=py_dss_interface.DSSDLL(r"/usr/local/share/opendsscmd")
if attivo_flessibilita==True:
    #soglia=threshold_flexibility()
    soglia=[-12,  26,  53,  43, 120, 152, 172, 265]
    print(soglia)



initial_population=[[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1]]

# CARICO corresponds to the buses that we would like to monitor
carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]
prossimi_kWh_stored=[15, 5, 2.5, 8, 33, 35, 35]

### INFINITE LOOP ###
while True:
    inizio = time.time()
### INDIVIDUAL METERS ARE INVOKED IN ORDER TO COLLECT DATA ###
    subprocess.call(['python', "testMain.py"])

### EACH MEASUREMENT (JSON FILE) IS OPENED AND ASSIGNED TO A VARIABLE #####
    w3p = open('W3_P.json', 'r')
    w3q = open('W3_Q.json', 'r')
    w3v = open('W3_V.json', 'r')
    w4p = open('W4_P.json', 'r')
    w4q = open('W4_Q.json', 'r')
    w4v = open('W4_V.json', 'r')
    w5p = open('W5_P.json', 'r')
    w5q = open('W5_Q.json', 'r')
    w5v = open('W5_V.json', 'r')
    w6p = open('W6_P.json', 'r')
    w6q = open('W6_Q.json', 'r')
    w6v = open('W6_V.json', 'r')
    w3v = open('W3_V.json', 'r')
    w4v = open('W4_V.json', 'r')
    w5v = open('W5_V.json', 'r')
    w6v = open('W6_V.json', 'r')
    W3_V = json.loads(w3v.read())
    W4_V = json.loads(w4v.read())
    W5_V, W6_V = json.loads(w5v.read()), json.loads(w6v.read())
    W3_P, W3_Q = json.loads(w3p.read()), json.loads(w3q.read())
    W4_P, W4_Q = json.loads(w4p.read()), json.loads(w4q.read())
    W5_P, W5_Q = json.loads(w5p.read()), json.loads(w5q.read())
    W6_P, W6_Q = json.loads(w6p.read()), json.loads(w6q.read())

### DATA ARE WRITTEN IN THE INPUT FILE OF THE DT (OPENDSS LF) ####
    dss_new_load_file = pathlib.Path(script_path).joinpath("Loads_DT.dss")
    o = open(dss_new_load_file, "w")
    o.write("New Load.Headquarters   phases=3 conn=wye Bus1=BUS8        kw=" + str(W4_P["d"]) + " kvar=" + str(W4_Q["d"]) + "   kv=0.4"
            + "\nNew Load.Slow           phases=3 conn=wye Bus1=BUS8        kw=22  kvar=1.4  kv=0.4 "
            +  "\nNew Load.Mazzocchio     phases=3 conn=wye Bus1=BUS10       kw=45  kvar=4  kv=0.4 "
            +  "\nNew Load.Celi           phases=3 conn=wye Bus1=BUS11       kw=90  kvar=14  kv=0.4"
            +  "\nNew Load.Storage         phases=3 conn=wye Bus1=BUS14        kw=" + str(W3_P["d"]) + " kvar="+ str(W3_Q["d"]) + "  kv=0.4"
            +  "\nNew Load.Fast             phases=3 conn=wye Bus1=BUS16      kw=" + str(W5_P["d"]) + " kvar="+ str(W5_Q["d"]) + "  kv=0.4"
            +  "\nNew Load.Croci            phases=3 conn=wye Bus1=BUS9        kw=150  kvar=23  kv=0.4"
            +  "\nNew Load.PV185            phases=3 conn=wye Bus1=BUS15       kw=" + str(W6_P["d"]) + " kvar=" + str(W6_Q["d"]) + " kv=0.4"
            +  "\nNew Load.PV60             phases=3 conn=wye Bus1=BUS8        kw=" + str((60/185)*W6_P["d"]) + "  kvar=0  kv=0.4"
            +  "\nNew Load.altroSCOV        phases=3 conn=wye Bus1=BUS15       kw=100  kvar=75  kv=0.4")
    o.close()

#### STATE ESTITMATION ##########
    ## COLLECTION OF THE VOLTAGES FOR THE STATE ESTIMATION
    misure = [W3_V["d"], W4_V["d"], W5_V["d"], W6_V["d"]]


    def fitness_func(solution, solution_idx):
        dss.text(f"compile [{dss_file}]")
        carichiSE = ["Mazzocchio", "Celi", "Croci", "altroSCOV", "Slow"]   # carichi da stimare
        for i in range(5):
            dss.loads_write_name(f"{carichiSE[i]}")
            dss.loads_write_kw(float(solution[2 * i]))
            dss.loads_write_kvar(float(solution[2 * i + 1]))

        # inserisco tra le soluzioni anche la potenza reattiva del carico PV60 (bus 8)
        dss.loads_write_name("PV60")
        dss.loads_write_kvar(float(solution[10]))
        #  include the voltage of the PS in the loop
        dss.vsources_write_name("Source")
        dss.vsources_write_pu(float(solution[11]))

        dss.solution_solve()

        tensioni_calc, delta = [], []
        nodi_noti = ["Storage", "Headquarters", "Fast", "PV185"]
        for i in range(4):
            dss.circuit_set_active_element(f"Load.{nodi_noti[i]}")
            tensione = dss.cktelement_voltages_mag_ang()
            tensioni_calc.append(tensione)
            delta.append(float(misure[i]) - tensioni_calc[i][0])
        fitness = 4.0 / numpy.dot(delta, delta)
        return fitness


    fitness_function = fitness_func

    num_generations = 50
    num_parents_mating = 4
    sol_per_pop = 10
    num_genes = 12

    # Leggo i valori medi delle potenze che passano nei nodi 9, 10 e 11, così da fare una stima più accurata ed inserirli nel gene_space con + o - 20%
    h=time.localtime().tm_hour
    m=time.localtime().tm_min
    valoreP9=21.41749
    valoreP10=3.92556
    valoreP11=12.76311
    valoreQ9=6.44643
    valoreQ10=0.79711
    valoreQ11=0.59104

    dss.text(f"compile [{dss_file}]")
    dss.loads_write_name("PV60")
    Q_max_PV60=0.5*(dss.loads_read_kw())

    gene_space = [numpy.linspace(valoreP10 - 5, valoreP10 + 5, 20), # carico mazzocchio, per la P faccio + e - il 10% della potenza nominale (50 kVA)
                  numpy.linspace(valoreQ10 - 2.5, valoreQ10 + 2.5, 10), # carico mazzocchio, per la Q faccio + e - il 5% della potenza nominale (50 kVA)
                  numpy.linspace(valoreP11 - 10, valoreP11 + 10, 20),  # carico celi, per la P faccio + e - il 10% della potenza nominale(100 kVA)
                  numpy.linspace(valoreQ11 - 5, valoreQ11 + 5, 10), # carico celi, per la Q faccio + e - il 5% della potenza nominale(100 kVA)
                  numpy.linspace(valoreP9 - 16, valoreP9 + 16, 20), # carico croci, per la P faccio + e - il 10% della potenza nominale(160 kVA)
                  numpy.linspace(valoreQ9 - 8, valoreQ9 + 8, 10), # carico croci, per la Q faccio + e - il 5% della potenza nominale(160 kVA)
                  numpy.linspace(valoreP11 - 10, valoreP11 + 10, 20), # non avendo le curve di AltroScov ipotizzo che seguano un profilo simile a Celi
                  numpy.linspace(valoreQ11 - 5, valoreQ11 + 5, 10),
                  numpy.linspace(0, 22, 10),    # carico SLOW potenza attiva
                  numpy.linspace(-2.2, 2.2, 10),  # carico SLOW potenza reattiva
                  numpy.linspace(-Q_max_PV60, Q_max_PV60, 10),  # fotovoltaico 60kW potenza reattiva
                  numpy.linspace(0.9, 1.1, 40)   # nodo di saldo tensione pu
                  ]
    parent_selection_type = "sss"
    keep_parents = 1
    crossover_type = "single_point"
    mutation_type = "random"
    mutation_percent_genes = 10
    stop_criteria="reach_4" #Tolleranza 0.25 V

    def on_generation(ga):
        print("Generation", ga.generations_completed)
        print(ga.population)


    ga_instance = pygad.GA(num_generations=num_generations,
                           num_parents_mating=num_parents_mating,
                           fitness_func=fitness_function,
                           sol_per_pop=sol_per_pop,
                           stop_criteria=stop_criteria,
                           num_genes=num_genes,
                           gene_space=gene_space,
                           parent_selection_type=parent_selection_type,
                           keep_parents=keep_parents,
                           crossover_type=crossover_type,
                           mutation_type=mutation_type,
                           mutation_percent_genes=mutation_percent_genes,
                           initial_population=initial_population)

    start = time.time()
    ga_instance.run()
    end = time.time()

    ora_attuale = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    o = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\KPI_GA_Execution_Time.csv.txt", "a")
    o.write("\n"+ f"[{ora_attuale}];" +str(end - start))
    o.close()

    solution, solution_fitness, solution_idx = ga_instance.best_solution()
    initial_population = [solution, solution, solution, solution, solution]

    o = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\GA_Fitness.csv.txt", "a")
    o.write("\n" + f"[{ora_attuale}];" + str(1 / solution_fitness))
    o.close()

    ora_attuale = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')[:-3]

    ## CALCOLO I RISULTATI E LI MOSTRO
    dss.text(f"compile [{dss_file}]")
    carichiSE = ["Mazzocchio", "Celi", "Croci", "altroSCOV", "Slow"]
    for i in range(5):
        dss.loads_write_name(f"{carichiSE[i]}")
        dss.loads_write_kw(float(solution[2 * i]))
        dss.loads_write_kvar(float(solution[2 * i + 1]))
        json_object["d"] = solution[2 * i]
        json_object["ts"] = ora_attuale
        json_message = json.dumps(json_object, indent=4)
        client.publish("A2MQTT/" + carichiSE[i] + "/Power_P_1_7_0/Cv", json_message)
        json_object["d"] = solution[2 * i + 1]
        json_object["ts"] = ora_attuale
        json_message = json.dumps(json_object, indent=4)
        client.publish("A2MQTT/" + carichiSE[i] + "/Power_Q_3_7_0/Cv", json_message)
        #client.publish("A2MQTT/" + carichiSE[i] + "/Power_P_1_7_0/Cv","{\"d\":" + str(solution[2 * i]) + ",\"dt\":4,\"ts\":" + ora_attuale + "Z,\"q\":192}")
        #client.publish("A2MQTT/" + carichiSE[i] + "/Power_Q_3_7_0/Cv","{\"d\":" + str(solution[2 * i + 1]) + ",\"dt\":4,\"ts\":" + ora_attuale + "Z,\"q\":192}")
    dss.loads_write_name("PV60")
    dss.loads_write_kvar(float(solution[10]))
    dss.vsources_write_name("Source")
    dss.vsources_write_pu(float(solution[11]))
    dss.solution_solve()

#####Pubblicazione Tensioni
    nodi_noti = ["Storage", "Headquarters", "Fast", "PV185"]
    tensioni_calc, delta = [], []
    for i in range(4):
        dss.circuit_set_active_element(f"Load.{nodi_noti[i]}")
        tensione = dss.cktelement_voltages_mag_ang()
        tensioni_calc.append(tensione)
#        delta.append( - )
        json_object["d"] = float(misure[i] - tensioni_calc[i][0])
        json_object["ts"] = ora_attuale
        json_message = json.dumps(json_object, indent=4)
        client.publish("A2MQTT/" + nodi_noti[i] + "/Voltage_Error_U_32_7_0/Cv", json_message)

        json_object["d"] = tensioni_calc[i][0]
        json_object["ts"] = ora_attuale
        json_message = json.dumps(json_object, indent=4)
        client.publish("A2MQTT/" + nodi_noti[i] + "/Voltage_Calc_U_32_7_0/Cv", json_message)
    #dss.circuit_set_active_element(f"Load.{nodi_noti[i]}")




#### LF RESULTS HANDLING #####
    ora_attuale = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # EXPORT POWER REQUIRED BY EACH LOAD (USEFUL FOR FLEXIBILITY OPTIMIZATION)
    potenza_SE = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE.txt", "a")
    potenza_SE.write(f"[{ora_attuale}]; ")
    potenza_SE.close()

    #carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]

    for i in range(10):
        dss.circuit_set_active_element(f"Load.{carico[i]}")
        potenza = dss.cktelement_powers()
        pot_attiva= potenza[0] + potenza[2] + potenza[4]
        pot_reattiva = potenza[1] + potenza[3] + potenza[5]
        pot=[pot_attiva, pot_reattiva]
        potenza_SE = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE.txt", "a")
        potenza_SE.write(f"{pot}; ")
        potenza_SE.close()
    potenza_SE = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE.txt", "a")
    potenza_SE.write("\n")
    potenza_SE.close()

    # EXPORT VOLTAGE PU IN THE PRIMARY SUBSTATION (USEFUL FOR FLEXIBILITY OPTIMIZATION)
    tensione_pu = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensione_master.txt", "a")
    tensione_pu.write(f"[{ora_attuale}]; ")
    dss.vsources_write_name("Source")
    voltage_pu = dss.vsources_read_pu()
    tensione_pu.write(f"{voltage_pu}; ")
    tensione_pu.write("\n")
    tensione_pu.close()

    # EXPORT VOLTAGE RESULTS FOR EACH LOAD
    voltage= open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni.txt", "a")
    voltage.write(f"[{ora_attuale}]; ")
    voltage.close()
    for i in range(10):
        dss.circuit_set_active_element(f"Load.{carico[i]}")
        tensione = dss.cktelement_voltages_mag_ang()
        voltage= open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni.txt", "a")
        voltage.write(f"{tensione[0:2]}; ")
        voltage.close()
    voltage = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni.txt", "a")
    voltage.write("\n")
    voltage.close()

    # EXPORT CURRENT RESULTS FOR EACH LINE
    current = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti.txt", "a")
    current.write(f"[{ora_attuale}]; ")
    current.close()
    for j in range(11):
        dss.circuit_set_active_element(f"Line.line{j}")
        corrente = dss.cktelement_currents_mag_ang()
        current = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti.txt", "a")
        current.write(f"{corrente[0:2]}; ")
        current.close()
    current = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti.txt", "a")
    current.write("\n")
    current.close()


    # EXPORT REVERSE POWER FLOW RESULTS
    reverse = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\RPF.txt", "a")
    dss.circuit_set_active_element("Transformer.EXSIT")
    rpf = 3*dss.cktelement_powers()[0]
    reverse.write(f"[{ora_attuale}]; {rpf}; \n")    # scrivo la potenza che passa nel trasformatore EXSIT, è negativa se è RPF, positiva se va verso il carico.
    reverse.close()


#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
    # DA QUI IN POI EFFETTUO LO STUDIO SFRUTTANDO LA FLESSIBILITà
#######################################################################################################################
#######################################################################################################################
#######################################################################################################################
    if attivo_flessibilita==True:
        #valori_flusso=[]

        #reverse = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\RPF.txt", "r")
        #for riga in reverse:
        #    valori_flusso.append((float(riga.split(";")[1])))
        #reverse.close()

        # ricalcolo questi valori continuamente, così più il programma è eseguito e più è preciso,
        # posso però metterlo prima del while che così risparmio un po' di tempo
        #val_10=numpy.percentile(valori_flusso, 10)
        #val_20=numpy.percentile(valori_flusso, 20)
        #val_30=numpy.percentile(valori_flusso, 30)
        #val_40=numpy.percentile(valori_flusso, 40)
        #val_60=numpy.percentile(valori_flusso, 60)
        #val_70=numpy.percentile(valori_flusso, 70)
        #val_80=numpy.percentile(valori_flusso, 80)
        #val_90=numpy.percentile(valori_flusso, 90)

        #print("il flusso in cabina primaria rpf è", str(rpf))
        # utilizzo lo stato di carica che avevo lasciato dalla iterazione precedente
        batterie = ["BEMS", "Celi", "Mazzocchio", "Croci", "Scov", "Slow", "Fast"]
        for i in range(7):
            dss.text(f"Edit Storage.{batterie[i]} kWhstored={prossimi_kWh_stored[i]}")


        # controllo se ci sono i veicoli elettrci, e in tal caso li abilito, altrimenti no e non possono essere usati per la flessibilità
        dss.circuit_set_active_element(f"Load.Slow")
        enabled_Slow = float(dss.cktelement_powers()[0])
        if enabled_Slow > 3:
            dss.text(f"Edit Storage.Slow enabled=yes")
        else:
            dss.text(f"Edit Storage.Slow enabled=no %stored=100")

        dss.circuit_set_active_element(f"Load.Fast")
        enabled_Fast = float(dss.cktelement_powers()[0])
        if enabled_Fast > 3:
            dss.text(f"Edit Storage.Fast enabled=yes")
        else:
            dss.text(f"Edit Storage.Fast enabled=no %stored=100")


        # gestione degli storage
        if rpf<=soglia[0]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=100")

        elif rpf<=soglia[1]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=75")

        elif rpf<=soglia[2]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=50")

        elif rpf<=soglia[3]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=25")

        elif rpf<=soglia[4]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=IDLING")

        elif rpf <= soglia[5]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=discharging %discharge=25")
            dss.text(f"Edit Storage.Slow %discharge=0")
            dss.text(f"Edit Storage.Fast %discharge=0")

        elif rpf <= soglia[6]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=discharging %discharge=50")
            dss.text(f"Edit Storage.Slow %discharge=0")
            dss.text(f"Edit Storage.Fast %discharge=0")

        elif rpf <= soglia[7]:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=discharging %discharge=75")
            dss.text(f"Edit Storage.Slow %discharge=0")
            dss.text(f"Edit Storage.Fast %discharge=0")

        else:
            for i in range(7):
                dss.text(f"Edit Storage.{batterie[i]} state=discharging %discharge=100")
            dss.text(f"Edit Storage.Slow %discharge=0")
            dss.text(f"Edit Storage.Fast %discharge=0")

        dss.solution_solve()
        dss.circuit_update_storage_t()



    #### LF RESULTS HANDLING #####
        # EXPORT VOLTAGE RESULTS FOR EACH LOAD
        voltage= open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni_DR.txt", "a")
        voltage.write(f"[{ora_attuale}]; ")
        voltage.close()
        for i in range(10):
            dss.circuit_set_active_element(f"Load.{carico[i]}")
            tensione = dss.cktelement_voltages_mag_ang()
            voltage= open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni_DR.txt", "a")
            voltage.write(f"{tensione[0:2]}; ")
            voltage.close()
        voltage = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensioni_DR.txt", "a")
        voltage.write("\n")
        voltage.close()

        # EXPORT CURRENT RESULTS FOR EACH LINE
        current = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti_DR.txt", "a")
        current.write(f"[{ora_attuale}]; ")
        current.close()
        for j in range(11):
            dss.circuit_set_active_element(f"Line.line{j}")
            corrente = dss.cktelement_currents_mag_ang()
            current = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti_DR.txt", "a")
            current.write(f"{corrente[0:2]}; ")
            current.close()
        current = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\correnti_DR.txt", "a")
        current.write("\n")
        current.close()

        # EXPORT SOC RESULTS FOR EACH LINE
        state_of_charge = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\SOC_DR.txt", "a")
        state_of_charge.write(f"[{ora_attuale}]; ")
        state_of_charge.close()
        potenza = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\P_storage.txt", "a")
        potenza.write(f"[{ora_attuale}]; ")
        potenza.close()
        prossimi_kWh_stored=[]
        for elemento in batterie:
            soc=dss.text(f"? Storage.{elemento}.kWHstored")
            #print("kWh stored= ", str(soc))
            prossimi_kWh_stored.append(soc)
            P = dss.text(f"? Storage.{elemento}.kW")
            #print("P= ", str(P))
            state_of_charge = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\SOC_DR.txt", "a")
            state_of_charge.write(f"{soc}; ")
            state_of_charge.close()
            potenza = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\P_storage.txt", "a")
            potenza.write(f"{P}; ")
            potenza.close()
        state_of_charge = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\SOC_DR.txt", "a")
        state_of_charge.write("\n")
        state_of_charge.close()
        potenza = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\P_storage.txt", "a")
        potenza.write("\n")
        potenza.close()


        # EXPORT REVERSE POWER FLOW RESULTS
        reverse = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\RPF_DR.txt", "a")
        dss.circuit_set_active_element("Transformer.EXSIT")
        rpf = 3*dss.cktelement_powers()[0]
        reverse.write(f"[{ora_attuale}]; {rpf}; \n")    # scrivo la potenza che passa nel trasformatore EXSIT, è negativa se è RPF, positiva se va verso il carico.
        #print("il flusso in cabina primaria rpf_DT è", str(rpf))
        reverse.close()
        fine = time.time()
        durata = fine - inizio

    if inizio - time.time() < MAX_TIME:     # impongo che il tempo totale sia uguale a 20s
        time.sleep(MAX_TIME-(inizio - time.time()))
