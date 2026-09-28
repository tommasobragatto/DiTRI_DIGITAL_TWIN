import pandapower as pp #import pandapower
import network_function
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

net = network_function.iotngin_network()

## KPIs
energy_losses=[]
energy_produced=[]
energy_exported=[]
energy_consumed=[]
energy_exchanged=[]

factor=1

## IMPORTING ENERGY CONSUMPTION AND GENERATION DATA
LOADS_D=pd.read_csv('RESIDENTIAL.csv')
# LOADS_D[0][11] the first [] is for the time and the second fot the type of load
# the list of loads is:
# LOADS_D[][0] = NS0490_000
# LOADS_D[][1] = NS0495_000
# LOADS_D[][2] = NS0494_000
# LOADS_D[][3] = NS0749_000
# LOADS_D[][4] = NS0486_000
# LOADS_D[][5] = NS0487_000
# LOADS_D[][6] = NS0493_000
# LOADS_D[][7] = NS0748_000
# LOADS_D[][8] = NS0747_000
# LOADS_D[][9] = NS0492_000
# LOADS_D[][10] = NS0489_000
# LOADS_D[][11] = NS0491_000
# LOADS_D[][12] = NS0496_000

# Industrial loads
LOADS_I=pd.read_csv('INDUSTRIAL.csv')
# LOADS_I[0][11] the first [] is for the time and the second fot the type of load
# the list of loads is:
# LOADS_I[][0] = NS0490_000
# LOADS_I[][1] = NS0495_000
# LOADS_I[][2] = NS0494_000
# LOADS_I[][3] = NS0749_000
# LOADS_I[][4] = NS0486_000
# LOADS_I[][5] = NS0487_000
# LOADS_I[][6] = NS0493_000
# LOADS_I[][7] = NS0748_000
# LOADS_I[][8] = NS0747_000
# LOADS_I[][9] = NS0492_000
# LOADS_I[][10] = NS0489_000
# LOADS_I[][11] = NS0491_000
# LOADS_I[][12] = NS0496_000
PV=pd.read_csv('PV_GENERATION.csv')
# PV[0][11] the first [] is for the time and the second fot the node of the PV
# the list of PV is:
# PV[][0] = NS0490_000
# PV[][1] = NS0495_000
# PV[][2] = NS0494_000
# PV[][3] = NS0749_000
# PV[][4] = NS0486_000
# PV[][5] = NS0487_000
# PV[][6] = NS0493_000
# PV[][7] = NS0748_000
# PV[][8] = NS0747_000
# PV[][9] = NS0492_000
# PV[][10] = NS0489_000
# PV[][11] = NS0491_000
# PV[][12] = NS0496_000

# ANALYSIS OVER 24 HOURS
for i in range(np.shape(LOADS_D)[0]):  #for all the 24 hours

# ASSIGN THE CORRECT POWER VALUE FOR EACH DOMESTIC LOAD
    loads_list = LOADS_D.columns
    consumed_timestemp = 0  # power consumed in this timestemp
    for j in range(len(loads_list)):
        net.load.p_mw.at[pp.get_element_index(net, "load", loads_list[j])] = float(LOADS_D.loc[i][str(loads_list[j])])/1000   #we have to divide for 1000 because in the file RESIDENTIAL.csv  it's expressed in kw
        net.load.q_mvar.at[pp.get_element_index(net, "load", loads_list[j])] = float(LOADS_D.loc[i][str(loads_list[j])])*np.tan(np.arccos(0.9))/1000
        consumed_timestemp += float(LOADS_D.loc[i][str(loads_list[j])])/1000


# ASSIGN THE CORRECT POWER VALUE FOR EACH INDUSTRIAL LOAD
    loads_list = LOADS_I.columns
    for z in range(len(loads_list)):
        net.load.p_mw.at[pp.get_element_index(net, "load", loads_list[z])] = float(LOADS_I.loc[i][str(loads_list[z])])/1000
        net.load.q_mvar.at[pp.get_element_index(net, "load", loads_list[z])] = float(LOADS_I.loc[i][str(loads_list[z])])/1000  * np.tan(np.arccos(0.9))
        consumed_timestemp += float(LOADS_I.loc[i][str(loads_list[z])])/1000


# ASSIGN THE CORRECT POWER VALUE FOR EACH PV
    pv_list = PV.columns
    produced_timestemp=0   # power produced in this timestemp
    for k in range(len(pv_list)):
        float(PV.loc[i][str(pv_list[k])]) / 1000
        net.sgen.p_mw.at[pp.get_element_index(net, "sgen", pv_list[k])] = float(PV.loc[i][str(pv_list[k])]) / 1000
        produced_timestemp += float(PV.loc[i][str(pv_list[k])]) / 1000



# SOLVE THE SNAP SHOT OF THE CIRCUIT
    pp.runpp(net)  # solve the circuit


#  UPDATE KPIs
    energy_produced.append(float(produced_timestemp)/4)
    energy_consumed.append(float(consumed_timestemp)/4)

    power_exchange = net.res_ext_grid.p_mw.at[0]  # this is the connection line with the external grid
    losses_timestemp = abs(power_exchange + produced_timestemp - consumed_timestemp)
    energy_losses.append(losses_timestemp/4)
    energy_exchanged.append(float(power_exchange/4))
    if power_exchange>0:
        power_exchange=0
    else:
        power_exchange=-power_exchange
    energy_exported.append(power_exchange/4)



# FINAL RESULTS
if sum(energy_produced)>0:
    SCR=100*(1-(sum(energy_exported)/sum(energy_produced)))
else:
    SCR=0
print(f" the self consumption rate is {SCR} %")
SSR=100*((sum(energy_produced)-sum(energy_exported))/(sum(energy_consumed)+sum(energy_losses)))
print(f" the self sufficiency rate is {SSR} %")

print(f"energy consumed = {sum(energy_consumed)} MWh")
print(f"energy produced = {sum(energy_produced)} MWh")
print(f"energy exported = {sum(energy_exported)} MWh")
print(f"energy exchanged = {sum(energy_exchanged)} MWh")
print(f"energy losses = {sum(energy_losses)} MWh")
print(f"energy losses in % = {100*(sum(energy_losses))/(sum(energy_consumed))} MWh")