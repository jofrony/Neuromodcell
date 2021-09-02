import pathlib
import json


def combine_neuromodulators(dir_path, neuromodulators=None):
    files_path = pathlib.Path(dir_path)

    temp_dict = dict()

    for f in files_path.iterdir():

        if f.is_dir() and f.name in neuromodulators:
            for ids in f.iterdir():
                final_modulation = ids / 'final_modulation.json'

                if final_modulation.is_file():
                    data = json.load(open(final_modulation))
                else:
                    print('Skipping folder',dir_path.name, f.name, 'ID' , ids.name)
                    data = []
                if f.name in temp_dict.keys():
                    temp_dict[f.name].update({ids.name: data})

                else:
                    temp_dict.update({f.name: {ids.name: data}})

    final_dict = dict()

    for name, modulations in temp_dict.items():

        for id_name, data_id in modulations.items():
         
            if id_name not in final_dict.keys():
                final_dict.update({id_name: data_id})
            else:
                final_dict[id_name] = final_dict[id_name] + data_id


    num_parameter_sets = len([*final_dict.values()])
    temp_list = list()
    
    for i in range(num_parameter_sets):

        temp_list.append(final_dict['ID_' + str(i)])

    return temp_list


def save(out_dir, temp_list):
    
    with open(pathlib.Path(out_dir) / 'modulation.json', 'w') as f:
        json.dump(temp_list, f)
