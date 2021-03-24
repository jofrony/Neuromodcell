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
    morph = define_morphology(morph_file=morph_file,replaceAxon=False)
    modulation = define_modulation(json.load(open(test_dir_path / 'modulation.json','r')))

    sim = NrnSimulatorParallel(cvode_active=False)

    print("Running nrnivmodl:")
    os.system("rm -r $PWD/x86_64/")

    os.system("nrnivmodl examples/dSPN/mechanisms-dspn")

    sim.neuron.h.nrn_load_dll(os.getcwd() + '/x86_64/.libs/libnrnmech.so')
    

    test_model = NeuronModel(cell_name=cell_name,morph=morph,mech=mech,param=param, modulation=[])

    test_model.instantiate(sim=sim)

     
    from deepdiff import DeepDiff

    loaded_param = json.load(open(param_file,'r'))[parameterID]


    model_params = list()        

    for tpart in ['axon','dend','soma']:
        for neuron_part in getattr(test_model.icell,tpart):

            import pdb
            pdb.set_trace()


            section_param = {
		"dist_type": "uniform",
		"param_name": "g_pas",
		"sectionlist": "axonal",
		"type": "section",
		"value": 0.0007134535418891711
            }

            
            model_params.append(section_param)



    difference = DeepDiff(loaded_param[2:], model_params, ignore_order=True)

    import pprint

    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(difference)

    assert len(difference) == 0


   
        

   
                

if __name__ == "__main__":

     
     test_model_setup()

    

