from neuromodcell.plotting import plot_comparison
from neuromodcell.analysis import OptimisationResult
from neuromodcell.experimental_data import Experimental
import os
import pathlib
def test_plot_comparison():

    import numpy as np

    abs_path = os.path.dirname(os.path.abspath(__file__))

    test_dir_path = pathlib.Path(os.path.join(abs_path, "test_result"))

    test_dl = OptimisationResult(test_dir_path)

    test_dl.load()


    test_exp = Experimental()
    test_exp.define_exp(control={"mean": 3.566, "std": 0.88})
    test_exp.define_exp(modulated={"mean": 3.566 + test_dl.modulation_setup['selection_criteria'][0]['criteria']['selection']['mean'],
                                         "std": test_dl.modulation_setup['selection_criteria'][0]['criteria']['selection']['std'] * 1.5})

    test_exp.define_exp(control_sim=[[8], [8]])
    test_exp.define_exp(modulated_sim=[[10], [10]])
    plot_comparison(test_exp.experimental_data['control'], test_exp.experimental_data['control_sim'],
                       test_exp.experimental_data['modulated'], test_exp.experimental_data['modulated_sim'],
                       x_ticks=['Model 1'], ylabel='Number of APs', title='Dopamine modulation', num_models=1,
                       save=True, dir_path="",
                       filename='model_1.pdf', width=3, height=5)

if __name__ == '__main__':

    test_plot_comparison()
