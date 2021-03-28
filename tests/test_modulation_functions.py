import neuromodulation.modulation_functions as mf
import numpy as np

def test_alpha():

    parameters = {'time_step_array' : np.arange(0,100,0.025),
                  'tstart' : 10,
                  'gmax' : 1,
                  'tau' : 10}
    magnitudes = mf.alpha(parameter=parameters)

    assert isinstance(magnitudes,list) == True

def test_step():

    parameters = {'time_step_array' : np.arange(0,100,0.025),
                  'tstart' : 10,
                  'gmax' : 1,
                  'duration' : 50}

    magnitudes = mf.step(parameter=parameters)

    assert isinstance(magnitudes,list) == True

def test_bath_application():

    parameters = {'time_step_array' : np.arange(0,100,0.025),
                  'gmax' : 1}

    magnitudes = mf.bath_application(parameter=parameters)

    assert isinstance(magnitudes,list) == True


def test_alpha_background():


    parameters = {'time_step_array' : np.arange(0,100,0.025),
                  'tstart' : 10,
                  'gmax_decrease' : 0.5,
                  'tau' : 10,
                  'tonic' : 1}

    magnitudes = mf.alpha_background(parameter=parameters)

    assert isinstance(magnitudes,list) == True

def test_time_series():

    parameters = {'array' : '[0,1]'}

    magnitudes = mf.time_series(parameter=parameters)

    assert isinstance(magnitudes,list) == True

    
