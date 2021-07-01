from collatz import Collatz,Collatz_test
from salted_collatz import SaltedCollatz,SaltedCollatz_test
 
def main():
    global x,y
    global e1,e2,e3,a1,a2,a3,a4,a5,a6,s0,s1,s,sInv,modulo

    x = 30
    y = 63

    # calculating values for salted collatz
    sc = SaltedCollatz(x)
    SaltedCollatz_test().test(sc)
    #print(sc)
    
    # initializing variables
    e1,e2,e3 = sc.e1, sc.e2, sc.e3
    a1,a2,a3,a4,a5,a6 = sc.a1, sc.a2, sc.a3, sc.a4, sc.a5, sc.a6
    s0,s1,s = sc.s0, sc.s1, sc.s
    sInv = sc.sInv_coef
    modulo =  sc.modulo
    # calling embedded function
    hailstoneSequence = target_func()

    Collatz_test().test(hailstoneSequence,y)
    print('retrived hailstone sequenc : ({})'.format(len(hailstoneSequence)))
    print(hailstoneSequence)
    hailstoneSequenceO = Collatz.hailstoneSequence(y)
    print('correct hailstone sequenc : ({})'.format(len(hailstoneSequenceO)))
    print(hailstoneSequenceO)
    subset=False
    if len(hailstoneSequence) <= len(hailstoneSequenceO):
        subset = hailstoneSequenceO[:len(hailstoneSequence)] == hailstoneSequence
    print("retrived subset of correct sequence : "+("true" if subset else "fasle"))

def target_func():
    yr = y
    c = 30
    sr = 0
    hailstoneSequence = []
    while(SaltedCollatz.evalPoly(sInv,yr-x-1) % modulo != x):
    #while(True):
        yr = yr + e1 - sr
        if yr % 2 == 1:
            yr = (a1 * yr + a2 * e2)//a3 + s0
            hailstoneSequence.append(0)
        else:
            yr = (a4 * yr + a5 * e3)//a6 + s1
            hailstoneSequence.append(1)
        sr = s

        if SaltedCollatz.evalPoly(sInv,(yr-c-1)) % modulo == x :
            print('\n....payload block....\n')
            break
    return tuple(hailstoneSequence)
        
if __name__ == '__main__':
    main()