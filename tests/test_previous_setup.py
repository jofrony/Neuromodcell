from neuromodulation.previous_setup import old_setup


def test_old_setup():

    dirpath = 'tests/test_data'

    test_setup = old_setup(dirpath)

    assert test_setup.return_population() == 200
