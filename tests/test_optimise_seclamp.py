from neuromodulation.optimise_seclamp import Optimise_modulation_seclamp
import os
import pathlib

def test_optimise_seclamp():


    abs_path =  os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path,'test_data')
    
    Opt = Optimise_modulation_seclamp(setup = test_dir_path)

    Opt.setup_load()
    Opt.set_gids()
    Opt.set_seed(1234)
    Opt.modulation_list()

