from neuromodcell.previous_setup import OldSetup
import os
import pathlib


def test_old_setup():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_data')

    test_setup = OldSetup(test_dir_path)

    assert test_setup.return_population() == 3
