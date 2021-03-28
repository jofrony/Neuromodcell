'''
def create_modulation_parameter_ID():

Combine the results of the optimisation for Snudda simulations

'''
import pathlib
import json
import numpy as np

def combine_neuromodulators(dir_path,ID,neuromodulators = None):

    files_path = pathlib.Path(dir_path)

    temp_dict = dict()
    
    combined_modulation = list()

    for f in files_path.iterdir():
        if f.is_dir():
            f_ID  = pathlib.Path(f,'ID_' + str(ID))
            data = json.load(open(f_ID / 'modulations.json'))
            temp_dict.update({f_ID.name : data})
            size = len(data)

    final_dict = {"combined" : list()}

    for i in range(size):
        final_dict['combined'].append(list())

    for name, modulations in temp_dict.items():
            for mod_i in range(len(modulations)):
                final_dict["combined"][mod_i] = final_dict["combined"][mod_i] + modulations[mod_i]

    json.dump(final_dict["combined"],open(f.parent / 'modulation.json','w'))

        

    
    

    
    
