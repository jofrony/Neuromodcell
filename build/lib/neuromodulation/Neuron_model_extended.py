""" Based on BluePyOpt exampel code by Werner van Geit, 
modified by Johannes Hjorth """

import os
import json
import numpy as np

import bluepyopt.ephys as ephys


class NeuronModel(ephys.models.CellModel):

    def __init__(self,
                 cell_name="Unknown",
                 morph=None,
                 mech=None,
                 param=None,
                 modulation=None):

        self.name = cell_name
        self.parameters = []

        params = param + modulation

        super(NeuronModel, self).__init__(name=cell_name, morph=morph,
                                          mechs=mech, params=params)
        self.syn_list = []
        self.section_lookup = None

        
    def instantiate(self, sim=None):
        """Instantiate model in simulator"""

        # TODO replace this with the real template name
        if not hasattr(sim.neuron.h, self.name):
            self.icell = self.create_empty_cell(
                self.name,
                sim=sim,
                seclist_names=self.seclist_names,
                secarray_names=self.secarray_names)
        else:
            self.icell = getattr(sim.neuron.h, self.name)()

        self.icell.gid = self.gid

        self.morphology.instantiate(sim=sim, icell=self.icell)

        for mechanism in self.mechanisms:
            mechanism.instantiate(sim=sim, icell=self.icell)
        for param in self.params.values():
            param.instantiate(sim=sim, icell=self.icell)

    ############################################################################
