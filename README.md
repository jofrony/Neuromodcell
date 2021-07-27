

# Neuromodcell

[![Join the chat at https://gitter.im/Neuro_modulation/community](https://badges.gitter.im/Neuro_modulation/community.svg)](https://gitter.im/Neuro_modulation/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

[![codecov](https://codecov.io/gh/jofrony/Neuromodulation/branch/main/graph/badge.svg?token=LKUJ5SC457)](https://codecov.io/gh/jofrony/Neuromodulation)


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







