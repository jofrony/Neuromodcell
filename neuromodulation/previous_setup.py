import pathlib
import json

class old_setup:


    def __init__(self,dir_path):

        self.previous_setup = json.load(open(pathlib.Path(dir_path) / 'modulation_setup.json', 'rb'))


    def return_population(self):

        pop_num = self.previous_setup['population']

        return pop_num
