from neuromodulation.modulation_set import defineModulation
import pathlib
import os

def test_modulation_set():

    pathlib.Path('tmp').mkdir(parents=True, exist_ok=True)

    abs_path =  os.path.dirname(os.path.abspath(__file__))
    cell_test_folder = pathlib.Path(abs_path,'tmp')

    out_put_test_dir = cell_test_folder

    ModSet = defineModulation(parameterID=100)
    ModSet.cell_name('test')
    ModSet.define_neuromodulation(modulationA = "neuromodulatorX")
    ModSet.new_modulation_dir(out_put_test_dir)
    ModSet.tstop = 1000
    ModSet.set_time_step(dt=0.025)
    ModSet.population = 1
    ModSet.cellDir = cell_test_folder

    ModSet.define_modulation_parameter('naf','neuromodulatorX','somatic', [0.6,0.8])
    ModSet.define_modulation_parameter('naf','neuromodulatorX','basal', [0.6,0.8])
    ModSet.define_modulation_function(modulation_function = {"function" : "bath_application","gmax" : 1})
    ModSet.define_protocol(typeEx = 'current_clamp', parameters = {"start" : 0,"duration" : 1000 , "amp" : 0.08})
    ModSet.define_selection_criteria(function = "number_AP_increase", criteria ={ "selection" : {"mean" : 6.44, "std" : 2.8, "threshold":1.5}, "parameters" : { "tstart":200,"tstop": 700}})

    ModSet.save_modulation_setup()
    ModSet.save_modulation()
    
    assert  ModSet.population == 1
    
    

if __name__ == "__main__":

    test_modulation_set()
