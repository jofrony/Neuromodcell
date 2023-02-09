import os

def compile_mechanisms():

    print("Running nrnivmodl:")
    mech_dir = os.path.join(os.path.dirname(__file__), "mechanisms")

    if not os.path.exists("mechanisms"):
        print("----> Copying mechanisms")
        # os.symlink(mech_dir, "mechanisms")
        from distutils.dir_util import copy_tree
        copy_tree(mech_dir, "mechanisms")
    else:
        print("------------->   !!! mechanisms already exists")

    eval_str = f"nrnivmodl mechanisms"  # f"nrnivmodl {mech_dir}
    print(f"Running: {eval_str}")
    os.system(eval_str)

    # For the unittest we for some reason need to load mechansism separately
    from mpi4py import MPI  # This must be imported before neuron, to run parallel
    from neuron import h  # , gui
    import neuron

    # For some reason we need to import modules manually
    # when running the unit test.
    if os.path.exists("x86_64/.libs/libnrnmech.so"):
        print("!!! Manually loading libraries")
        try:
            h.nrn_load_dll("x86_64/.libs/libnrnmech.so")
        except:
            import traceback
            tstr = traceback.format_exc()
            print(tstr)

    if os.path.exists("aarch64/.libs/libnrnmech.so"):
        print("Manually loading libraries")
        try:
            h.nrn_load_dll("aarch64/.libs/libnrnmech.so")
        except:
            import traceback
            tstr = traceback.format_exc()
            print(tstr)
