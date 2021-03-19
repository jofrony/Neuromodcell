import neuromodulation.selection_criteria as sc
import neuromodulation.selection_functions as sf
from neuromodulation.analysis import optimisationResult
import numpy as np
from neuromodulation.plotting import plot_comparison


class dSPNanalysis(optimisationResult):
    
    def __init__(self,dir_path):
        
        self.zscore_values = list()
        self.frequency = list()
        self.frequency_control = list()
        self.passing = list()
        self.num_AP_list = list()
        self.num_AP_control = list()
        
        super(dSPNanalysis,self).__init__(dir_path=dir_path)
        
    def num_ap_analysis_control(self,criteria):
        
        criteria.update({'dt' : self.dt})
        
        self.num_AP_list_control = list()

        self.num_AP_list_control.append(sf.number_action_potentials(self.voltages[-1],criteria))
        
    def num_ap_analysis(self,criteria):
        
        criteria.update({'dt' : self.dt})
        
        self.num_AP_list = list()
        
        for volt in self.voltages[1:-1]:
            
            self.num_AP_list.append(sf.number_action_potentials(volt,criteria))
        
    def zscore_analysis(self,criteria):

        criteria['parameters'].update({'dt' : self.dt})
        
        self.zscore_values = list()
        
        for volt in self.voltages[1:-1]:

            result = sc.frequency_change(criteria,[self.voltages[-1],volt])
        
            self.zscore_values.append([result['zscore'], result['diff']])
            
        index = np.where((np.transpose(self.zscore_values)[1] > 0) & (np.transpose(self.zscore_values)[0] < criteria['selection']['threshold']))
        self.passing = np.take(np.array(self.voltages[1:]),index,axis=0)[0]

    def frequency_analysis(self,criteria):

        criteria.update({'dt' : self.dt})
        
        self.frequency = list()
        
        for volt in self.passing:

            self.frequency.append(sf.mean_frequency(volt,criteria))
            
    def frequency_analysis_all(self,criteria):

        criteria.update({'dt' : self.dt})
         
        self.frequency_all = list()
        
        for volt in self.voltages[1:-1]:

            self.frequency_all.append(sf.mean_frequency(volt,criteria))
            
    def frequency_analysis_control(self,criteria):
        
        self.frequency_control = list()
        
        self.frequency_control.append(sf.mean_frequency(self.voltages[-1],criteria))

    def plot_comparison(self,control,control_sim,modulated,modulated_sim, num_models,ylabel,title,x_ticks=tuple(),parameterID=None,save=False,filename=None):

        plot_comparison(control=control,control_sim=control_sim,modulated=modulated,modulated_sim=modulated_sim, num_models=num_models,ylabel=ylabel,title=title,x_ticks=x_ticks,dir_path=self.dir_path,save=save,filename=filename)
        
        
