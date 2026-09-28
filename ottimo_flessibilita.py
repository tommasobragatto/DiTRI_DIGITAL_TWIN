import py_dss_interface
import os
import pathlib
import pygad

def threshold_flexibility():
        script_path = os.path.dirname(os.path.abspath(__file__))
        dss_file = pathlib.Path(script_path).joinpath("Run_DT.dss")
        dss=py_dss_interface.DSSDLL()

        # CARICO corresponds to the buses that we would like to monitor
        carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60", "altroSCOV"]
        prossimi_kWh_stored=[15, 5, 2.5, 8, 33, 35, 35]

        # 1) leggo i valori dal file potenza_SE e li salvo dentro valori_P e valori_Q
        # dentro valori_P e valori_Q la riga indica il carico, quindi va da 1 a 10, mentre la colonna indica il timestemp
        potenza_SE = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\potenza_SE.txt", "r")
        p=potenza_SE.read()
        potenza_SE.close()
        p=p.split("\n")
        numero_righe=len(p)-1
        for i in range(numero_righe):
                p[i]=p[i].split(";")

        valori_P=[[],[],[],[],[],[],[],[],[],[]]
        valori_Q=[[],[],[],[],[],[],[],[],[],[]]
        for j in range(numero_righe):  # per ogni riga
                for c in range(10):  # per ogni carico
                        p[j][c + 1] = p[j][c + 1].strip("[] ")
                        p[j][c+1]=p[j][c+1].split(",")
                        att=float(p[j][c + 1][0])
                        rea=float(p[j][c + 1][1])
                        valori_P[c].append(att)
                        valori_Q[c].append(rea)


        # 2) leggo i valori dal file tensione_master e li salvo dentro tensione_vsource
        # tensione_vsource è un vettore con tutte i valori della tensione in pu nel nodo della cabina primaria
        tensione_pu = open(r"C:\Users\Alberto\PycharmProjects\py-dss-interface\data\results\tensione_master.txt", "r")
        v = tensione_pu.read()
        tensione_pu.close()
        v = v.split("\n")
        numero_righe = len(p) - 1
        for i in range(numero_righe):
                v[i] = v[i].split(";")

        tensione_vsource = []
        for j in range(numero_righe):  # per ogni riga
                val = float(v[j][1])
                tensione_vsource.append(val)





        def fitness_func(solution, solution_idx):
                carico = ["Headquarters", "Slow", "Mazzocchio", "Celi", "Storage", "Fast", "Croci", "PV185", "PV60",
                          "altroSCOV"]
                prossimi_kWh_stored = [15, 5, 2.5, 8, 33, 35, 35]
                dss.text(f"compile [{dss_file}]")

                # inserisco il valore di P e di Q in tutti timestemps
                Eimmessa=0
                Eprodotta=0
                for tempo in range(numero_righe):

                        for i in range(10):
                                dss.loads_write_name(f"{carico[i]}")
                                dss.loads_write_kw(valori_P[i][tempo])
                                dss.loads_write_kvar(valori_Q[i][tempo])
                        dss.vsources_write_name("Source")
                        dss.vsources_write_pu(tensione_vsource[tempo])

                        # utilizzo lo stato di carica che avevo lasciato dalla iterazione precedente
                        batterie = ["BEMS", "Celi", "Mazzocchio", "Croci", "Scov", "Slow", "Fast"]
                        for i in range(7):
                                dss.text(f"Edit Storage.{batterie[i]} kWhstored={prossimi_kWh_stored[i]}")

                        dss.text(f"Edit Storage.Slow enabled=no %stored=100")
                        dss.text(f"Edit Storage.Fast enabled=no %stored=100")


                        dss.circuit_set_active_element("Transformer.EXSIT")
                        flusso = 3 * dss.cktelement_powers()[0]

                        # gestione degli storage
                        if flusso <= solution[0]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=100")

                        elif flusso <= solution[1]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=75")

                        elif flusso <= solution[2]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=50")

                        elif flusso <= solution[3]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=charging %charge=25")

                        elif flusso <= solution[4]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=IDLING")

                        elif flusso <= solution[5]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=discharging %discharge=25")
                                        dss.text(f"Edit Storage.Slow %discharge=0")
                                        dss.text(f"Edit Storage.Fast %discharge=0")

                        elif flusso <= solution[6]:
                                for i in range(7):
                                        dss.text(f"Edit Storage.{batterie[i]} state=discharging %discharge=50")
                                        dss.text(f"Edit Storage.Slow %discharge=0")
                                        dss.text(f"Edit Storage.Fast %discharge=0")

                        elif flusso <= solution[7]:
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

                        # UPDATE SOC RESULTS FOR EACH LINE
                        prossimi_kWh_stored = []
                        for elemento in batterie:
                                soc = dss.text(f"? Storage.{elemento}.kWHstored")
                                prossimi_kWh_stored.append(soc)

                        dss.circuit_set_active_element("Transformer.EXSIT")
                        flowPS = float(3 * dss.cktelement_powers()[0])

                        if flowPS < 0:
                                Eimmessa += abs(flowPS) * (1/6)  # divido per perchè i dati sono misurati ogni 10 minuti e così lo riporto in kWh

                        dss.circuit_set_active_element("Load.PV60")
                        Eprod_PV60 = 3*dss.cktelement_powers()[0]
                        dss.circuit_set_active_element("Load.PV185")
                        Eprod_PV185 = 3*dss.cktelement_powers()[0]
                        Eprodotta += (abs(Eprod_PV60) + abs(Eprod_PV185)) * (1/6)  # divido per perchè i dati sono misurati ogni 10 minuti e così lo riporto in kWh
                fitness = 1 - Eimmessa/Eprodotta
                return fitness


        fitness_function = fitness_func

        num_generations = 100
        num_parents_mating = 4
        sol_per_pop = 5
        num_genes = 8

        init_range_low = -200
        init_range_high = 400
        parent_selection_type = "sss"
        keep_parents = 1
        crossover_type = "single_point"
        mutation_type = "random"
        mutation_percent_genes = 10
        soluzione_iniziale=[-12,  13,  41,  53, 120, 164, 172, 265]
        gene_space = [{'low': soluzione_iniziale[0]-50, 'high': soluzione_iniziale[0]+50}, {'low': soluzione_iniziale[1]-50, 'high': soluzione_iniziale[1]+50}, {'low': soluzione_iniziale[2]-50, 'high': soluzione_iniziale[2]+50}, {'low': soluzione_iniziale[3]-50, 'high': soluzione_iniziale[3]+50}, {'low': soluzione_iniziale[4]-50, 'high': soluzione_iniziale[4]+50}, {'low': soluzione_iniziale[5]-50, 'high': soluzione_iniziale[5]+50}, {'low': soluzione_iniziale[6]-50, 'high': soluzione_iniziale[6]+50}, {'low': soluzione_iniziale[7]-50, 'high': soluzione_iniziale[7]+50}]
        initial_population=[soluzione_iniziale, soluzione_iniziale, soluzione_iniziale, soluzione_iniziale, soluzione_iniziale]

        def on_generation(ga):
            print("Generation", ga.generations_completed)
            print(ga.population)

        ga_instance = pygad.GA(num_generations=num_generations,
                               num_parents_mating=num_parents_mating,
                               fitness_func=fitness_function,
                               sol_per_pop=sol_per_pop,
                               num_genes=num_genes,
                               gene_space=gene_space,
                               parent_selection_type=parent_selection_type,
                               keep_parents=keep_parents,
                               crossover_type=crossover_type,
                               mutation_type=mutation_type,
                               mutation_percent_genes=mutation_percent_genes,
                               gene_type=int,
                               initial_population=initial_population,
                               stop_criteria=["saturate_5"])

        ga_instance.run()

        solution, solution_fitness, solution_idx = ga_instance.best_solution()

        return(solution)
