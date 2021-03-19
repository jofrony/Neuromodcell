from neuromodulation.selection_functions import number_action_potentials

def test_number_action_potentials():

    voltage = [-100,-100,-100,100,-100,-100]
    parameters = {'dt' : 0.025}

    assert number_action_potentials(voltage,parameters) == 1
