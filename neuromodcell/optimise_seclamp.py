from neuromodcell.optimise import Optimise_modulation
from neuromodcell.optimise import NumpyEncoder
from neuromodcell.optimisation_setup_seclamp import optimisation_setup_seclamp
from neuromodcell.NrnSimulatorParallel import NrnSimulatorParallel
import numpy as np
import neuromodcell.selection_criteria as sc
import json

class Optimise_modulation_seclamp(Optimise_modulation):


    def __init__(self,setup=None):

        self.c_save = None

        self.cell_model_current_pass = dict()

        super(Optimise_modulation_seclamp,self).__init__(setup=setup)


    def select(self):


        if self.rank==0:

            self.control_c = self.c_save[-1]
            self.c_save.pop(-1, None)
            
            for i in range(1, self.size):
                self.comm.send(self.control_c, dest=i, tag=i)

        else:
       
            self.control_c  = self.comm.recv(source=0, tag=self.rank)
 
        for trial, current in self.c_save.items():

            trial_test = np.zeros(len(self.modulation_setup['selection_criteria']), dtype=bool)
           
            for i, select_method in enumerate(self.modulation_setup['selection_criteria']):
                
                method = getattr(sc,select_method["function"])
                opt_result  = method(criteria = select_method["criteria"], voltages = [np.array(self.control_c),np.array(current)])
                trial_test[i] = opt_result['boolean']
            
            if np.all(trial_test):

                for receptor_descr in self.unit_modulation["receptor"][trial]:

                    self.cell_model_pass_receptor[trial] = receptor_descr
                    
                self.cell_model_pass[trial] = self.unit_modulation["param_set"][trial]
                self.cell_model_current_pass[trial] = np.array(list(current))


    def setup_optimisation(self):

        self.sim = NrnSimulatorParallel(cvode_active=False)
        
        opt = optimisation_setup_seclamp(self.modulation_setup)
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

        self.c_save = opt.current_save()

        opt.define_ion_channel()

        opt.define_receptor()
        
        opt.define_protocol()

        opt.run()


    def save_optimisation(self,downsample=1):

        world_model_pass_all = self.comm.gather(self.cell_model_pass, root=0)

        world_model_current_pass_all = self.comm.gather(self.cell_model_current_pass, root=0)
        world_current = self.comm.gather(self.c_save,root = 0)
        
        

        self.pc.barrier()
        
        if self.rank == 0:

            world_model_current_pass = list()
            
            for result in world_model_current_pass_all:

                for task,pass_current in result.items():
                    world_model_current_pass.append(pass_current)

            np.savetxt(self.setup / "current_modulation_pass.csv",world_model_current_pass)

            print('Models passed  ', len(world_model_current_pass))

            
            world_model_pass = list()
            
            for result in world_model_pass_all:

                for task, model in result.items():

                    world_model_pass.append(model)

            out_file = open(self.setup / "modulation_pass.json", "w")

            json.dump(world_model_pass, out_file, indent = 6, cls=NumpyEncoder) 
            
            out_file.close()

            

            current_saves = list()

            current_saves.append(np.array(list(self.t_save))[::downsample])

            for current in world_current:
                for k, current_recording in current.items():
                    current_array = np.array(list(current_recording))
                    current_saves.append(current_array[::downsample])

            current_saves.append(np.array(list(self.control_c))[::downsample])

            np.savetxt(self.setup / "current.csv",current_saves)


