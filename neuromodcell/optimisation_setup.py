import neuromodcell.modulation_functions as mf
from neuromodcell.model_functions import define_mechanisms
from neuromodcell.model_functions import define_parameters
from neuromodcell.model_functions import define_morphology
from neuromodcell.model_functions import define_modulation
from neuromodcell.model_functions import files
from neuromodcell.Neuron_model_extended import NeuronModel
import numpy as np
import json
import logging
import os


'''
Class for setting up the population of neuron models, which will have different modulations

A control model is also added and saved in the last index



'''


class optimisation_setup():

    def __init__(self, modulation_setup):
       
        self.modulation_setup = modulation_setup
        self.cellDir = self.modulation_setup["cellDir"]
        self.neurons = dict()
        self.sim = None
        self.mod_file = None
        self.ion_channels = dict()
        self.modulation_opt_setup = dict()
        self.neuromodulation_name = dict()
        self.t_save = None
        self.v_save =  dict()
        self.gidlist = None
        self.i_stim = list()
        self.receptors = list()
        self.synapses = list()
        self.netcon = list()
        self.unit_modulation = list()

    def set_gidlist(self,gidlist):

        self.gidlist = gidlist

    def start_logging(self):
        
        directory = "logfiles"

        if not os.path.exists(directory):
            os.makedirs(directory)

        logging.basicConfig(filename= "logfiles/log-file-"+str(self.gidlist[0])+".log",level=logging.DEBUG)

    def section_translation(self, section_name):

        translation = {'dend': 'basal', 'somatic': 'soma', 'axon': 'axon'}

        return translation[section_name]

    def define_neuromodulation(self):

        self.neuromodulation_name.update({self.modulation_setup["name"]: self.modulation_setup["key"]})

        self.modulation_type()       

    def setup_neurons(self, unit_modulation):

        self.unit_modulation = unit_modulation
 
        param_file, morph_file, self.mod_file, mech_file = files(self.cellDir)

        param = define_parameters(parameter_config=param_file,parameter_id=self.modulation_setup["parameterID"])
        mech = define_mechanisms(mech_file)
        morph = define_morphology(morph_file=morph_file)

        logging.info('This worker : '+ str(len(self.gidlist)))
      
        for k in range(len(self.gidlist)):

            modulation = define_modulation(param_set=unit_modulation["param_set"][k])

            self.neurons[k] = NeuronModel(cell_name=self.modulation_setup["cell_name"],morph=morph,mech=mech,param=param, modulation=modulation)
    
    def control_neuron(self):

        param_file, morph_file, self.mod_file, mech_file = files(self.cellDir)

        param = define_parameters(parameter_config=param_file,parameter_id=self.modulation_setup["parameterID"])
        mech = define_mechanisms(mech_file)
        morph = define_morphology(morph_file=morph_file)

        self.neurons[-1] = NeuronModel(cell_name=self.modulation_setup["cell_name"],morph=morph,mech=mech,param=param, modulation=[])


    def modulation_type(self):

        name = self.modulation_setup["name"]
        parameters = self.modulation_setup["modulation_function"]
        mod_type = parameters["function"]
        method = getattr(mf, mod_type)

        parameters.update({"ht" :  np.arange(0,parameters["tstop"],parameters["dt"])})

        from neuron import h
        
        vector = h.Vector(method(parameter=parameters))
        
        self.modulation_opt_setup.update({self.neuromodulation_name[name]: {"function": method,
                                                                            "parameters": parameters,
                                                                            "vector" : vector }})

    def instantiate(self, sim):

        self.sim = sim

        for i, cell in self.neurons.items():

            self.neurons[i].instantiate(sim=self.sim)

    def define_ion_channel(self):

        ion_channel_list = list()

        for i, ion_channel_infos in enumerate(self.unit_modulation["param_set"]):

            ion_channel_modulation = dict()

            for param in ion_channel_infos:


                if param["sectionlist"] not in ion_channel_modulation.keys():

                    ion_channel_modulation.update({param["sectionlist"] : list()})
                    ion_channel_modulation[param["sectionlist"]].append(param)

                else:
                    ion_channel_modulation[param["sectionlist"]].append(param)


        for i in range(len(self.unit_modulation["param_set"])):

            for section in ion_channel_modulation.keys():
                for neuron_part in getattr(self.neurons[i].icell,section):
                    for seg in neuron_part:

                        mod_factors = ion_channel_modulation[section]
                        for mod_factor  in mod_factors:

                            if "mod" in mod_factor["mech_param"]:
                                setattr(seg, mod_factor["param_name"],1)

                            if "level" in mod_factor["mech_param"]:
                                dt = self.modulation_setup["modulation_function"]["dt"]
                                                               
                                self.modulation_opt_setup[mod_factor["name"]]['vector'].play(getattr(getattr(seg,mod_factor["mech"]),"_ref_" + mod_factor["mech_param"]),dt)

    def define_receptor(self):
  
        for i, synapse_infos in enumerate(self.unit_modulation["receptor"]):
            for modulation_unit in synapse_infos:
                for synapse_name, modulation_parameters in modulation_unit.items():

                    if "syn_param" != synapse_name:

                        synapse = getattr(self.sim.neuron.h,synapse_name)
                        syn = synapse(self.neurons[i].icell.soma[0](0.5))

                        if "syn_param" in modulation_unit.keys():
                            for syn_parameter, value in modulation_unit["syn_param"].items():
                                setattr(syn,syn_parameter,value)

                        
                        for mod_param in modulation_parameters:

                            setattr(syn,mod_param["param_name"],mod_param["value"])
                            setattr(syn,mod_param["modON"],1)
                            dt = self.modulation_setup["modulation_function"]["dt"]
                            self.modulation_opt_setup[mod_param["name"]]['vector'].play(getattr(syn,"_ref_"+ mod_param["level_param"]),dt)
                       
                        self.receptors.append(syn)

        """
        Check if control neuron is on index -1
        
        """
        if -1 in self.neurons.keys():

            for modulation_unit in self.modulation_setup["receptor_modulation"]:

                for synapse_name, modulation_parameters in modulation_unit.items():

                    if "syn_param" != synapse_name:

                        synapse = getattr(self.sim.neuron.h,synapse_name)
                        syn = synapse(self.neurons[-1].icell.soma[0](0.5))

                        if "syn_param" in modulation_unit.keys():
                            for syn_parameter, value in modulation_unit["syn_param"].items():
                                setattr(syn,syn_parameter,value)
                       
                        self.receptors.append(syn)

        
    def define_protocol(self):

        for i, cell in self.neurons.items():

            for protocol in self.modulation_setup["protocols"]:

                if 'current_clamp' == protocol['type']:
                    cur_stim = self.sim.neuron.h.IClamp(0.5, sec=self.neurons[i].icell.soma[0])
                    cur_stim.delay = protocol['parameters']["start"]
                    cur_stim.dur = protocol['parameters']["duration"]
                    cur_stim.amp =protocol['parameters']["amp"]  
                    self.i_stim.append(cur_stim)

                elif 'synaptic_input' == protocol['type']:
       
                    for syn in self.receptors:

                        if "spiketimes" in protocol['parameters']:
                            VecStim = self.sim.neuron.h.VecStim()
                            spikeTime = self.sim.neuron.h.Vector(protocol["parameters"]["spiketimes"])
                            VecStim.play(spikeTime)

                        ncToSynapse = self.sim.neuron.h.NetCon(VecStim,syn)
                        ncToSynapse.delay= protocol["parameters"]["delay"]
                        ncToSynapse.threshold= protocol["parameters"]["threshold"]
                        ncToSynapse.weight[0]= protocol["parameters"]["conductance"]

                        self.synapses.append(VecStim)
                        self.netcon.append(ncToSynapse)

    def time_save(self):

        self.t_save = self.sim.neuron.h.Vector()
        self.t_save.record(self.sim.neuron.h._ref_t)

        return self.t_save


    def voltage_save(self):

        for i, cell in self.neurons.items():

            v = self.sim.neuron.h.Vector()
            v.record(getattr(cell.icell.soma[0](0.5), '_ref_v'))
            self.v_save[i] = v

        return self.v_save

    def run(self):

        self.sim.neuron.h.tstop = self.modulation_setup["tstop"]
        self.sim.neuron.h.run()


   

        


                

        
        

        
