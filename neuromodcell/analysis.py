import pathlib
import numpy as np
import json
import neuromodcell.modulation_functions as mf
import matplotlib.pyplot as plt


'''
Class for loading the result of the optimisation

functions for analysing the data

'''


class optimisationResult:
    
    def __init__(self,dir_path):
        
        self.voltages = None
        self.model_pass_param = None
        self.model_pass_receptor = None
        self.modulation = None
        self.modulations = None
        self.voltage_modulation_pass = None
        self.dir_path = pathlib.Path(dir_path)
        self.dt = None

    def load(self):
        
        self.voltages = np.loadtxt(self.dir_path / 'voltages.csv')
        self.model_pass_param = json.load(open(self.dir_path / 'modulation_pass.json','rb'))
        self.model_pass_receptor = json.load(open(self.dir_path / 'receptor_modulation_pass.json','rb'))
        self.modulation = json.load(open(self.dir_path / 'modulation.json','rb'))
        self.modulations = json.load(open(self.dir_path / 'modulations.json','rb'))
        self.modulation_setup = json.load(open(self.dir_path / 'modulation_setup.json','rb'))
        self.voltage_modulation_pass = np.loadtxt(self.dir_path /  'voltage_modulation_pass.csv')

        if len(self.voltage_modulation_pass) == 0 or not(isinstance(self.voltage_modulation_pass[0],np.ndarray)):

            self.voltage_modulation_pass = np.array([self.voltage_modulation_pass])

        self.dt = self.voltages[0][1]-self.voltages[0][0]

    def plot_control(self,title=None,filename=None, save=False):

        method = getattr(mf,self.modulation_setup['modulation_function']['function'])
        time_series = method(self.modulation_setup['modulation_function'])

        plt.figure(figsize=(9,3))

        plt.plot(self.voltages[0],self.voltages[-1],label="Control")
        plt.title(title)
        plt.ylabel("membrane potential (mV)")
        plt.xlabel("Time (ms)")
        plt.legend()

        if save:
            plt.savefig(pathlib.Path(self.dir_path) / filename, dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None, metadata=None)
        else:
            plt.show()

    def plot_all_traces(self,title=None,filename=None, save=False):

        method = getattr(mf,self.modulation_setup['modulation_function']['function'])
        time_series = method(self.modulation_setup['modulation_function'])

       
        plt.figure(figsize=(9,3))
        plt.subplot(121)
        
        time = self.voltages[0]
        
        for k in self.voltages[1:]:
            plt.plot(time,k)
   
        plt.title(title)
        plt.ylabel("membrane potential (mV)")
        plt.xlabel("Time (ms)")
        plt.legend()

        plt.subplot(122)
        plt.plot(self.modulation_setup['modulation_function']["time_step_array"],time_series)
        plt.title(title)
        plt.xlabel("Time (ms)")

        if save:
            plt.savefig(pathlib.Path(self.dir_path) / filename, dpi=None, facecolor='w', edgecolor='w',
                        orientation='portrait', papertype=None, format=None,
                        transparent=False, bbox_inches=None, pad_inches=0.1,
                        frameon=None, metadata=None)
        else:
            plt.show()


    

