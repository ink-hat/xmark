'''uses lizard module to calculate cyclomatic complexity

all calculations are done in lizard, here the functions 
only format the result
'''

from lizard import FileAnalyzer,OutputScheme,print_and_save_modules,get_extensions

def calculate(src, functions=False):
    '''returns cyclomatic complexity and avg cyclomatic
    complexity of a source file

    parameters
    ----------
    src : string
        filepath of the file whose complexity is to be computed
    functions : boolean, default: False
        if true the return value will have individual cyclomatic 
        complexity of each function in the source file.

    return
    ------
    list
        0 : int
            cyclomatic complexity of the source file
        1 : float
            average cyclomatic complexity of all function
            in the source file
        2 : list of list(3) (only if functions = True)
            the keys will be in format 'func_name@start_line'
            func_name is the name of function, start_line is the
            line number of function header. The value gives the 
            cyclomatic complexity of the function 
    '''
    file_analyzer = FileAnalyzer(get_extensions([]))
    result = file_analyzer(src)
    ret = [result.CCN,result.average_CCN]
    if functions:
        func = []
        for fun_result in result.function_list:
            func.append([fun_result.name,fun_result.start_line,fun_result.cyclomatic_complexity])
        ret.append(func)
    return ret