import neuromodcell.selection_criteria as sc
import neuromodcell.selection_functions as sf
from neuromodcell.analysis import OptimisationResult
import numpy as np
from neuromodcell.plotting import plot_comparison
import matplotlib.pyplot as plt
import pathlib
import os
import json
from neuromodcell.modulation_set import NumpyEncoder

class dSPNanalysis(OptimisationResult):
    
    def __init__(self,dir_path):

        self.num_AP_control_muscarinic = list()

        self.num_AP_passing_traces_muscarinic = list()

        self.num_AP_all_traces_muscarinic = list()

        self.num_AP_result_muscarinic = list()

        self.num_AP_passing_analysis_traces_muscarinic = list()

        

        self.num_AP_control_dopamine = list()

        self.num_AP_passing_traces_dopamine = list()

        self.num_AP_all_traces_dopamine = list()

        self.num_AP_result_dopamine = list()

        self.num_AP_passing_analysis_traces_dopamine = list()

        
        
        super(dSPNanalysis,self).__init__(dir_path=dir_path)

    def muscarinic_analysis(self):

        criteria = self.modulation_setup['selection_criteria'][0]['criteria']

        self.num_AP_control_muscarinic.append(sf.number_action_potentials(self.voltages[-1],criteria['parameters']))


        for volt in self.voltage_modulation_pass:

            self.num_AP_passing_traces_muscarinic.append(sf.number_action_potentials(volt,criteria['parameters']))

        for volt in self.voltages[1:-1]:

            self.num_AP_all_traces_muscarinic.append(sf.number_action_potentials(volt,criteria['parameters']))

        num_AP_results_muscarinic = list()
        
        for volt in self.voltages[1:-1]:
            
            result = sc.number_AP_increase(criteria,[self.voltages[-1],volt])

            self.num_AP_result_muscarinic.append(result)

            num_AP_results_muscarinic.append([result['zscore'], result['diff']])

        index = np.where((np.transpose(num_AP_results_muscarinic)[0] < criteria['selection']['threshold']) & (np.transpose(num_AP_results_muscarinic)[1] > 0))
            
        num_AP_passing_analysis = np.take(np.array(self.voltages[1:-1]),index,axis=0)[0]

        for volt_pass in num_AP_passing_analysis:

            self.num_AP_passing_analysis_traces_muscarinic.append(sf.number_action_potentials(volt_pass,criteria['parameters']))

    def get_muscarinic_control(self):

        return self.num_AP_control_muscarinic

    def get_criteria(self):

        return self.modulation_setup['selection_criteria'][0]['criteria']['selection']

    def dopamine_analysis(self):

        criteria = self.modulation_setup['selection_criteria'][0]['criteria']

        self.num_AP_control_dopamine.append(sf.number_action_potentials(self.voltages[-1],criteria['parameters']))


        for volt in self.voltage_modulation_pass:

            self.num_AP_passing_traces_dopamine.append(sf.number_action_potentials(volt,criteria['parameters']))

        for volt in self.voltages[1:-1]:

            self.num_AP_all_traces_dopamine.append(sf.number_action_potentials(volt,criteria['parameters']))

        num_AP_results_dopamine = list()
        
        for volt in self.voltages[1:-1]:
            
            result = sc.number_AP_increase(criteria,[self.voltages[-1],volt])

            self.num_AP_result_dopamine.append(result)

            num_AP_results_dopamine.append([result['zscore'], result['diff']])

        index = np.where((np.transpose(num_AP_results_dopamine)[0] < criteria['selection']['threshold']) & (np.transpose(num_AP_results_dopamine)[1] > 0))
            
        num_AP_passing_analysis = np.take(np.array(self.voltages[1:-1]),index,axis=0)[0]

        for volt_pass in num_AP_passing_analysis:

            self.num_AP_passing_analysis_traces_dopamine.append(sf.number_action_potentials(volt_pass,criteria['parameters']))

    def get_dopamine_control(self):

        return self.num_AP_control_dopamine
        
    def save_selected_modulation(self):

        criteria = self.modulation_setup['selection_criteria'][0]['criteria']
        AP_result = list()
        
        for volt in self.voltages[1:-1]:
            
            result = sc.number_AP_increase(criteria,[self.voltages[-1],volt])

            AP_result.append([result['zscore'], result['diff']])

        index_original = np.where((np.transpose(AP_result)[0] < criteria['selection']['threshold']) & (np.transpose(AP_result)[1] > 0))

        results_pass = np.take(AP_result,index_original,axis=0)[0]

        modulations_sub = np.take(self.modulations,index_original,axis=0)[0]

        voltage_sub = np.take(self.voltages[1:-1],index_original,axis=0)[0]

        index = np.where(np.transpose(results_pass)[0] ==  min(np.transpose(results_pass)[0]))

        if len(index[0])>1:
            import random
            index = random.choice(index[0])
        else:
            index = index[0][0]
 
        chosen = modulations_sub[index]

        self.final_modulation_result  = results_pass[index]
        self.final_modulation_voltage = voltage_sub[index]

        with open(pathlib.Path(os.path.abspath(self.dir_path)) / 'final_modulation.json','w') as f:
            json.dump(chosen,f,cls=NumpyEncoder)

    def get_final_modulation(self):

        return self.final_modulation_result, self.final_modulation_voltage
        
    def plot_comparison(self,control,control_sim,modulated,modulated_sim, num_models,ylabel,title,x_ticks=tuple(),width=None,height=None,parameterID=None,save=False,filename=None):

        plot_comparison(control=control,control_sim=control_sim,modulated=modulated,modulated_sim=modulated_sim, num_models=num_models,ylabel=ylabel,width=width,height=height,title=title,x_ticks=x_ticks,dir_path=self.dir_path,save=save,filename=filename)

    def plot_chosen_modulation(self):

        modulation, voltage = self.get_final_modulation()

        plt.plot(self.voltages[0],voltage, label='chosen')
        plt.plot(self.voltages[0],self.voltages[-1],label='control',c='black')
        plt.show()
        

    def plot_validated_traces_with_control(self,titles=None,filename=None, save=False,skip=50,plot_protocols=True,resting_tick=True):

        if plot_protocols:
            fig, axs = plt.subplots(2, 1, sharex=True, sharey=False,gridspec_kw={'height_ratios': [3, 1]})
        else:
            fig, axs = plt.subplots(1, 1, sharex=True, sharey=False)


        time = self.voltages[0]

        #if len(self.voltage_modulation_pass) == 0 or not(isinstance(self.voltage_modulation_pass[0],np.ndarray)):
        #     self.voltage_modulation_pass = np.array([self.voltage_modulation_pass])

        if not(len(self.voltage_modulation_pass[0]) == 0):
            for voltage in self.voltage_modulation_pass:
                axs[0].plot(time[int(skip/self.dt):],voltage[int(skip/self.dt):])
        else:
            print(' No passing models')

        if resting_tick:
            resting = np.mean(self.voltages[-1][int(50/self.dt):int(100/self.dt)])
            axs[0].plot(np.arange(25),np.ones_like(np.arange(25))*resting,c='red')
            axs[0].plot(800*np.ones_like(np.arange(-20,0)),np.arange(-20,0),c='black')
            axs[0].text(825,-12,'20 mV')
            axs[0].plot(np.arange(800,1000),np.ones_like(np.arange(800,1000))*-75,c='black')
            axs[0].text(850,-70,'200 ms')

        axs[0].plot(self.voltages[0][int(50/self.dt):],self.voltages[-1][int(50/self.dt):],label="Control",c='black')
        axs[0].set_title(titles)
        axs[0].set_ylabel("membrane potential (mV)")
        axs[0].set_xlabel("Time (ms)")
        axs[0].legend()

        if plot_protocols:

            base = np.zeros_like(self.voltages[0])

            for protocol in self.modulation_setup['protocols']:

                addition = np.zeros_like(self.voltages[0])
                addition[int(protocol['parameters']['start']/self.dt):int((protocol['parameters']['start']+protocol['parameters']['duration'])/self.dt)] = addition[int(protocol['parameters']['start']/self.dt):int((protocol['parameters']['start']+protocol['parameters']['duration'])/self.dt)] + protocol['parameters']['amp']*1e3 
                d = np.add(base,addition)
            axs[1].plot(time[int(skip/self.dt):],d[int(skip/self.dt):],c='black')
            axs[1].set_ylabel('current (pA)')
            axs[1].set_xlabel("Time (ms)")
            axs[1].plot(np.arange(800,1000),np.ones_like(np.arange(800,1000))*100,c='black')
            axs[1].text(850,150,'200 ms')
            axs[1].plot(800*np.ones_like(np.arange(150,550)),np.arange(150,550),c='black')
            axs[1].text(825,325,'400 pA')

        if save:
            plt.savefig(pathlib.Path(self.dir_path) / filename, dpi=300)
        else:
            plt.show()

        
