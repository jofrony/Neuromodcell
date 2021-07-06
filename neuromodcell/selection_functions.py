import elephant as elp
import neo
import quantities as pq
import numpy as np

'''

Functions which calculates the specific value which is evaluated in the criteria


'''

def number_action_potentials(voltage,parameters):

    neo_voltage = neo.AnalogSignal(np.array(voltage)*pq.mV,sampling_period=parameters["dt"]*pq.ms,units='mV')
    spike_train = elp.spike_train_generation.peak_detection(neo_voltage,threshold=-20 *pq.mV)

    num_AP = len(spike_train)

    return num_AP

    

def mean_frequency(voltage,parameters):

    neo_voltage = neo.AnalogSignal(np.array(voltage)*pq.mV,sampling_period=parameters["dt"]*pq.ms,units='mV')
    spike_train = elp.spike_train_generation.peak_detection(neo_voltage,threshold=-20 *pq.mV)

    if len(spike_train)==0:

        mean_fr = np.array(0)/ 1 * pq.s

    else:

        mean_fr = elp.statistics.mean_firing_rate(spike_train,t_start=parameters["tstart"]*pq.ms, t_stop=parameters["tstop"]*pq.ms)


    return mean_fr

def ISI(voltage,parameters):

    neo_voltage = neo.AnalogSignal(np.array(voltage)*pq.mV,sampling_period=parameters["dt"]*pq.ms,units='mV')
    spike_train = elp.spike_train_generation.peak_detection(neo_voltage)
    isi = elp.statistics.isi(spike_train)

    return isi

def cv(voltage,parameters):

    isi = ISI(voltage,parameters)
    cv_isi = elp.statistics.cv(isi)
    
    return cv_isi


def membrane_amplitude(voltage,parameters):
    
    start_slice = int(parameters['start_base']/parameters['dt'])

    stop_slice = int(parameters['stop_base']/parameters['dt'])

    start_measure = int(parameters['start_measure']/parameters['dt'])
    
    stop_measure = int(parameters['stop_measure']/parameters['dt'])
    
    average = np.mean(voltage[start_slice: stop_slice])

    amplitude = np.mean(voltage[start_measure:stop_measure]) - average

    return amplitude


def synaptic_amplitude(voltage,parameters):

    start_slice = int(parameters['start_base']/parameters['dt'])

    stop_slice = int(parameters['stop_base']/parameters['dt'])

    start_measure = int(parameters['start_measure']/parameters['dt'])
    
    stop_measure = int(parameters['stop_measure']/parameters['dt'])
    
    average = np.mean(voltage[start_slice: stop_slice])

    amplitude = np.mean(voltage[start_measure:stop_measure]) - average

    return amplitude
