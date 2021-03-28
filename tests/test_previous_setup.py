from neuromodulation.previous_setup import old_setup
import os
import pathlib

def test_old_setup():

    abs_path =  os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path,'test_data')

    test_setup = old_setup(test_dir_path)

    assert test_setup.return_population() == 200
