import random
import math 
import re

class SaltGenerator:
    def __init__(self,modulo = 64,eil = 100, ail = 60):
        '''
        parameters
        ----------
        modulo : int
            an integer of form 2^n.
        eil : int
            upper limit for coeficients of ei polynomial. 
            It should be grater than 2 * square root of modulo,
            otherwise an exception is raised.
        ail : int
            upper limit for choosing values for a1 to a6.
            larger numbers give more randomness. It can have a
            minimum value of 3, but this will not produce
            any randomness.
        '''

        self.ei_upperLimit = eil	# max value for salt poly coefficient (depends on modulo)
        self.ai_upperLimit = ail  	# max value for ai
        self.modulo = modulo		# should be a 2^n number

        self.calcSaltPolynomials()
        self.calcAiCoefficients()
        self.calcSCoefficients()
        self.calcSInverseCoefficients()

        #self.applyModuloToAll()

    def applyModuloToAll(self):
        self.e1 %= self.modulo
        self.e2 %= self.modulo
        self.e3 %= self.modulo

        self.s0 %= self.modulo
        self.s1 %= self.modulo
        self.s %= self.modulo

        self.sInv_coef = [ (coef % self.modulo) for coef in self.sInv_coef]


    def calcSaltPolynomials(self):
        '''
        calculates ei(x) coeficients 
        (e1 to e3 each with 4 coeficients ie cubic)
        '''
        # finding num of 2 in modulo
        countOf2 = math.log2(self.modulo)
        # our required count of 2 in each coefficien of ei is countOf2 / 2
        reqCountOf2 = math.ceil(countOf2/2)

        min2Value = 2**reqCountOf2
        sampleSpaceU = tuple(range(min2Value, self.ei_upperLimit+1, min2Value))
        sampleSpaceL = tuple(range(2, self.ei_upperLimit+1, 2))

        # sample space for e1 poly require an aditional 2 in it
        # because it will get divided by 2 in s0 so give another 2 
        # the +1 is to make the uper limit inclusive
        sampleSpaceUe1 = tuple(range(min2Value*2, self.ei_upperLimit+1, min2Value*2))
        sampleSpaceLe1 = tuple(range(4, self.ei_upperLimit+1, 4))

        if len(sampleSpaceUe1) < 1:
            raise Exception('current ei_upperLimit too small for the modulo, sample sapce is empty')
        elif len(sampleSpaceUe1) < 2:
            print('WARNING: ei_upperLimit is very small to get any random behaviour in ei coiefficients')

        self.e1_coef = tuple(random.choices(sampleSpaceLe1, k=2) + random.choices(sampleSpaceUe1, k=2))
        self.e2_coef = tuple(random.choices(sampleSpaceL, k=2) + random.choices(sampleSpaceU, k=2))
        self.e3_coef = tuple(random.choices(sampleSpaceL, k=2) + random.choices(sampleSpaceU, k=2))
        
    def calcAiCoefficients(self):
        '''
        calculate ai (a1 to a6)
        '''
        # a1,a2,a3,a4,a5,a6
        # a1=3*a3 | a6=2*a4 | a2=n*a3 | a5=m*a6
        if self.ai_upperLimit < 3:
            raise Exception('value given for ai upper limit is too small')
        self.a3 = random.randint(1,self.ai_upperLimit//3)
        self.a4 = random.randint(1,self.ai_upperLimit//(2+2))
        
        self.a1 = 3 * self.a3
        self.a6 = 2 * self.a4
        
        self.a2 = random.randint(0,self.ai_upperLimit//self.a3) * self.a3
        self.a5 = random.randint(0,self.ai_upperLimit//self.a6) * self.a6

    def calcSCoefficients(self):
        ''' This computes coefficient of S-x'''
        # calculating s0 
        s0_coef = list(map( lambda e1i,e3i: (self.a4 * e1i + self.a5 * e3i)//self.a6 , self.e1_coef, self.e3_coef))
        #calculating s1
        s1_coef = list(map( lambda e1i,e2i: (self.a1 * e1i + self.a2 * e2i)//self.a3 , self.e1_coef, self.e2_coef))
        s1_coef[0] -= 1 # substract 1 from last element of s1_coef

        s_coef = list(map( lambda s0i,s1i: s0i+s1i, s0_coef, s1_coef) )

        self.s_coef = tuple(s_coef)
    
    def calcSInverseCoefficients(self):
        ''' computes s inverse coefficients'''
        modulo = self.modulo
        a = list(self.s_coef)
        # subtract 1x from s ( or a )
        a[1] -= 1
        # find modular multiplicative inverse of a[1]
        a1Inv = pow(a[1], -1 , modulo)

        # intializing s-1 (s inverse) array
        b = list( 0 for i in range(len(a)) )

        b[3] = -a1Inv**4 % modulo * a[3]
        b[2] = -a1Inv**3 % modulo * a[2] + a1Inv**4 % modulo * 3*a[0]*a[3]
        b[1] = a1Inv + a1Inv**3 % modulo * 2*a[0]*a[2] - a1Inv**4 % modulo * 3*a[0]**2*a[3]
        b[0] = -a1Inv * a[0] - a1Inv**3 % modulo * a[0]**2*a[2] + a1Inv**4 % modulo * a[0]**3*a[3]
        # 2 interpretation of unary minus bottom seems to be the intended one
        # as it is the common format according to wikipdia. both form passes
        # permutation and invertibility test
        b[3] = -(a1Inv**4 % modulo) * a[3]
        b[2] = -(a1Inv**3 % modulo) * a[2] + (a1Inv**4 % modulo) * 3*a[0]*a[3]
        b[1] = a1Inv + (a1Inv**3 % modulo) * 2*a[0]*a[2] - (a1Inv**4 % modulo) * 3*a[0]**2*a[3]
        b[0] = -a1Inv * a[0] - (a1Inv**3 % modulo) * a[0]**2*a[2] + (a1Inv**4 % modulo) * a[0]**3*a[3]

        # doing modulo not sure if its needed
        b = tuple(map(lambda x: x % modulo,b))
        
        self.sInv_coef = tuple(b)

    @staticmethod
    def evalPoly(p,x):
        """
        compute the value of a polynomila given its
        coefficients and value for x
        
        Parameters
        ----------
        p : list(int)
            a list of integers representing the coefficients
            in the order x0 , x1, x2, x3 ...
            i.e first element is the coeficient of x raise to 0
            and so on
        x : Number
            the value for x
        
        return
        ------
        int
            value of polynomial after evaluation
        """
        exponents=range(len(p))
        return sum(map(lambda pi,e: pi*x**e , p, exponents ))
    
    def __str__(self):
        s=''
        s+='modulo = {0[modulo]}, ei limit = {0[ei_upperLimit]} , ai Limit = {0[ai_upperLimit]}\n'.format(self.__dict__)
        s+="e1 = {0[e1_coef]} \n".format(self.__dict__)
        s+="e2 = {0[e2_coef]} \n".format(self.__dict__)
        s+="e3 = {0[e3_coef]}\n".format(self.__dict__)
        s+="a1={0[a1]}, a2={0[a2]}, a3={0[a3]}, a4={0[a4]}, a5={0[a5]}, a6={0[a6]} \n".format(self.__dict__)
        s+="s = {0[s_coef]}, s-1 = {0[sInv_coef]} ".format(self.__dict__)
        return s

class SaltGenerator_test:

    def __init__(self,sc):
        self.sc = sc
        self.log = ''
        self.failed = 0
    
    def runTest(self,show=True):
        self.printResult = show
        self.print('------ Salt Generator Test -------')
        try:
            self._test_s_x()
            self._test_s_1()
            self._test_salted_loop()
        except KeyboardInterrupt as kb_excp:
            self.log += 'Keyboard interupt recieved.\n'
            self.log_error()
            raise kb_excp
        
        if self.failed > 0:
            self.log_error()
            return False

        self.print('Generator Test complete       : PASSED ALL')
        return True

    def log_error(self):
        self.print('Generator Test complete       : FAILED', self.failed)
        # writing log to file
        with open('SaltGenerator.log','a') as f:
            import time
            ct = time.strftime('[%y-%m-%d %H:%M:%S %b %a]',time.localtime())
            f.write(ct+"\n")
            f.write(str(self.sc)+'\n')
            f.write(self.log+'\n\n')
        return False

    def _test_s_x(self):
        self.print('testing S-x')

        self.print('    {:25} :'.format('permutation test'),end=' ')
        s_coef = list(self.sc.s_coef)    # S
        s_coef[1] -= 1              # sub x from S
        resPermPoly = self.verifyPermPoly(s_coef,self.sc.modulo)
        if resPermPoly:
            self.print('PASSED')
        else:
            self.print('FAILED')
            self.failed += 1
            self.log += "S-x permutation test failed.\n"

        self.print('    {:25} :'.format('invertibility test'),end=' ')
        resInvert = self.verifyInvertibility(s_coef,self.sc.modulo)
        if resInvert:
            self.print('PASSED')
        else:
            self.print('FAILED')
            self.failed += 1
            self.log += "S-x invertibility test failed.\n"
    
    def _test_s_1(self):
        self.print('testing S-1 (S inverse)')

        self.print('    {:25} :'.format('permutation test'),end=' ')
        s_coef = list(self.sc.s_coef)    # S
        s_coef[1] -= 1              # sub x from S
        resPermPoly = self.verifyPermPoly(self.sc.sInv_coef,self.sc.modulo)
        if resPermPoly:
            self.print('PASSED')
        else:
            self.print('FAILED')
            self.failed += 1
            self.log += "S-1 permutation test failed.\n"

        self.print('    {:26}:'.format('invertibility test'),end=' ')
        resInvers = self.verifyInverse(s_coef,self.sc.sInv_coef,self.sc.modulo)
        if resInvers:
            self.print('PASSED')
        else:
            self.print('FAILED')
            self.failed += 1
            self.log += "S-1 inverse test failed.\n"

    def _test_salted_loop(self):
        try: from collatz import Collatz
        except ImportError:
            self.print("WARNING: Salted loop testing skipped. Requires collatz.py")
            return
        
        self.print('testing salted loop')

        x = 30
        c = 30
        failed_result = {}
        check_hailstone_sequence = True
        max_hailstone_check_number = int(math.sqrt(self.sc.modulo))
        all_hailstone_sequence_passed = True
        all_payload_execution_passed = True
        all_while_condition_passed = True

        for y in range(2,self.sc.modulo):
            res = self.saltedLoop(x,c,y)
            info = {}
            info['payload_executed'] = res[0]
            info['while_condition_stops'] = res[1]
            info['hailstone_sequence_match'] = True
            
            if check_hailstone_sequence:
                correct_hailstone = Collatz.hailstoneSequence(y)
                if correct_hailstone != tuple(res[2]):
                    info['hailstone_sequence_match'] = False
                    info['hailstone_sequence'] = res[2]
                    info['retrived_hailstone_len'] = len(res[2])
                    info['correct_hailstone_len'] = len(correct_hailstone)
                    info['matched_hailstone_len'] = min(len(correct_hailstone),len(res[2]))
                    for i in range( min(len(correct_hailstone),len(res[2])) ):
                        if correct_hailstone[i] != res[2][i]:
                            info['matched_hailstone_len'] = i
                            break
                if y > max_hailstone_check_number:
                    check_hailstone_sequence = False
                    self.print('    {:25} :'.format('hailstone test (2-'+str(max_hailstone_check_number)+')'),end=' ')
                    if all_hailstone_sequence_passed: self.print('PASSED')
                    else: self.print('FAILED'); self.failed += 1

            info['passed_all'] = info['payload_executed'] and info['while_condition_stops'] and info['hailstone_sequence_match']
            if not info['passed_all']:
                failed_result[y]=info
            
            all_hailstone_sequence_passed = all_hailstone_sequence_passed and info['hailstone_sequence_match']
            all_payload_execution_passed = all_payload_execution_passed and info['payload_executed']
            all_while_condition_passed = all_while_condition_passed and info['while_condition_stops']
        
        self.print('    {:25} :'.format('payload execution test'),end=' ')
        if all_payload_execution_passed: self.print('PASSED')
        else: self.print('FAILED'); self.failed += 1
        
        self.print('    {:25} :'.format('while condition test'),end=' ')
        if all_while_condition_passed: self.print('PASSED')
        else: self.print('FAILED'); self.failed += 1

        if len(failed_result) > 0:
            self.log += "Salted loop test failed.\n"
            self.log += "Salted loop failed results:\n"
            self.log += str(failed_result)
        

    def verifyInvertibility(self,poly,modulo):
        status = True
        # check x coeifficient is odd
        status &= (poly[1]&1)
        # check coifficient above x are even
        for i in range(2,len(poly)):
            status &= not (poly[i]&1)
        # check square of coifficient above x are 0 mod modulo
        for i in range(2,len(poly)):
            status &= not (poly[i]**2 % modulo)
        return status

    def verifyPermPoly(self,poly,modulo):
        yValues=[]
        for i in range(modulo):
            y = SaltGenerator.evalPoly(poly,i) % modulo
            yValues.append(y)
        yValues.sort()
        yValuesSet=set(yValues)
        return yValuesSet == set(range(0,modulo))

    def verifyInverse(self,poly,ipoly,modulo):
        #valuesPoly, valuesIpoly = [],[]
        for i in range(modulo):
            y = SaltGenerator.evalPoly(poly,i) % modulo
            x = SaltGenerator.evalPoly(ipoly,y) % modulo
            #valuesPoly.append(y)
            #valuesIpoly.append(x)
            if x != i:
                return False
        return True		

    def saltedLoop(self,x,c,y):
        payload_executed = False
        will_while_stop = True
        hailstoneSequence = []
        iteration, max_iteration = 0, 3000
        # salted Loop ------------------
        e1 = self.sc.evalPoly(self.sc.e1_coef,x)
        e2 = self.sc.evalPoly(self.sc.e2_coef,x)
        e3 = self.sc.evalPoly(self.sc.e3_coef,x)
        s0 = (self.sc.a4 * e1 + self.sc.a5 * e3)//self.sc.a6
        s1 = (self.sc.a1 * e1 + self.sc.a2 * e2)//self.sc.a3 - 1
        s = s0 + s1
        yr = y
        sr = 0
        while(self.sc.evalPoly(self.sc.sInv_coef,yr-x-1) % self.sc.modulo != x):
            yr = yr + e1 - sr
            if yr % 2 == 1:
                yr = (self.sc.a1 * yr + self.sc.a2 * e2)//self.sc.a3 + s0
                hailstoneSequence.append(0)
            else:
                yr = (self.sc.a4 * yr + self.sc.a5 * e3)//self.sc.a6 + s1
                hailstoneSequence.append(1)
            sr = s

            # temp code-----------
            if y == 63:
                print(yr%self.sc.modulo,end=", ")
            # end temp code -----------

            if self.sc.evalPoly(self.sc.sInv_coef,(yr-c-1)) % self.sc.modulo == x :
                # .............. PAYLOAD BLOCK .................
                payload_executed = True
                will_while_stop = not (self.sc.evalPoly(self.sc.sInv_coef,yr-x-1) % self.sc.modulo != x)
                break
            
            # forced iteration breaker
            iteration += 1
            if iteration > max_iteration:
                payload_executed = False
                will_while_stop = False
                hailstoneSequence = [y]
                break
        # END Salted Loop ----------------
        return payload_executed,will_while_stop,hailstoneSequence

    def print(self,*argv,**kwarg):
        '''This is just to support conditional printing of error'''
        if self.printResult:
            print(*argv,**kwarg)

if __name__=='__main__':
    sg=SaltGenerator(1<<16,1<<9,100)
    sgt=SaltGenerator_test(sg)
    sgt.runTest()
    print(sg)

    #sc.saltedCode()