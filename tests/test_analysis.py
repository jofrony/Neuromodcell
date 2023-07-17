from neuromodcell.analysis import OptimisationResult
import os
import pathlib


def test_analysis():

    abs_path = os.path.dirname(os.path.abspath(__file__))

    test_dir_path = pathlib.Path(os.path.join(abs_path, "test_result"))

    test_dl = OptimisationResult(test_dir_path)
    test_dl.load()

    import numpy as np

    test_dl.voltage_modulation_pass = np.array([])

    test_dl.plot_control(title='test', filename='test.pdf', save=True)

    test_dl.plot_all_traces(title='test', filename='test.pdf', save=True)

if __name__ == '__main__':
    test_analysis()
