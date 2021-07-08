from neuromodcell.analysis import OptimisationResult
import os
import pathlib


def test_analysis():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_result')

    testdl = OptimisationResult(test_dir_path)
    testdl.load()

    testdl.plot_control(title='test', filename='test.pdf', save=True)

    testdl.plot_all_traces(title='test', filename='test.pdf', save=True)
