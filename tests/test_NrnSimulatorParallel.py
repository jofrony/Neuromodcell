from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel


def test_NrnSimulatorParallel():
    sim_test = NrnSimulatorParallel()

    assert hasattr(sim_test, 'run') == True

    sim_test = NrnSimulatorParallel(cvode_active=True)

    assert sim_test.neuron.h.cvode_active() == 1

    sim_test = NrnSimulatorParallel(cvode_active=True)
    sim_test.run(tstop=10, dt=0.1)

    assert sim_test.neuron.h.tstop == 10
    assert sim_test.neuron.h.dt == 0.1
