'''calculate potency from a metric
'''

def calculate(value1,value2):
    '''return potency value for given value

    parameters
    ----------
    value_list : list of number (size 2)
        a list containig 2 numeric values. These numbers 
        are the complexity value of normal and obfuscated
        program of a common metric

    return
    ------
    float
        a number that gives the potency
    '''
    if value2 > 0:
        return value1/value2 - 1
    return 0.0
