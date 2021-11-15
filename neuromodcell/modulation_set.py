from pathlib import Path
import json
import numpy as np
import pathlib

'''

Class which sets up the modulation parameters for the neuron models


'''


class DefineModulation:

    def __init__(self, parameterID=None, morph_key=None, parameter_key=None,
                 cell_name=None, output_dir=None, cell_dir=None, population=None,
                 tstop=None, time_step=None):

        self.set_mod = list()
        self.neuromodulation_name = dict()
        self.population = population
        self.protocols = list()
        self.parameter_id = parameterID
        self.morph_key = morph_key
        self.parameter_key = parameter_key
        self.neuromodulation_dir = pathlib.Path(output_dir)
        self.cell_dir = cell_dir
        self.selection_criteria = list()
        self.modulation_function = None
        self.name = cell_name
        self.set_receptor = list()
        self.tstop = tstop
        self.dt = time_step

    def set_time_step(self, dt):

        self.dt = dt

    def cell_name(self, name):

        self.name = name

    def define_neuromodulation(self, **kwargs):

        for key, value in kwargs.items():
            self.neuromodulation_name.update({value: key})

    def define_modulation_function(self, modulation_function, **kwargs):

        if self.tstop is None or self.dt is None:

            print("Define tstop and dt before defining the modulation function")

        else:
            modulation_functions = dict()
            modulation_functions.update({"function": modulation_function})
            for key, value in kwargs.items():
                modulation_functions.update({key: value})
            modulation_functions.update({"tstop": self.tstop})
            modulation_functions.update({"dt": self.dt})

            modulation_functions.update({"time_step_array": np.arange(0, self.tstop, self.dt)})

            self.modulation_function = modulation_functions

    def define_selection_criteria(self, **kwargs):

        criteria = {"parameters": dict(), "selection": dict()}
        function = None

        for key, value in kwargs.items():

            if "function" in key:
                function = value

            elif "mean" in key or "std" in key or "threshold" in key:

                criteria["selection"].update({key: value})

            else:
                criteria["parameters"].update({key: value})

        criteria["parameters"].update({"dt": self.dt})

        self.selection_criteria.append({"function": function, "criteria": criteria})

    def define_protocol(self, **kwargs):

        parameters = dict()
        type_ex = None

        for key, value in kwargs.items():

            if "experiment_type" in key or "typeEx" in key:
                type_ex = value
            else:
                parameters.update({key: value})

        self.protocols.append({"experiment_type": type_ex,
                               "parameters": parameters})

    def define_modulation_receptor(self, syn, neuromod, syn_param, modulation_param):

        name = self.neuromodulation_name[neuromod]

        synaptic_param = {syn: list()}

        for mod_param, bounds in modulation_param.items():
            syn_param_key = mod_param + self.neuromodulation_name[neuromod].replace("modulation", "")
            level_syn_key = "level" + self.neuromodulation_name[neuromod].replace("modulation", "")
            on_syn_key = self.neuromodulation_name[neuromod].replace("ulation", "")

            setmod = {
                "syn": syn,
                "param_name": syn_param_key,
                "level_param": level_syn_key,
                "bounds": bounds,
                "modON": on_syn_key,
                "name": name
            }

            synaptic_param[syn].append(setmod)

        synaptic_param.update({"syn_param": syn_param})

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
            "param_name": f"{mech_param_key}_{mech}",
            "sectionlist": sectionlist,
            "type": "range",
            "bounds": bounds,
            "name": name
        }

        level_param_key = "level" + self.neuromodulation_name[mech_param].replace("modulation", "")
        level = {
            "dist_type": "uniform",
            "mech": mech,
            "mech_param": level_param_key,
            "param_name": f"{level_param_key}_{mech}",
            "sectionlist": sectionlist,
            "type": "range",
            "value": 0,
            "name": name
        }

        on_param_key = self.neuromodulation_name[mech_param].replace("ulation", "")
        on = {
            "dist_type": "uniform",
            "mech": mech,
            "mech_param": on_param_key,
            "param_name": f"{on_param_key}_{mech}",
            "sectionlist": sectionlist,
            "type": "range",
            "value": 0,
            "name": name
        }
        self.set_mod.append(setmod)
        self.set_mod.append(level)
        self.set_mod.append(on)

    def new_modulation_dir(self, directory=None):

        dir_name = None

        if directory is None:
            raise ValueError("directory is not defined")

        for key, value in self.neuromodulation_name.items():

            if self.parameter_key is None and self.morph_key is None:
                pass
            else:
                dir_name = f"{self.parameter_key}_{self.morph_key}"

            if self.parameter_id is None:
                pass
            else:
                dir_name = f"ID_{self.parameter_id}"

            if dir_name is None:
                raise ValueError(f"dir name is not defined, either parameter_id {self.parameter_id} or "
                                 f"morph_key {self.morph_key} and parameter_key {self.parameter_key} cannot be None")

            neuromodulation_dir = Path(directory, key, dir_name)

            if not neuromodulation_dir.exists():
                neuromodulation_dir.mkdir(parents=True, exist_ok=True)

            self.neuromodulation_dir = neuromodulation_dir

    def save_modulation(self, name=None):

        if name is None:
            name = "modulation.json"

        with open(self.neuromodulation_dir / name, "w") as f:
            json.dump(self.set_mod, f)

    def save_modulation_setup(self, name=None):

        if name is None:
            name = "modulation_setup.json"

        define_modulation = dict()

        self.new_modulation_dir(self.neuromodulation_dir)

        for key, value in self.neuromodulation_name.items():
            define_modulation.update({
                "cell_name": self.name,
                "parameter_key": self.parameter_key,
                "morph_key": self.morph_key,
                "parameter_id": self.parameter_id,
                "name": key,
                "key": value,
                "tstop": self.tstop,
                "time_step": self.dt,
                "population": self.population,
                "protocols": self.protocols,
                "model_dir": self.cell_dir,
                "neuromodulation_dir": pathlib.Path(self.neuromodulation_dir),
                "ion_channel_modulation": self.set_mod,
                "receptor_modulation": self.set_receptor,
                "modulation_function": self.modulation_function,
                "selection_criteria": self.selection_criteria
            })

        with open(self.neuromodulation_dir / name, "w") as f:
            json.dump(define_modulation, f, cls=NumpyEncoder)

        self.save_modulation()


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pathlib.PosixPath):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)
