import neuromodulation.selection_functions as sf
import numpy as np

'''
Functions which are used to select the models which pass the criteria

New functions can be added, the function should accept criteria, voltages and shoudl return a dictionary, 
which contain at least boolean key, which returns True or False pass for the criteria



'''

def number_AP_increase(criteria,voltages):

    parameters = criteria["parameters"]

    selection = criteria["selection"]

    threshold = criteria["selection"]["threshold"]
    
    control = sf.number_action_potentials(voltages[0],parameters)
                        
    modulated = sf.number_action_potentials(voltages[1],parameters)
    
    zscore = abs(selection["mean"] - abs(modulated.take(0) - control.take(0)))/selection["std"]

    diff = modulated.take(0) - control.take(0)

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
    
    control = sf.cv(voltages[0],parameters["dt"])
                        
    modulated = sf.cv(voltages[1],parameters["dt"])

    zcore = abs(selection["mean"] - (control.take(0) - modulated.take(0)))/selection["std"]

    boolean = (zcore < selection["threshold"]) > 0 

    result = { "boolean" : boolean}
    
    return  result


