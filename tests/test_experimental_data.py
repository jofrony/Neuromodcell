from neuromodcell.experimental_data import experimental


def test_experimental():

    exp_trial = experimental()

    exp_trial.define_exp(mean = 2)

    assert exp_trial.experimental_data['mean'] == 2


