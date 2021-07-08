from neuromodcell.optimisation_setup import OptimisationSetup
from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel
import json
import os
import pathlib


def test_optimisation_setup():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_data')

    modulation_setup = json.load(open(test_dir_path / 'modulation_setup.json'))

    unit_modulation = {'receptor': [[]], 'param_set': [[]]}

    sim = NrnSimulatorParallel(cvode_active=False)

    opt = OptimisationSetup(modulation_setup)
    opt.set_gidlist([0])
    opt.start_logging()

    opt.setup_neurons(unit_modulation)
    opt.control_neuron()

    opt.setup_neurons(opt.unit_modulation)

    opt.define_neuromodulation()

    opt.instantiate(sim=sim)

    t_save = opt.time_save()

    v_save = opt.voltage_save()

    opt.define_ion_channel()

    opt.define_receptor()

    opt.define_protocol()

    opt.run()
