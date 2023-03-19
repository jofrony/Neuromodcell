import pytest

from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel


def test_NrnSimulatorParallel():
    sim_test = NrnSimulatorParallel()

    assert hasattr(sim_test, 'run') == True

    sim_test = NrnSimulatorParallel(cvode_active=True, dt=0.1)

    assert sim_test.neuron.h.cvode_active() == 1

    sim_test = NrnSimulatorParallel(cvode_active=True)
    sim_test.run(tstop=10)

    assert sim_test.neuron.h.tstop == 10
    assert sim_test.neuron.h.dt == 0.1


def test_NrnSimulatorParallel_cvode():

    sim_test = NrnSimulatorParallel()
    with pytest.raises(ValueError):
        sim_test.run(tstop=10, cvode_active=True, dt=0.5)

    with pytest.raises(Exception):
        sim_test.neuron.h.dt = 0.5
        sim_test.run(tstop=10, cvode_active=False, dt=None)

    sim_test = NrnSimulatorParallel()
    sim_test.run(tstop=10, cvode_active=False, dt=None)

    sim_test = NrnSimulatorParallel()
    sim_test.run(tstop=10, cvode_active=False)

    sim_test = NrnSimulatorParallel()
    sim_test.run(tstop=10, cvode_active=False, random123_globalindex=1)

    sim_test = NrnSimulatorParallel(cvode_minstep=0.1)
    sim_test.run(tstop=10, cvode_active=False)