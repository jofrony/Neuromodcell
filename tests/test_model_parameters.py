from neuromodcell.model_functions import define_mechanisms
from neuromodcell.model_functions import define_parameters
from neuromodcell.model_functions import define_morphology
from neuromodcell.model_functions import define_modulation
from neuromodcell.model_functions import files
from neuromodcell.Neuron_model_extended import NeuronModel
from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel
from .compile_mechanisms import compile_mechanisms
import pathlib
import json
import os
import pytest

def test_files():

    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_model')

    _, _, _, _ = files(test_dir_path)

    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_model_broken')

    with pytest.raises(ValueError) as e:
        _, _, _, _ = files(test_dir_path)

def test_model_param():

    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_model_param_v1')

    parameterID = 0
    param_file, morph_file, mod_file, mech_file = files(test_dir_path)

    param = define_parameters(parameter_config=param_file, parameter_id=parameterID)

    test_dir_path = pathlib.Path(abs_path, 'test_model_param_v2')

    parameterID = 0
    param_file, morph_file, mod_file, mech_file = files(test_dir_path)

    with pytest.raises(Exception) as e:
        param = define_parameters(parameter_config=param_file, parameter_id=parameterID)

    with pytest.raises(Exception) as r:
        _ = define_parameters(parameter_config=None,parameter_id=0)

def test_model_modulation():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_model')

    parameterID = 0
    param_file, morph_file, mod_file, mech_file = files(test_dir_path)

    m = json.load(open(mod_file))
    _ = define_modulation(param_set=m)



def test_model_setup():

    abs_path =  os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_model')

    parameterID = 0
    cell_name = 'test'

    param_file, morph_file, mod_file, mech_file = files(test_dir_path)

    param = define_parameters(parameter_config=param_file,parameter_id=parameterID)
    mech = define_mechanisms(mech_file)
    morph = define_morphology(morph_file=morph_file,replaceAxon=False)

    sim = NrnSimulatorParallel(cvode_active=False)    

    test_model = NeuronModel(cell_name=cell_name,morph=morph,mech=mech,param=param, modulation=[])

    test_model.instantiate(sim=sim)

     
    from deepdiff import DeepDiff

    loaded_param = json.load(open(param_file,'r'))[parameterID]


    model_params = list()

    translator = {'axon' : 'axonal', 'dend' : 'basal', 'soma' : 'somatic' }

    for tpart in ['axon','dend','soma']:
        for neuron_part in getattr(test_model.icell,tpart):

            sectionlist_name = translator[tpart]

            for ion, ion_spec in neuron_part.psection()['ions'].items():


                reversal = next(iter(ion_spec))

                value = ion_spec[reversal][0]

                section_param = {
		    "dist_type": "uniform",
		    "param_name": reversal,
		    "sectionlist": sectionlist_name,
		    "type": "section",
		    "value":  value
	        }

                model_params.append(section_param)

            


            section_param = {
                    "dist_type": "uniform",
                    "param_name": 'cm',
                    "sectionlist": sectionlist_name,
                    "type": "section",
                    "value": neuron_part.psection()['cm'][0]
                }

            model_params.append(section_param)



            
            section_param = {
                    "dist_type": "uniform",
                    "param_name": 'Ra',
                    "sectionlist": sectionlist_name,
                    "type": "section",
                    "value": neuron_part.psection()['Ra']
                }

            model_params.append(section_param)
            

            for param, spec in neuron_part.psection()['density_mechs'].items():


                if param == 'pas':

                    iterator = iter(spec)
                    param_key = next(iterator)

                    param_name = '_'.join([param_key,param])

                    value = spec[param_key][0]


                    section_param = {
                        "dist_type": "uniform",
                        "param_name": param_name,
                        "sectionlist": sectionlist_name,
                        "type": "section",
                        "value": value
                    }

                    model_params.append(section_param)

                    param_key = next(iterator)

                    param_name = '_'.join([param_key,param])

                    value = spec[param_key][0]


                    section_param = {
                        "dist_type": "uniform",
                        "param_name": param_name,
                        "sectionlist": sectionlist_name,
                        "type": "section",
                        "value": value
                    }
        

            
                    model_params.append(section_param)

                else:

                    
                    param_key = next(iter(spec))

                    param_name = '_'.join([param_key,param])

                    value = spec[param_key][0]


                    section_param = {
                        "dist_type": "uniform",
                        "mech" : param,
                        "mech_param" : param_key,
                        "param_name": param_name,
                        "sectionlist": sectionlist_name,
                        "type": "range",
                        "value": value
                    }

                    model_params.append(section_param)


    difference = DeepDiff(loaded_param[2:], model_params, ignore_order=True)

    assert len(difference) == 0

if __name__ == "__main__":

     
     test_model_modulation()

    

