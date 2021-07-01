import random
import math 
import re

class SaltedCollatz:
    def __init__(self,modulo = 64,eil = 100, ail = 60):
        '''
        parameters
        ----------
        modulo : int
            an integer of form 2^n.
        eil : int
            upper limit for coeficients of ei polynomial. 
            It should be grater than square root of modulo,
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
        # finding num of 2 in modulo
        countOf2 = math.log2(self.modulo)
        # our required count of 2 in each coefficien of ei is countOf2 / 2
        reqCountOf2 = math.ceil(countOf2/2)

        min2Value = 2**reqCountOf2
        sampleSpaceU = tuple(range(min2Value, self.ei_upperLimit, min2Value))
        sampleSpaceL = tuple(range(2, self.ei_upperLimit, 2))

        # sample space for e1 poly require an aditional 2 in it
        # because it will get divided by 2 in s0 so give another 2 
        sampleSpaceUe1 = tuple(range(min2Value*2, self.ei_upperLimit, min2Value*2))
        sampleSpaceLe1 = tuple(range(4, self.ei_upperLimit, 4))

        if len(sampleSpaceUe1) < 1:
            raise Exception('current ei_upperLimit too small for the modulo, sample sapce is empty')
        elif len(sampleSpaceUe1) < 2:
            print('ei_upperLimit is very small to get any random behaviour in ei coiefficients')

        self.e1_coef = tuple(random.choices(sampleSpaceLe1, k=2) + random.choices(sampleSpaceUe1, k=2))
        self.e2_coef = tuple(random.choices(sampleSpaceL, k=2) + random.choices(sampleSpaceU, k=2))
        self.e3_coef = tuple(random.choices(sampleSpaceL, k=2) + random.choices(sampleSpaceU, k=2))
        
    def calcAiCoefficients(self):
        # a1,a2,a3,a4,a5,a6
        # a1=3*a3 | a6=2*a4 | a2=n*a3 | a5=m*a6
        if self.ai_upperLimit < 3:
            raise Exception('value given for ai upper limit is too small')
        self.a3 = random.randint(1,self.ai_upperLimit//3)
        self.a4 = random.randint(1,self.ai_upperLimit//2)
        
        self.a1 = 3 * self.a3
        self.a6 = 2 * self.a4
        
        self.a2 = random.randint(0,self.ai_upperLimit//self.a3) * self.a3
        self.a5 = random.randint(0,self.ai_upperLimit//self.a6) * self.a6

    def calcSCoefficients(self):
        ''' This calculates coefficient of S-x'''
        # calculating s0 
        s0_coef = list(map( lambda e1i,e3i: (self.a4 * e1i + self.a5 * e3i)//self.a6 , self.e1_coef, self.e3_coef))
        #calculating s1
        s1_coef = list(map( lambda e1i,e2i: (self.a1 * e1i + self.a2 * e2i)//self.a3 , self.e1_coef, self.e2_coef))
        s1_coef[0] -= 1 # substract 1 from last element of s1_coef

        s_coef = list(map( lambda s0i,s1i: s0i+s1i, s0_coef, s1_coef) )

        self.s_coef = tuple(s_coef)
    
    def calcSInverseCoefficients(self):
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
        
        self.sInv_coef = tuple(b)
    
    #@staticmethod
    def saltedCode(self):
        code = """
e1,e2,e3 = e1_val, e2_val, e3_val
s0 = (a4*e1 + a5*e3)//a6
s1 = (a1*e1 + a2*e2)//a3 - 1
s = s0 + s1
while(evalPoly(sInv,yr-x-1) % modulo != x):
    yr = yr + e1 - sr
    if yr % 2 == 1:
        yr = (a1 * yr + a2 * e2)//a3 + s0
    else:
        yr = (a4 * yr + a5 * e3)//a6 + s1
    sr = s

    if evalPoly(sInv,(yr-c-1)) % modulo == x :
        print('\\n....payload block....\\n')
        break

        """
        code = code.replace('sInv',self.sInv_coef.__str__())
        code = code.replace('modulo',self.modulo.__str__())
        code = code.replace('e1_val','evalPoly({},x)'.format(self.e1_coef))
        code = code.replace('e2_val','evalPoly({},x)'.format(self.e2_coef))
        code = code.replace('e3_val','evalPoly({},x)'.format(self.e3_coef))
        code = code.replace('a1',self.a1.__str__())
        code = code.replace('a2',self.a2.__str__())
        code = code.replace('a3',self.a3.__str__())
        code = code.replace('a4',self.a4.__str__())
        code = code.replace('a5',self.a5.__str__())
        code = code.replace('a6',self.a6.__str__())

        with open('kil.txt','w') as f:
            f.write(code)

    @staticmethod
    def evalPoly(p,x):
        """
        compute the value of a polynomila given its
        coefficients and value for x
        
        Parameters
        ----------
        p : list(int)
            a list of integers representing the coefficients
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
        s+="e1 = {0[e1_coef]} = {0[e1]} \n".format(self.__dict__)
        s+="e2 = {0[e2_coef]} = {0[e2]} \n".format(self.__dict__)
        s+="e2 = {0[e3_coef]} = {0[e3]} \n".format(self.__dict__)
        s+="a1={0[a1]}, a2={0[a2]}, a3={0[a3]}, a4={0[a4]}, a5={0[a5]}, a6={0[a6]} \n".format(self.__dict__)
        s+="s0 = {0[s0]}, s1 = {0[s1]} \n".format(self.__dict__)
        s+="s = {0[s_coef]} = {0[s]}, s-1 = {0[sInv_coef]} ".format(self.__dict__)
        return s

class SaltedCollatz_test:
    
    def test(self,sc):
        print('--- Salted Collatz Test ----')
        print('S - X ')
        print('  permutation test :',end=' ')
        s_coef = list(sc.s_coef)
        s_coef[1] -= 1
        print('passed') if self.verifyPermPoly(s_coef,sc.modulo) else print('failed')
        print('  invertibility test :',end=' ')
        print('passed') if self.verifyInvertibility(s_coef,sc.modulo) else print('failed')

        print('S-1 ')
        print('  permutation test :',end=' ')
        print('passed') if self.verifyPermPoly(sc.sInv_coef,sc.modulo) else print('failed')
        print('  inverse test :',end=' ')
        print('passed') if self.verifyInverse(s_coef,sc.sInv_coef,sc.modulo) else print('failed')

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
            y = SaltedCollatz.evalPoly(poly,i) % modulo
            yValues.append(y)
        yValues.sort()
        yValuesSet=set(yValues)
        return yValuesSet == set(range(0,modulo))

    def verifyInverse(self,poly,ipoly,modulo):
        #valuesPoly, valuesIpoly = [],[]
        for i in range(modulo):
            y = SaltedCollatz.evalPoly(poly,i) % modulo
            x = SaltedCollatz.evalPoly(ipoly,y) % modulo
            #valuesPoly.append(y)
            #valuesIpoly.append(x)
            if x != i:
                return False
        return True		

if __name__=='__main__':
    sc=SaltedCollatz()
    sct=SaltedCollatz_test()
    sct.test(sc)
    #print(sc)

    sc.saltedCode()