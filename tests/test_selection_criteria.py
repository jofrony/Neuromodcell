import neuromodcell.selection_criteria as sc
import numpy as np


def test_number_AP_decrease():
    voltage_control = np.array([-100, -100, 100, -100, -100, -100])
    voltage = np.array([-100, -100, -100, -100, -100, -100])

    criteria = {"selection": {"mean": 1, "std": 1, "threshold": 1}, "parameters": {'dt': 0.1}}

    result = sc.number_AP_decrease(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_number_AP_increase():
    voltage_control = np.array([-100, -100, -100, -100, -100, -100])
    voltage = np.array([-100, -100, 100, -100, -100, -100])

    criteria = {"selection": {"mean": 1, "std": 1, "threshold": 1}, "parameters": {'dt': 0.1}}

    result = sc.number_AP_increase(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_frequency_change():
    voltage_control = np.array([-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100])
    voltage = np.array([-100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100])

    criteria = {"selection": {"mean": 5, "std": 1, "threshold": 1},
                "parameters": {"tstart": 0, "tstop": 1000, 'dt': 100}}

    result = sc.frequency_change(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_frequency_increase():
    voltage_control = np.array([-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100])
    voltage = np.array([-100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100])

    criteria = {"selection": {"mean": 5, "std": 1, "threshold": 1},
                "parameters": {"tstart": 0, "tstop": 1000, 'dt': 100}}

    result = sc.frequency_change_increase(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_frequency_decrease():
    voltage_control = np.array([-100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100])
    voltage = np.array([-100, -100, -100, -100, -100, -100, -100, -100, -100, -100, -100])

    criteria = {"selection": {"mean": 5, "std": 1, "threshold": 1},
                "parameters": {"tstart": 0, "tstop": 1000, 'dt': 100}}

    result = sc.frequency_change_decrease(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_cv_change():
    voltage_control = np.array([-100, 100, -100, 100, -100, 100, -100, 100, -100, 100, -100])
    voltage = np.array([-100, -100, -100, 100, -100, -100, -100, 100, -100, 100, -100])

    criteria = {"selection": {"mean": 0.333, "std": 1, "threshold": 1}, "parameters": {'dt': 100}}

    result = sc.cv_change(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True


def test_membrane_amplitude_increase():
    voltage_control = np.array([-100, -100, -100, -100, -90, -90, -90, -90, -100, -100, -100, -100])
    voltage = np.array([-100, -100, -100, -100, -80, -80, -80, -80, -100, -100, -100, -100])

    criteria = {"selection": {"mean": 10, "std": 1, "threshold": 1},
                "parameters": {'start_base': 0, 'stop_base': 0.2, 'start_measure': 0.4, 'stop_measure': 0.8, 'dt': 0.1}}

    result = sc.membrane_amplitude_increase(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_membrane_amplitude_increase_percentage():
    voltage_control = np.array([-100, -100, -100, -100, -90, -90, -90, -90, -100, -100, -100, -100])
    voltage = np.array([-100, -100, -100, -100, -80, -80, -80, -80, -100, -100, -100, -100])

    criteria = {"selection": {"mean": 200, "std": 1, "threshold": 1},
                "parameters": {'start_base': 0, 'stop_base': 0.2, 'start_measure': 0.4, 'stop_measure': 0.8, 'dt': 0.1}}

    result = sc.membrane_amplitude_increase_percentage(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0


def test_membrane_amplitude_decrease_percentage():
    voltage_control = np.array([-100, -100, -100, -100, -80, -80, -80, -80, -100, -100, -100, -100])
    voltage = np.array([-100, -100, -100, -100, -90, -90, -90, -90, -100, -100, -100, -100])

    criteria = {"selection": {"mean": 50, "std": 1, "threshold": 1},
                "parameters": {'start_base': 0, 'stop_base': 0.2, 'start_measure': 0.4, 'stop_measure': 0.8, 'dt': 0.1}}

    result = sc.membrane_amplitude_decrease_percentage(criteria, [voltage_control, voltage])

    boolean = result['boolean']
    zscore = result['zscore']

    assert boolean == True
    assert zscore == 0
