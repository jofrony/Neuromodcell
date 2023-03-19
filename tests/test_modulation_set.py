from neuromodcell.modulation_set import DefineModulation
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


if __name__ == "__main__":
    test_DefineModulation()
