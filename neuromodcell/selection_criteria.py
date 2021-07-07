import neuromodcell.selection_functions as sf
import numpy as np

'''
Functions which are used to select the models which pass the criteria

New functions can be added, the function should accept criteria, voltages and shoudl return a dictionary, 
which contain at least boolean key, which returns True or False pass for the criteria



'''

def number_AP_decrease(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.number_action_potentials(voltages[0],parameters)
                        
    modulated = sf.number_action_potentials(voltages[1],parameters)
    
    zscore = abs(selection["mean"] - abs(modulated - control))/selection["std"]

    diff = modulated - control

    boolean = zscore < threshold and diff < 0

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlAP" : control, "modulatedAP" : modulated}
 
    return result

def number_AP_increase(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.number_action_potentials(voltages[0],parameters)
                        
    modulated = sf.number_action_potentials(voltages[1],parameters)
    
    zscore = abs(selection["mean"] - abs(modulated - control))/selection["std"]

    diff = modulated - control

    boolean = zscore < threshold and diff > 0

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlAP" : control, "modulatedAP" : modulated}
 
    return result

def frequency_change(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.mean_frequency(voltages[0],parameters)
                        
    modulated = sf.mean_frequency(voltages[1],parameters)
    
    zscore = abs(selection["mean"] - abs(modulated.take(0) - control.take(0)))/selection["std"]

    boolean = zscore < threshold

    diff = modulated.take(0) - control.take(0)

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlHz" : control, "modulatedHz" : modulated}
 
    return result

def frequency_change_increase(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.mean_frequency(voltages[0],parameters)
                        
    modulated = sf.mean_frequency(voltages[1],parameters)
    
    zscore = abs(selection["mean"] - abs(modulated.take(0) - control.take(0)))/selection["std"]

    diff = modulated.take(0) - control.take(0)

    boolean = zscore < threshold and diff > 0 

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlHz" : control, "modulatedHz" : modulated}
 
    return result

def frequency_change_decrease(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.mean_frequency(voltages[0],parameters)
                        
    modulated = sf.mean_frequency(voltages[1],parameters)
    
    zscore = abs(selection["mean"] - abs(modulated.take(0) - control.take(0)))/selection["std"]

    diff = modulated.take(0) - control.take(0)

    boolean = zscore < threshold and diff < 0 

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlHz" : control, "modulatedHz" : modulated}
 
    return result


def cv_change(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.cv(voltages[0],parameters)
                        
    modulated = sf.cv(voltages[1],parameters)

    zscore = abs(selection["mean"] - abs(control.take(0) - modulated.take(0)))/selection["std"]

    diff = modulated.take(0) - control.take(0)

    boolean = zscore < threshold

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlcv" : control, "modulatedcv" : modulated}
    
    return  result


def membrane_amplitude_increase(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.membrane_amplitude(voltages[0],parameters)
                        
    modulated = sf.membrane_amplitude(voltages[1],parameters)

    zscore = abs(selection["mean"] - abs(control.take(0) - modulated.take(0)))/selection["std"]

    diff = modulated.take(0) - control.take(0)

    boolean = zscore < threshold and diff > 0

    result = { "boolean" : boolean, "zscore" : zscore, "diff" : diff, "controlcv" : control, "modulatedcv" : modulated}
    
    return  result

def membrane_amplitude_increase_percentage(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.membrane_amplitude(voltages[0],parameters)
                        
    modulated = sf.membrane_amplitude(voltages[1],parameters)

    percentage = ((modulated.take(0) -control.take(0))/control.take(0))*100 + 100

    zscore = abs(selection["mean"] - abs(percentage))/selection["std"]

    boolean = zscore < threshold and percentage > 100

    result = { "boolean" : boolean, "zscore" : zscore, "percentage" : percentage, "controlcv" : control, "modulatedcv" : modulated}

    return  result


def membrane_amplitude_decrease_percentage(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.membrane_amplitude(voltages[0],parameters)
                        
    modulated = sf.membrane_amplitude(voltages[1],parameters)

    percentage = ((modulated.take(0) -control.take(0))/control.take(0))*100 + 100

    zscore = abs(selection["mean"] - abs(percentage))/selection["std"]

    boolean = zscore < threshold and percentage < 100

    result = { "boolean" : boolean, "zscore" : zscore, "percentage" : percentage, "controlcv" : control, "modulatedcv" : modulated}

    return  result

def synaptic_amplitude_decrease_percentage(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.synaptic_amplitude(voltages[0],parameters)
                        
    modulated = sf.synaptic_amplitude(voltages[1],parameters)

    percentage = ((modulated.take(0) -control.take(0))/control.take(0))*100 + 100

    zscore = abs(selection["mean"] - abs(percentage))/selection["std"]

    boolean = zscore < threshold and percentage < 100

    result = { "boolean" : boolean, "zscore" : zscore, "percentage" : percentage, "controlcv" : control, "modulatedcv" : modulated}

    return  result


