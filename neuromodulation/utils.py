'''
def create_modulation_parameter_ID():

Combine the results of the optimisation for Snudda simulations

'''
import pathlib
import json
import numpy as np

def combine_neuromodulators(dir_path,neuromodulators = None):

    files_path = pathlib.Path(dir_path)

    temp_dict = dict()
    
    combined_modulation = list()

    for f in files_path.iterdir():
        if f.is_dir() and f.name in neuromodulators:
            for ids in f.iterdir():
                data = json.load(open(ids / 'final_modulation.json'))
                if f.name in temp_dict.keys():
                    temp_dict[f.name].update({ids.name : data})

                else:
                    temp_dict.update({f.name : {ids.name : data}})

    final_dict = dict()

    for name, modulations in temp_dict.items():
        
        for id_name, data_id in modulations.items():
            print(id_name)
            if id_name not in final_dict.keys():
                final_dict.update({id_name : data_id})
            else:
                final_dict[id_name] = final_dict[id_name] + data_id

    temp_list = [*final_dict.values()]

    return temp_list

def save(out_dir):
    
    with open(pathlib.Path(out_dir) / 'modulation.json','w') as f: 
        json.dump(temp_list,f)

        

    
    

    
    
