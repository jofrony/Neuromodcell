from neuromodulation.NrnSimulatorParallel import NrnSimulatorParallel


def test_NrnSimulatorParallel():

    sim_test = NrnSimulatorParallel()

    assert hasattr(sim_test,'run') == True
