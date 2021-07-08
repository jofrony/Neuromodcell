import neuromodcell.selection_functions as sf
import numpy as np


def test_number_action_potentials():
    voltage = np.array([-100, -100, -100, 100, -100, -100])
    parameters = {'dt': 0.025}

    assert sf.number_action_potentials(voltage, parameters) == 1


def test_mean_frequency():
    voltage = np.array([-100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100])

    parameters = {"tstart": 0, "tstop": 1000, 'dt': 100}

    assert sf.mean_frequency(voltage, parameters) == 5


def test_ISI():
    voltage = np.array([-100, -100, 100, -100, -100, 100, -100, -100])

    parameters = {'dt': 100}

    assert sf.ISI(voltage, parameters)[0] == 0.3


def test_cv():
    voltage = np.array([-100, -100, 100, -100, 100, -100, -100, 100, -100, -100, 100])
    parameters = {'dt': 100}

    assert sf.cv(voltage, parameters) == 0.17677669529663687


def test_membrane_amplitude():
    voltage = np.array([-100, -100, -100, -100, -80, -80, -80, -80, -100, -100, -100, -100])

    parameters = {'start_base': 0, 'stop_base': 0.2, 'start_measure': 0.4, 'stop_measure': 0.8, 'dt': 0.1}

    assert sf.membrane_amplitude(voltage, parameters) == 20


def test_synaptic_amplitude():
    voltage = np.array([-100, -100, -100, -100, -80, -80, -80, -80, -100, -100, -100, -100])

    parameters = {'start_base': 0, 'stop_base': 0.2, 'start_measure': 0.4, 'stop_measure': 0.8, 'dt': 0.1}

    assert sf.synaptic_amplitude(voltage, parameters) == 20
