from neuromodcell.modulation_set import DefineModulation
import pathlib
import os

def test_modulation_set():

    pathlib.Path('tmp').mkdir(parents=True, exist_ok=True)

    abs_path =  os.path.dirname(os.path.abspath(__file__))
    cell_test_folder = pathlib.Path(abs_path,'tmp')

    out_put_test_dir = cell_test_folder

    mod_set = DefineModulation(parameterID=100)
    mod_set.cell_name('test')
    mod_set.define_neuromodulation(modulationA = "neuromodulatorX")
    mod_set.new_modulation_dir(out_put_test_dir)
    mod_set.tstop = 1000
    mod_set.set_time_step(dt=0.025)
    mod_set.population = 1
    mod_set.cellDir = cell_test_folder

    mod_set.define_modulation_parameter('naf','neuromodulatorX','somatic', [0.6,0.8])
    mod_set.define_modulation_parameter('naf','neuromodulatorX','basal', [0.6,0.8])
    mod_set.define_modulation_function(modulation_function = {"function" : "bath_application","gmax" : 1})
    mod_set.define_protocol(typeEx = 'current_clamp', parameters = {"start" : 0,"duration" : 1000 , "amp" : 0.08})
    mod_set.define_selection_criteria(function = "number_AP_increase", criteria ={ "selection" : {"mean" : 6.44, "std" : 2.8, "threshold":1.5}, "parameters" : { "tstart":200,"tstop": 700}})

    mod_set.save_modulation_setup()
    mod_set.save_modulation()
    
    assert mod_set.population == 1
    
    

if __name__ == "__main__":

    test_modulation_set()
