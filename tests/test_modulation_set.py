import numpy as np

from neuromodcell.modulation_set import DefineModulation
from neuromodcell.modulation_set import NumpyEncoder
import pytest


def test_DefineModulation():
    _ = DefineModulation()

    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    _ = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                         output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)


def test_DefineModulation_raise_typeerror():
    _ = DefineModulation()

    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = 10
    population = 10
    tstop = 100
    time_step = 1
    with pytest.raises(TypeError):
        _ = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                             output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)


def test_set_time_step():
    a = DefineModulation()
    a.set_time_step(dt=10)

    assert a.dt == 10


def test_cell_name():
    a = DefineModulation()
    a.cell_name(name="test")

    assert a.name == "test"


def test_define_neuromodulation():
    a = DefineModulation()
    a.define_neuromodulation(modulationDA="dopamine")

    assert a.neuromodulation_name["dopamine"] == "modulationDA"


def test_define_modulation_function():
    a = DefineModulation()

    with pytest.raises(AttributeError):
        a.define_modulation_function(modulation_function="alpha")

    a = DefineModulation(tstop=10)
    a.set_time_step(dt=5)
    a.define_modulation_function(modulation_function="alpha")

    a = DefineModulation(tstop=10)
    a.set_time_step(dt=None)
    with pytest.raises(UnboundLocalError):
        a.define_modulation_function(modulation_function="alpha", gmax=10, tau=10)


def test_define_selection_criteria():
    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    a = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                         output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)

    a.define_selection_criteria(function="number_AP_increase", mean=6.44, std=2.8,
                                threshold=1.5, tstart=200, tstop=700)


def test_define_protocol():
    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    a = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                         output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)

    a.define_protocol(typeEx="current_clamp", start=200, duration=500, amp=0.5)


def test_define_modulation_receptor():
    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    a = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                         output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)
    a.define_neuromodulation(modulationDA="dopamine")
    a.define_modulation_receptor(syn="tmGaba", neuromod="dopamine", syn_param="tmGabaA",
                                 modulation_param={"failrate": [0.1, 0.5]})


def test_define_modulation_parameter():
    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    a = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                         output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)
    a.define_neuromodulation(modulationDA="dopamine")
    a.define_modulation_parameter('can_ms', 'dopamine', 'somatic', [0.2, 1])


def test_save_modulation():

    parameterID = 0
    cell_name = "test"
    cell_dir = "test_dir"
    output_dir = "test_out"
    population = 10
    tstop = 100
    time_step = 1
    a = DefineModulation(parameterID=parameterID, cell_name=cell_name, cell_dir=cell_dir,
                         output_dir=output_dir, population=population, tstop=tstop, time_step=time_step)

    a.define_neuromodulation(modulationDA="dopamine")
    print(a.neuromodulationDir)
    a.new_modulation_dir(directory="try")
    a.save_modulation(name=None)
    a.save_modulation_setup(name=None)
    a.save_modulation(name="mod.json")
    a.save_modulation_setup(name="mod.json")

def test_numpy_decoder():

    import pathlib
    import numpy as np
    a = NumpyEncoder()
    a.default(np.array([0, 1], dtype=int))
    a.default(np.array([0, 1], dtype=float))
    a.default(np.array([0, 1]))
    a.default(pathlib.PosixPath('string'))

if __name__ == "__main__":
    test_DefineModulation()
