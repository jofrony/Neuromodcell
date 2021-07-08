from neuromodcell.model_functions import define_mechanisms
from neuromodcell.model_functions import define_parameters
from neuromodcell.model_functions import define_morphology
from neuromodcell.model_functions import define_modulation
from neuromodcell.model_functions import files
from neuromodcell.Neuron_model_extended import NeuronModel
from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel
import pathlib
import json
import os
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

    modulation_file = json.load(open(test_dir_path / 'modulation.json','r'))

    sim = NrnSimulatorParallel(cvode_active=False)    

    test_model = NeuronModel(cell_name=cell_name,morph=morph,mech=mech,param=param, modulation=modulation)

    test_model.instantiate(sim=sim)

     
    from deepdiff import DeepDiff

    loaded_param = json.load(open(param_file,'r'))[parameterID]

    translator = {'axon' : 'axonal', 'dend' : 'basal', 'soma' : 'somatic' }
    
    model_params = list()        

    for tpart in ['axon','dend','soma']:
        for neuron_part in getattr(test_model.icell,tpart):

            sectionlist_name = translator[tpart]

            for param, spec in neuron_part.psection()['density_mechs'].items():

                for keys in spec.keys():


                    if 'maxMod' in keys and spec[keys][0] != 1.0:

                        value = spec[keys][0]

                        type_modulation = 'modulation' + keys.replace('maxMod','')

                        section_param = {
                            "dist_type": "uniform",
                            "mech": param,
                            "mech_param": keys,
                            "param_name": keys + '_' + param,
                            "sectionlist": sectionlist_name,
                            "type": "range",
                            "name": type_modulation,
                            "value": value
                        }

                        model_params.append(section_param)


            



    difference = DeepDiff(modulation_file, model_params, ignore_order=True)

    assert len(difference) == 0
         

if __name__ == "__main__":

     
     test_model_setup()

    

