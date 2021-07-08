from neuromodcell.optimise import OptimiseModulation
import os
import pathlib


def test_optimise():
    abs_path = os.path.dirname(os.path.abspath(__file__))
    test_dir_path = pathlib.Path(abs_path, 'test_data')

    opt = OptimiseModulation(setup=test_dir_path)

    opt.setup_load()
    opt.set_gids()
    opt.set_seed(1234)
    opt.modulation_list()
