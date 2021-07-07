from neuromodcell.optimisation_setup import optimisation_setup


class optimisation_setup_seclamp(optimisation_setup):


    def __init__(self, modulation_setup):


        self.seclamp = list()
        self.c_save = dict()

        super(optimisation_setup_seclamp,self).__init__(modulation_setup=modulation_setup)
        


    def current_save(self):

        for i, cell in self.neurons.items():

            seclamp = self.sim.neuron.h.SEClamp(cell.icell.soma[0](0.5))
            seclamp.rs = 1e-6
            seclamp.dur1 = self.modulation_setup["tstop"]
            seclamp.amp1 = -63

            c = self.sim.neuron.h.Vector()
            c.record(seclamp._ref_i)
            self.c_save[i] = c
            self.seclamp.append(seclamp)

        return self.c_save
        

        

    


         
