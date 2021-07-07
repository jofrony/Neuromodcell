from mpi4py import MPI
from neuron import h
import json
import copy
import numpy as np
from neuromodcell.optimisation_setup import optimisation_setup
from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel
import neuromodcell.selection_criteria as sc
from math import exp
import pathlib

'''

Script which runs the optimisation

The Class will set up the number of models (runs both in serial and parallel)


'''

class Optimise_modulation:

    def __init__(self, setup=None):
        
        self.setup = pathlib.Path(setup)
        self.modulation_setup = None
        self.unit_modulation = {"param_set" : list(), "receptor" : list()}
        self.sim = None
        self.t_save = None
        self.v_save = None
        self.control_v = None
        self.cell_model_pass = dict()
        self.cell_model_voltage_pass = dict()
        self.cell_model_pass_receptor = dict()
        

    def setup_load(self):

        self.modulation_setup = json.load(open(self.setup / 'modulation_setup.json'))

    def set_seed(self,seed=10e5):

        np.random.seed(int(self.pc.id())*int(seed))

    def set_gids(self):

        self.comm = MPI.COMM_WORLD
        self.rank = self.comm.Get_rank()
        self.size = self.comm.Get_size()
  
        pc = h.ParallelContext()
        self.pc = pc
        self.gidlist = []
    
        for i in range(int(pc.id()),self.modulation_setup["population"], int(pc.nhost())):
            self.gidlist.append(i)

    def setup_optimisation(self):

        self.sim = NrnSimulatorParallel(cvode_active=False)
        
        opt = optimisation_setup(self.modulation_setup)
        opt.set_gidlist(self.gidlist)
        opt.start_logging()
        
        if self.rank == 0: 
            opt.setup_neurons(self.unit_modulation)
            opt.control_neuron()

        else:
            opt.setup_neurons(self.unit_modulation)
            
        opt.define_neuromodulation()
        

        opt.instantiate(sim = self.sim)

        self.t_save = opt.time_save()

        self.v_save = opt.voltage_save()

        opt.define_ion_channel()

        opt.define_receptor()
        
        opt.define_protocol()

        opt.run()

    def select(self):


        if self.rank==0:

            self.control_v = self.v_save[-1]
            self.v_save.pop(-1, None)
            
            for i in range(1, self.size):
                self.comm.send(self.control_v, dest=i, tag=i)

        else:
       
            self.control_v  = self.comm.recv(source=0, tag=self.rank)
 
        for trial, voltage in self.v_save.items():

            trial_test = np.zeros(len(self.modulation_setup['selection_criteria']), dtype=bool)
           
            for i, select_method in enumerate(self.modulation_setup['selection_criteria']):
                
                method = getattr(sc,select_method["function"])
                opt_result  = method(criteria = select_method["criteria"], voltages = [np.array(self.control_v),np.array(voltage)])
                trial_test[i] = opt_result['boolean']
            
            if np.all(trial_test):

                for receptor_descr in self.unit_modulation["receptor"][trial]:

                    self.cell_model_pass_receptor[trial] = receptor_descr
                    
                self.cell_model_pass[trial] = self.unit_modulation["param_set"][trial]
                self.cell_model_voltage_pass[trial] = np.array(list(voltage))

    def save_optimisation(self,downsample=1):

        world_model_pass_all = self.comm.gather(self.unit_modulation["param_set"], root=0)
        world_model_voltage_pass_all = self.comm.gather(self.cell_model_voltage_pass, root=0)

        world_voltage = self.comm.gather(self.v_save,root = 0)

        self.pc.barrier()
        
        if self.rank == 0:

            world_model_voltage_pass = list()
            
            for result in world_model_voltage_pass_all:

                for task,pass_volt in result.items():
                    world_model_voltage_pass.append(pass_volt)

            np.savetxt(self.setup / "voltage_modulation_pass.csv",world_model_voltage_pass)

            print('Models passed  ', len(world_model_voltage_pass))

            
            
            world_model_pass = list()

 
            for modulations_all in world_model_pass_all:

                for model in modulations_all:

                    world_model_pass.append(model)

            out_file = open(self.setup / "modulations.json", "w")

            json.dump(world_model_pass, out_file, indent = 6, cls=NumpyEncoder) 
            
            out_file.close()

            

            voltage_saves = list()

            voltage_saves.append(np.array(list(self.t_save))[::downsample])

            for volt in world_voltage:
                for k, volt_recording in volt.items():
                    volt_array = np.array(list(volt_recording))
                    voltage_saves.append(volt_array[::downsample])

            voltage_saves.append(np.array(list(self.control_v))[::downsample])

            np.savetxt(self.setup / "voltages.csv",voltage_saves)


    def export_modulation(self,size):

        
        world_model_pass = self.comm.gather(self.cell_model_pass, root=0)

        if self.rank == 0:

            out_file = open(self.setup / "modulation_pass.json", "w")
            
            modulations_temp = list()
        
            for worker in world_model_pass:
                
                for key, modulation_list in worker.items():

                    temp = list()

                    for mod in modulation_list:

                        if 'maxMod' in mod['param_name']:
                            
                            temp.append(mod)
                    
                    modulations_temp.append(temp)

            json.dump(modulations_temp, out_file, indent = 6)

         

        world_model_pass_receptor = self.comm.gather(self.cell_model_pass_receptor, root=0)


        if self.rank == 0:

            out_rc_file = open(self.setup / "receptor_modulation_pass.json", "w")

            modulations_temp = list()
        
            for worker in world_model_pass_receptor:
                
                for key, modulation_list in worker.items():

                    temp = list()

                    for recep,mod in modulation_list.items():
                        
                            temp.append(mod)
                    
                    modulations_temp.append(temp)

            json.dump(modulations_temp, out_rc_file)


        
    def modulation_list(self):

        for k in self.gidlist:
            temp = copy.deepcopy(self.modulation_setup["ion_channel_modulation"])
        
            for modulation_unit in temp:

                if "maxMod" in modulation_unit["mech_param"]:
                    min_factor = modulation_unit['bounds'][0]
                    max_factor = modulation_unit['bounds'][1]
                    modulation_unit.pop('bounds', None)
                    value = np.random.uniform(min_factor,max_factor, 1)
                    modulation_unit.update({'value' : value[0] })

            temp_receptor = copy.deepcopy(self.modulation_setup["receptor_modulation"])

            self.unit_modulation["param_set"].append(temp)

            for modulation_unit in temp_receptor:

                for synapse_name, syn_params in modulation_unit.items():

                    if "syn_param" != synapse_name:

                        for param in syn_params:

                            min_factor = param['bounds'][0]
                            max_factor = param['bounds'][1]
                            param.pop('bounds', None)
                            value = np.random.uniform(min_factor,max_factor, 1)
                            param.update({'value' : value[0] })

            
            self.unit_modulation["receptor"].append(temp_receptor)
                
class NumpyEncoder(json.JSONEncoder):
	def default(self, obj):

		if isinstance(obj, np.integer):
			return int(obj)
		elif isinstance(obj, np.floating):
			return float(obj)
		elif isinstance(obj, np.ndarray):
			return obj.tolist()
		else:
			return json.JSONEncoder.default(self, obj)
