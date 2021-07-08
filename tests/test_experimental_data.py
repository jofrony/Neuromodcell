from neuromodcell.experimental_data import Experimental


def test_experimental():

    exp_trial = Experimental()

    exp_trial.define_exp(mean = 2)

    assert exp_trial.experimental_data['mean'] == 2


