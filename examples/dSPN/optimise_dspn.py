from neuromodulation.optimise import Optimise_modulation
import sys
import time

if '-python' in sys.argv:
        print("Network_simulate.py called through nrniv, fixing arguments")
        pythonidx = sys.argv.index('-python')
        if len(sys.argv) > pythonidx:
            sys.argv = sys.argv[pythonidx + 1:]
            

seconds = time.time()

objectives = sys.argv[1]
seed = sys.argv[2]
Opt = Optimise_modulation(setup = objectives)
Opt.setup_load()
Opt.set_gids()
Opt.set_seed(seed)
Opt.modulation_list()
Opt.setup_optimisation()
Opt.select()
Opt.save_optimisation()
Opt.export_modulation(size=10)

print("Seconds =", time.time() - seconds)
