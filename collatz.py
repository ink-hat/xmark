class Collatz:
    """
    contains common functions for Collatz Conjecture
    
    all methods in this class are class methods so
    no object creation  required
    """
    @classmethod
    def collatz(cls,a):
        '''
        apply collatz function on a given number

        Parameters
        ----------
        a : int
        
        Return
        ------
        int
        '''
        if a&1 :
            return 3*a+1
        else:
            return int(a/2)

    @classmethod
    def collatzSequence(cls,a):
        '''
        return the collatz sequence of a number
        
        This will calculate all the sequence of numbers 
        to get to 1 using collatz function and returns this sequence
        including 1 and excluding the orginal number

        Parameters
        ----------
        a : int

        Return
        ------
        tuple(int)
            this sequence does not contain the original input
        '''
        seq = []
        # old code ------
        # while a != 1:
        #     a=cls.collatz(a)
        #     seq.append(a)
        # --------------
        
        # this modified code produce collatz sequence of 1
        while True:
            a=cls.collatz(a)
            seq.append(a)
            if a == 1: break
        return seq

    @classmethod
    def hailstoneSequence(cls,a):
        '''
        Returns the hailstone sequence 

        This will calculate expected hailstone sequence 
        of a given number, so it can be used to check problems
        in generated hailstone sequence

        Parameters
        ----------
        a : int

        Return
        ------
        tuple(int)
            each entry will be either 0 or 1
            odd -> 0,  even -> 1
            this sequence will contain hailstone value of original input
            but not that of 1
        '''
        seq = cls.collatzSequence(a)
        seq = [a] + list(seq[0:-1])
        return tuple(map(lambda x: 1-x&1, seq))
    
    @classmethod
    def retriveWatermark(cls,seq):
        """
        Calculates the watermark for a given hailstone sequence

        Parameters
        ----------
        seq : tuple(int) or list(int)
            each entry in the list should be either 0 or 1

        Return
        ------
        int : the watermark
        """
        w = 1
        for i in seq[::-1]:
            if i == 1:
                w*=2
            else:
                w = (w-1)//3
        return w

class Collatz_test:
    def test(self,seq,y):
        print('--- Collatz Test ---')
        self.verifyHailstoneSequence(seq,y)
        self.verifyWaterMark(seq,y)
    
    def verifyHailstoneSequence(self,seq,y):
        print('Hailstone sequence :',end=' ')
        print('passed') if seq == Collatz.hailstoneSequence(y) else print('failed')
    
    def verifyWaterMark(self,seq,y):
        print('Watermark retrival :',end=' ')
        print('passed') if y == Collatz.retriveWatermark(seq) else print('failed')

if __name__=='__main__':
    a = input('enter a number: ')
    a = int(a)
    print(Collatz.collatzSequence(a))
    seq = Collatz.hailstoneSequence(a)
    print(seq)
    print('retrived watermark: ',Collatz.retriveWatermark(seq))
    Collatz_test().test(seq,a)