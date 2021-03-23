from neuromodulation.model_functions import define_mechanisms
from neuromodulation.model_functions import define_parameters
from neuromodulation.model_functions import define_morphology
from neuromodulation.model_functions import define_modulation
from neuromodulation.model_functions import files
from neuromodulation.Neuron_model_extended import NeuronModel
import pathlib
import json
import os
from neuromodulation.NrnSimulatorParallel import NrnSimulatorParallel

def test_model_setup():

    abs_path =  os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path,'test_model')
    
    parameterID = 0
    cell_name= 'test'

    param_file, morph_file, mod_file, mech_file = files(test_dir_path)

    param = define_parameters(parameter_config=param_file,parameter_id=parameterID)
    mech = define_mechanisms(mech_file)
    morph = define_morphology(morph_file=morph_file)
    modulation = define_modulation(json.load(open(test_dir_path / 'modulation.json','r')))

    sim = NrnSimulatorParallel(cvode_active=False)

    print("Running nrnivmodl:")
    os.system("rm -r $PWD/x86_64/")

    os.system("nrnivmodl examples/dSPN/mechanisms-dspn")

    sim.neuron.h.nrn_load_dll(os.getcwd() + '/x86_64/.libs/libnrnmech.so')
    

    test_model = NeuronModel(cell_name=cell_name,morph=morph,mech=mech,param=param, modulation=modulation)

    test_model.instantiate(sim=sim)

if __name__ == "__main__":

     
     test_model_setup()

    

