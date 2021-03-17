

'''

Class for adding the expreimental data for the cell model


'''

class experimental:
    
    def __init__(self):
        
        self.experimental_data = dict()
        
    def define_exp(self,**kwargs):
        
        for exp_type, data in kwargs.items():
            
            self.experimental_data.update({exp_type : data})
