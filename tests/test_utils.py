from neuromodcell.utils import combine_neuromodulators, save
import os
import pathlib


def test_combine_neuromodulators():

    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(os.path.join(abs_path, 'test_combine'))

    combine_neuromodulators(dir_path=test_dir_path, neuromodulators=["neuromodulatorX", "neuromodulatorY"])


def test_save():
    save(out_dir="", temp_list={})
