'''uses lizard module to calculate halsted complexity

all calculations are done in lizard, here the functions 
only format the result
'''

from lizard import FileAnalyzer,OutputScheme,print_and_save_modules,get_extensions

def calculate(src, functions=False):
    '''returns halsted complexity of a source file

    parameters
    ----------
    src : string
        filepath of the file whose complexity is to be computed
    functions : boolean, default: False
        if true the return value will have individual halsted 
        complexity of each function in the source file.

    return
    ------
    list
        0 : int
            halsted complexity of the source file
        1 : dict of int  (only if functions = True)
            the keys will be in format 'func_name@start_line'
            func_name is the name of function, start_line is the
            line number of function header. The value gives the 
            cyclomatic complexity of the function 
    '''
    file_analyzer = FileAnalyzer(get_extensions([]))
    result = file_analyzer(src)
    func = []
    for fun_result in result.function_list:
        func.append([fun_result.name,fun_result.start_line,fun_result.length])
    ret = [sum(map(lambda x:x[2], func)),]

    if functions:
        ret.append(func)
        
    return ret