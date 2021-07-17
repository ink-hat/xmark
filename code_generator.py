from salt_generator import SaltGenerator, SaltGenerator_test

class CodeGenerator():
    _avail_langs = {
        'python'    :  ['_python_reg','_python_salt'],
        'c'         :  ['_c_reg','_c_salt'],
        'c++'       :  ['_cpp_reg','_cpp_salt'],
    }
    
    def __init__(self,lang='python',type='regular'):
        
        if lang in self._avail_langs:
            self.lang = lang
        else:
            raise ValueError('Invalid value for lang; allowed values are: ',self._avail_langs.keys())
        
        if type == 'regular':
            self.type = 0
        elif type == 'salted':
            self.type = 1
        else:
            raise ValueError('Invalid value for type; allowed values are: regular or salted ')
    
    def set_salt_param(self,modulo, ei_limit, ai_limit):
        self.salt_param = [modulo,ei_limit,ai_limit]

    def get_code(self):
        # generating salt
        if 'salt_param' in self.__dict__:
            self.sg = SaltGenerator(*self.salt_param)
        else:
            self.sg = SaltGenerator()

        # running test on generated salt
        sgt = SaltGenerator_test(self.sg)
        sgt.runTest()
        print(self.sg)

        # calling appropriate code generating function
        func_name = self._avail_langs[self.lang][self.type]
        func = getattr(self,func_name)
        return func()
    
    def _python_salt(self):
        x_var = 'x'
        c_var = 'c'
        evalPoly_func = 'evalPoly'

        code = self._python_salt_template
        code = code.replace('modulo_val',str(self.sg.modulo))
        code = code.replace('sInv_val',str(self.sInv_coef))
        code = code.replace('e1_val','evalPoly({},x)'.format(self.sg.e1_coef))
        code = code.replace('e2_val','evalPoly({},x)'.format(self.sg.e2_coef))
        code = code.replace('e3_val','evalPoly({},x)'.format(self.sg.e3_coef))
        code = code.replace('a1_val',str(self.sg.a1))
        code = code.replace('a2_val',str(self.sg.a2))
        code = code.replace('a3_val',str(self.sg.a3))
        code = code.replace('a4_val',str(self.sg.a4))
        code = code.replace('a5_val',str(self.sg.a5))
        code = code.replace('a6_val',str(self.sg.a6))

        # replacing user specified variables or functions
        # 1. x variable
        code = code.replace('x',x_var)
        # 2. c Value
        code = code.replace('c',c_var)
        # 3. evalpoly
        code = code.replace('evalPoly',evalPoly_func)

        return code
    
    def _c_salt(self):
        x_var = 'x'
        c_var = 'c'
        evalPoly_func = 'evalPoly'

        code = self._c_salt_template
        code = code.replace('sInv_val','{{{}}}'.format( ','.join(map(str,self.sg.sInv_coef)) ))
        code = code.replace('e1_val','{{{}}}'.format( ','.join(map(str,self.sg.e1_coef)) ))
        code = code.replace('e2_val','{{{}}}'.format( ','.join(map(str,self.sg.e2_coef)) ))
        code = code.replace('e3_val','{{{}}}'.format( ','.join(map(str,self.sg.e3_coef)) ))
        code = code.replace('s0_val','{{{}}}'.format( ','.join(map(str,self.sg.s0_coef)) ))
        code = code.replace('a1_val',str(self.sg.a1))
        code = code.replace('a2_val',str(self.sg.a2))
        code = code.replace('a3_val',str(self.sg.a3))
        code = code.replace('a4_val',str(self.sg.a4))
        code = code.replace('a5_val',str(self.sg.a5))
        code = code.replace('a6_val',str(self.sg.a6))

        # There is a problem with calculation of s0. s0 calculation
        # has a hidden division by 2. This cause some problem with
        # overflow as division is not preserved in modulo operation.
        # So s0 is calculated using precalculated coefficient.

        # replacing user specified variables or functions
        # 1. x variable
        code = code.replace('x',x_var)
        # 2. c Value
        code = code.replace('c',c_var)
        # 3. evalpoly
        code = code.replace('evalPoly',evalPoly_func)

        return code
    
    # -------------------- code templates --------------------------

    _python_salt_template = """
e1,e2,e3 = e1_val, e2_val, e3_val
s0 = (a4_val*e1 + a5_val*e3)//a6_val
s1 = (a1_val*e1 + a2_val*e2)//a3_val - 1
s = s0 + s1
yr = y
sr = 0
while(evalPoly(sInv_val,yr-x-1) % modulo_val != x):
    yr = yr + e1 - sr
    if yr % 2 == 1:
        yr = (a1_val * yr + a2_val * e2)//a3_val + s0
    else:
        yr = (a4_val * yr + a5_val * e3)//a6_val + s1
    sr = s

    if evalPoly(sInv_val,(yr-c-1)) % modulo_val == x :
        print('\\n....payload block....\\n')
        break

    """

    _c_salt_template = '''
uint16_t e1a[] = e1_val, e2a[] = e2_val, e3a[] = e3_val;
uint16_t e1 = evalPoly(e1a,x), e2 = evalPoly(e2a,x), e3 = evalPoly(e3a,x);
//uint16_t s0 = (a4_val*e1 + a5_val*e3)/a6_val;
uint16_t s0_coef = s0_val;
uint16_t s0 = evalPoly(s0_coef);
uint16_t s1 = (a1_val*e1 + a2_val*e2)/a3_val - 1;
uint16_t s = s0 + s1;
uint16_t sInv[] = sInv_val;
uint16_t yr = y,sr = 0;

while(evalPoly(sInv,yr-x-1) != x)
{
    yr = yr + e1 - sr;
    if( yr % 2 == 1)
        yr = (a1_val * yr + a2_val * e2)/a3_val + s0;
    else
        yr = (a4_val * yr + a5_val * e3)/a6_val + s1;
    sr = s;

    if( evalPoly(sInv,(yr-c-1)) == x )
    {
        printf("\\n....payload block....\\n");
        break;
    }
}

    '''



if __name__ == '__main__':
    cg = CodeGenerator('c','salted')
    cg.set_salt_param(1<<16, 1<<13, 1000)
    code  = cg.get_code()
    print()
    print(code)
        