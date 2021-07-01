class CodeGenerator():
    _avail_langs = {
        'python'    :  ['_python_reg','_python_salt'],
        'c'         :  ['_c_reg','_c_salt'],
        'c++'       :  ['_cpp_reg','_cpp_salt'],
    }
    
    def __init__(lang='python',type='regular'):
        
        if lang in self._avail_langs:
            self.lang = lang
        else:
            raise ValueError('Invalid value for lang; allowed values are: ',_avail_langs.keys())
        
        if type == 'regular':
            self.type = 0
        elif type == 'salted':
            self.type = 1
        else:
            raise ValueError('Invalid value for type; allowed values are: regular or salted ')
    
    def get_code():
        #self.saltgen = salt_generator()
        pass
        