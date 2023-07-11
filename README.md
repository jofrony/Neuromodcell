

# Neuromodcell

[![Join the chat at https://gitter.im/Neuro_modulation/community](https://badges.gitter.im/Neuro_modulation/community.svg)](https://gitter.im/Neuromodcell/community)

Optimizing neuromodulation in multicompartmental neuron model.

### Tutorial for setting up neuromodulation for single cell models

See examples/ for Jupyter Notebook on dSPN optimization and analysis


# Install

To use Neuromodcell, you first have to install [NEURON](https://www.neuron.yale.edu/neuron/download) on your machine , then install Neuromodcell via

```
pip install neuromodcell

```

# Models

The multicompartmental models should have morphology file (SWC), mechanisms.json (JSON) and parameters.json (JSON) files. See examples/models/dspn for examples of dSPN multicompartmental models. 

# Testing

Uses pytest. To execute, run:

```
pytest tests/
```

REMOVE: complied mechanisms (eg. x86_64/-folder, depends on CPU architecture) before running tests again!

# Support

We provide support via gitter chat or github issues page

# Requirements
<ul>
<li>neuron</li>
<li>elephant</li>
<li>bluepyopt</li>
<li>deepdif</li>
<li>matplotlib</li>
</ul>


# Citation
Frost Nylen J, Hjorth J J J,Grillner S, and Hellgren Kotaleski J, Dopaminergic and Cholinergic Modulation of Large Scale Networks in silico Using Snudda, Frontiers in Neural Circuits, vol. 15, Oct. 2021.

# Funding
Horizon 2020 Framework Programme (785907, HBP SGA2); Horizon 2020 Framework Programme (945539, HBP SGA3); Vetenskapsrådet (VR-M-2017-02806, VR-M-2020-01652); Swedish e-science Research Center (SeRC); KTH Digital Futures. The computations are enabled by resources provided by the Swedish National Infrastructure for Computing (SNIC) at PDC KTH partially funded by the Swedish Research Council through grant agreement no. 2018-05973. We acknowledge the use of Fenix Infrastructure resources, which are partially funded from the European Union's Horizon 2020 research and innovation programme through the ICEI project under the grant agreement No. 800858.

# Usage


https://doi.org/10.3389/fncir.2021.748989







