from pathlib import Path
import json
import numpy as np
import pathlib

'''

Class which sets up the modulation parameters for the neuron models


'''


class DefineModulation:

    def __init__(self, parameterID: int = None, cell_name: str = None, cell_dir: str = None,
                 output_dir: str = None, population: int = None, tstop: float = None,
                 time_step: float = None) -> None:

        """

        @param parameterID:
        @param cell_name:
        @param cell_dir:
        @param output_dir:
        @param population:
        @param tstop:
        @param time_step:
        @param cellDir:
        """

        if population is None:
            print(f" Set population, currently {population}")
        else:
            self.population = population

        if parameterID is None:
            print(f" Set parameterID, currently {parameterID}")
        else:
            self.parameterID = parameterID

        if cell_dir is None:
            print(f" Set cell_dir, currently {cell_dir}")
        else:
            self.cellDir = cell_dir

        if output_dir is None:
            print(f" Set cell_dir, currently {output_dir}")
        else:
            try:
                self.neuromodulationDir = pathlib.Path(output_dir)
            except:
                raise TypeError(f"output_dir is not type 'str', but {type(output_dir)}")

        if cell_name is None:
            print(f" Set cell_dir, currently {cell_name}")
        else:
            self.name = cell_name

        if tstop is None:
            print(f" Set cell_dir, currently {tstop}")
        else:
            self.tstop = tstop

        if time_step is None:
            print(f" Set cell_dir, currently {time_step}")
        else:
            self.dt = time_step

        self.modulation_function = None
        self.set_mod = list()
        self.neuromodulation_name = dict()
        self.protocols = list()
        self.selection_criteria = list()
        self.set_receptor = list()

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
            modulation_functions.update({'tstop': self.tstop})
            modulation_functions.update({'dt': self.dt})

            modulation_functions.update({'time_step_array': np.arange(0, self.tstop, self.dt)})

        self.modulation_function = modulation_functions

    def define_selection_criteria(self, **kwargs):

        criteria = {'parameters': dict(), 'selection': dict()}
        for key, value in kwargs.items():

            if 'function' in key:
                function = value

            elif 'mean' in key or 'std' in key or 'threshold' in key:

                criteria['selection'].update({key: value})

            else:
                criteria['parameters'].update({key: value})

        criteria['parameters'].update({'dt': self.dt})

        self.selection_criteria.append({"function": function, "criteria": criteria})

    def define_protocol(self, **kwargs):

        parameters = dict()

        for key, value in kwargs.items():

            if 'typeEx' in key:
                typeEx = value
            else:
                parameters.update({key: value})

            # self.neuromodulation_name.update({value: key})

        self.protocols.append({'type': typeEx,
                               'parameters': parameters})

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
            "param_name": mech_param_key + '_' + mech,
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
            "param_name": level_param_key + '_' + mech,
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
            "param_name": on_param_key + '_' + mech,
            "sectionlist": sectionlist,
            "type": "range",
            "value": 0,
            "name": name
        }
        self.set_mod.append(setmod)
        self.set_mod.append(level)
        self.set_mod.append(on)

    def new_modulation_dir(self, directory=None):

        for key, value in self.neuromodulation_name.items():
            parameterID_name = f"ID_{self.parameterID}"

            neuromodulationDir = Path(directory, key, parameterID_name)

            if not neuromodulationDir.exists():
                neuromodulationDir.mkdir(parents=True, exist_ok=True)

            self.neuromodulationDir = neuromodulationDir

    def save_modulation(self, name=None):

        if name is None:
            name = "modulation.json"
        else:
            pass

        with open(self.neuromodulationDir / name, "w") as f:
            json.dump(self.set_mod, f)

    def save_modulation_setup(self, name=None):

        if name is None:
            name = "modulation_setup.json"
        else:
            pass

        define_modulation = dict()

        self.new_modulation_dir(self.neuromodulationDir)

        for key, value in self.neuromodulation_name.items():
            define_modulation.update({
                "name": key,
                "key": value,
                "tstop": self.tstop,
                "ion_channel_modulation": self.set_mod,
                "receptor_modulation": self.set_receptor,
                "population": self.population,
                "protocols": self.protocols,
                "parameterID": self.parameterID,
                "cellDir": self.cellDir,
                "modulation_function": self.modulation_function,
                "selection_criteria": self.selection_criteria,
                "cell_name": self.name
            })

        with open(self.neuromodulationDir / name, "w") as f:
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
