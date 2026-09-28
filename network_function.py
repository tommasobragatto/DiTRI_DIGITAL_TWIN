import pandapower as pp #import pandapower

def asm_feeder_network():

    net = pp.create_empty_network() #create an empty network

    # create the buses
    bus1 = pp.create_bus(net, vn_kv=20, name="EXSIT", geodata=(12.59, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)
    bus2 = pp.create_bus(net, vn_kv=20, name="ASM", geodata=(12.593, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)
    bus3 = pp.create_bus(net, vn_kv=20, name="ns_01", geodata=(12.596, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)
    bus4 = pp.create_bus(net, vn_kv=20, name="LECROCI2", geodata=(12.599, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)
    bus5 = pp.create_bus(net, vn_kv=20, name="ATC", geodata=(12.619224, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)
    bus6 = pp.create_bus(net, vn_kv=20, name="MAZZOCCHIO", geodata=(12.62, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)
    bus7 = pp.create_bus(net, vn_kv=20, name="SCOV", geodata=(12.62082, 42.537051), type='b', in_service=True, max_vm_pu=1.1, min_vm_pu=0.9)


    # create the external grid connection
    pp.create_ext_grid(net, pp.get_element_index(net, "bus", "EXSIT"), vm_pu=1.0, va_degree=0.0, name="ASM_Grid", in_service=True, s_sc_max_mva=31000, rx_max=0.125, r0x0_max=0.25)

    # create the linecodes
    pp.create_std_type(net, data={"r_ohm_per_km":0.193, "x_ohm_per_km":0.103, "c_nf_per_km":246, "max_i_ka":301, "type":"cs"}, name="Cu_95_UC", element='line', overwrite=True, check_required=True)
    pp.create_std_type(net, data={"r_ohm_per_km":0.387, "x_ohm_per_km":0.125, "c_nf_per_km":195, "max_i_ka":177, "type":"cs"}, name="Cu_50_UC", element='line', overwrite=True, check_required=True)


    # create the lines
    line1 = pp.create_line(net, from_bus=pp.get_element_index(net, "bus", "EXSIT"), to_bus=pp.get_element_index(net, "bus", "ASM"), length_km=0.463, std_type="Cu_95_UC", name="LINE_1")
    line2 = pp.create_line(net, from_bus=pp.get_element_index(net, "bus", "ASM"), to_bus=pp.get_element_index(net, "bus", "ns_01"), length_km=0.0382, std_type="Cu_95_UC", name="LINE_2")
    line3 = pp.create_line(net, from_bus=pp.get_element_index(net, "bus", "ns_01"), to_bus=pp.get_element_index(net, "bus", "LECROCI2"), length_km=0.552, std_type="Cu_50_UC", name="LINE_3")
    line4 = pp.create_line(net, from_bus=pp.get_element_index(net, "bus", "ASM"), to_bus=pp.get_element_index(net, "bus", "ATC"), length_km=0.421, std_type="Cu_95_UC", name="LINE_4")
    line5 = pp.create_line(net, from_bus=pp.get_element_index(net, "bus", "ATC"), to_bus=pp.get_element_index(net, "bus","MAZZOCCHIO"), length_km=0.162, std_type="Cu_50_UC", name="LINE_5")
    line6 = pp.create_line(net, from_bus=pp.get_element_index(net, "bus", "MAZZOCCHIO"), to_bus=pp.get_element_index(net, "bus", "SCOV"), length_km=0.364, std_type="Cu_50_UC", name="LINE_6")
    
    # create domestic loads
    pp.create_load(net, bus=pp.get_element_index(net, "bus", "ASM"), p_mw=0.050, q_mvar=0, name="Load_ASM", scaling=1.0, in_service=True, type='wye')
    pp.create_load(net, bus=pp.get_element_index(net, "bus", "LECROCI2"), p_mw=0.050, q_mvar=0, name="Load_LECROCI2", scaling=1.0, in_service=True, type='wye')
    pp.create_load(net, bus=pp.get_element_index(net, "bus", "ATC"), p_mw=0.050, q_mvar=0, name="Load_ATC", scaling=1.0, in_service=True, type='wye')
    pp.create_load(net, bus=pp.get_element_index(net, "bus", "MAZZOCCHIO"), p_mw=0.050, q_mvar=0, name="Load_MAZZOCCHIO", scaling=1.0, in_service=True, type='wye')
    pp.create_load(net, bus=pp.get_element_index(net, "bus", "SCOV"), p_mw=0.050, q_mvar=0, name="Load_SCOV", scaling=1.0, in_service=True, type='wye')
    pp.create_load(net, bus=pp.get_element_index(net, "bus", "SCOV"), p_mw=0.7, q_mvar=0, name="Load_SCOV_PV", scaling=1.0, in_service=True, type='wye')



    return net
