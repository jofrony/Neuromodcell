from pathlib import Path
import json
import numpy as np
import pathlib

'''

Class which sets up the modulation parameters for the neuron models


'''



class defineModulation:

    def __init__(self,parameterID,population_size=None,cellDir=None):

        self.set_mod = list()
        self.neuromodulation_name = dict()
        self.population = population_size
        self.protocols = list()
        self.parameterID = parameterID
        self.neuromodulationDir = None
        self.cellDir = cellDir
        self.selection_criteria = list()
        self.modulation_function = None
        self.name = None
        self.set_receptor = list()
        self.tstop = None
        self.dt = None

    def set_time_step(self,dt):

        self.dt = dt

    def cell_name(self,name):

        self.name = name
        
    def define_neuromodulation(self, **kwargs):

        for key, value in kwargs.items():
            self.neuromodulation_name.update({value: key})

    def define_modulation_function(self, modulation_function):

        if self.tstop is None or self.dt is None:

            print("Define tstop and dt before defining the modulation function")

        else:

            modulation_function.update({'tstop' : self.tstop})
            modulation_function.update({'dt' : self.dt})

            modulation_function.update({'time_step_array' : np.arange(0,self.tstop,self.dt)})

        self.modulation_function = modulation_function
  
    def define_selection_criteria(self,function,criteria):

        criteria['parameters'].update({'dt' : self.dt})

        self.selection_criteria.append({ "function" : function, "criteria" : criteria})

    def define_protocol(self, typeEx, parameters):

        self.protocols.append({'type': typeEx,
                                   'parameters': parameters})

    def define_modulation_receptor(self, syn, neuromod, syn_param, modulation_param):

        name = self.neuromodulation_name[neuromod]

        synaptic_param = {syn : list()}

        for mod_param, bounds in modulation_param.items():

            syn_param_key = mod_param + self.neuromodulation_name[neuromod].replace("modulation", "")
            level_syn_key = "level" + self.neuromodulation_name[neuromod].replace("modulation", "")
            on_syn_key = self.neuromodulation_name[neuromod].replace("ulation", "")
            
            setmod = {
                "syn": syn,
                "param_name": syn_param_key,
                "level_param": level_syn_key,
                "bounds": bounds,
                "modON" : on_syn_key,
                "name" : name
            }

            synaptic_param[syn].append(setmod)

        synaptic_param.update({"syn_param" : syn_param})



        self.set_receptor.append(synaptic_param)

    def define_modulation_parameter(self, mech, mech_param, sectionlist, bounds=None):
        name = self.neuromodulation_name[mech_param]
    
        if bounds is None:
            bounds = []
        mech_param_key = self.neuromodulation_name[mech_param].replace("ulation", "").replace("m", "maxM")
        setmod = {
            "dist_type": "uniform",
            "mech": mech,
            "mech_param": mech_param_key,
            "param_name": mech_param_key + '_' + mech,
            "sectionlist": sectionlist,
            "type": "range",
            "bounds": bounds,
            "name" : name
        }

        level_param_key = "level" + self.neuromodulation_name[mech_param].replace("modulation", "")
        level = {
            "dist_type": "uniform",
            "mech": mech,
            "mech_param": level_param_key,
            "param_name": level_param_key + '_' + mech,
            "sectionlist": sectionlist,
            "type": "range",
            "value": 0,
            "name" : name
        }

        on_param_key = self.neuromodulation_name[mech_param].replace("ulation", "")
        on = {
            "dist_type": "uniform",
            "mech": mech,
            "mech_param": on_param_key,
            "param_name": on_param_key + '_' + mech,
            "sectionlist": sectionlist,
            "type": "range",
            "value": 0,
            "name" : name
        }
        self.set_mod.append(setmod)
        self.set_mod.append(level)
        self.set_mod.append(on)

    def new_modulation_dir(self, directory=''):

        for key, value in self.neuromodulation_name.items():
            parameterID_name = 'ID_' + str(self.parameterID)

            neuromodulationDir = Path(directory,key,parameterID_name)
            
            if not neuromodulationDir.exists():
                neuromodulationDir.mkdir(parents=True, exist_ok=True)

            self.neuromodulationDir = neuromodulationDir


    def save_modulation(self, name = 'modulation.json'):

        with open(self.neuromodulationDir / name, 'w') as f:
            json.dump(self.set_mod, f)

        
    def save_modulation_setup(self, name='modulation_setup.json'):      

        define_modulation = dict()

        for key, value in self.neuromodulation_name.items():
            define_modulation.update({
                "name": key,
                "key" : value,
                "tstop": self.tstop,
                "ion_channel_modulation": self.set_mod,
                "receptor_modulation" : self.set_receptor,
                "population": self.population,
                "protocols": self.protocols,
                "parameterID": self.parameterID,
                "cellDir": self.cellDir,
                "modulation_function" : self.modulation_function,
                "selection_criteria" : self.selection_criteria,
                "cell_name" : self.name
            })
       
        with open(self.neuromodulationDir / name, 'w') as f:
            json.dump(define_modulation, f, cls=NumpyEncoder)

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj,pathlib.PosixPath):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
