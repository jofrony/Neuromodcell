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
    abs_path = os.path.dirname(os.path.abspath(__file__))
    print(abs_path)
    test_dir_path = pathlib.Path(abs_path, 'test_model')

    parameter_id = 0
    cell_name = 'test'

    param_file, morph_file, mod_file, mech_file = files(test_dir_path)

    param = define_parameters(parameter_config=param_file, parameter_id=parameter_id)
    mech = define_mechanisms(mech_file)
    morph = define_morphology(morph_file=morph_file, replaceAxon=False)
    modulation = define_modulation(json.load(open(test_dir_path / 'modulation.json', 'r')))

    sim = NrnSimulatorParallel(cvode_active=False)

    print("Running nrnivmodl:")

    os.system("rm -r $PWD/x86_64/")

    os.system("nrnivmodl examples/dSPN/mechanisms-dspn")

    sim.neuron.h.nrn_load_dll(os.getcwd() + '/x86_64/.libs/libnrnmech.so')

    test_model = NeuronModel(cell_name=cell_name, morph=morph, mech=mech, param=param, modulation=modulation)

    test_model.instantiate(sim=sim)

    from deepdiff import DeepDiff

    loaded_param = json.load(open(param_file, 'r'))[parameter_id]

    model_params = list()

    for global_param in ['celsius', 'v_init']:
        glob_dict = {
            "param_name": global_param,
            "type": "global",
            "value": getattr(sim.neuron.h, global_param)
        }
        model_params.append(glob_dict)

    difference = DeepDiff(loaded_param[0:2], model_params, ignore_order=True)

    assert len(difference) == 0

if __name__ == '__main__':

    test_model_setup()