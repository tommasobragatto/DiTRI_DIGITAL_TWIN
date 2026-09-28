import py_dss_interface as dss
import os
import pathlib

script_path = os.path.dirname(os.path.abspath(__file__))
dss_file = pathlib.Path(script_path).joinpath("Run_DT.dss")

dss.solution_solve()
