from collatz import Collatz
import csv
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
import math

INT_SIZE = 32
MAX_CHECK_NUMBER = 10000
DATA_CSV_NAME = 'Collatz_Iterations'

def main():
    while True:
        print('1. find iterations')
        print('2. visualize iterations')
        print('0. to exit')
        cho = int(input())
        if cho == 1 :
            findIteration_init()
            if MAX_CHECK_NUMBER < 1_000_000:
                findIteration()
            else:
                findIteration_fast()
        elif cho == 2 :
            visualize_init()
        elif cho == 0 :
            exit()
        else:
            print('invalid input') 

def visualize_init():
    dir="data\\"
    files=[]
    for filename in os.listdir(dir):
        if filename.endswith('.csv'):
            files.append(filename)
    print('choose csv file')
    for i,filename in enumerate(files):
        print('{}. {}'.format(i+1,filename))
    cho = int(input())
    visualize(files[cho-1])

def visualize(filename):
    maxNum, intsize = extractFilename(filename)
    csv = pd.read_csv('data\\'+filename,dtype={'Integer Overflow':str})
    maxValue = max(csv['Iteration'])
    corr = round(csv.corr()['Iteration']['X'],3)
    overflows = 0
    try:
        overflows = csv['Integer Overflow'].value_counts()['overflow']
    except KeyError:
        pass
    stdDeviation = round(csv['Iteration'].std(),3)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    csv.plot(x='X',y='Iteration',ax=ax)
    ax.set_ylabel('Iteration')
    ax.set_title('X vs Iteration '+maxNum+' '+intsize)
    fig.text(.01,.01,'Max: {} Overflows: {} Correlation: {} stdDeviation: {} '.format(maxValue,overflows,corr,stdDeviation))

    freq = csv['Iteration'].value_counts()
    freq.sort_index(inplace=True)
    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    freq.plot(ax=ax2)
    ax2.set_xlabel('Iteration')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Iteration vs Frequency '+maxNum+' '+intsize)

    plt.show()



def extractFilename(filename):
    filename = re.sub(r'\.csv$','',filename)
    arr = filename.split('_')
    return arr[-2],arr[-1]
#---------------------------------------------------
def findIteration_init():
    print('enter max value to run to: ')
    m = re.sub(r'[^\d]','',input())
    if len(m) == 0:
        m = 1000
        print('    using default value %d'%(m))
    print('enter integer size: ')
    n = re.sub(r'[^\d]','',input())
    if len(n) == 0:
        n = 32
        print('    using default value %d'%(n))
    global MAX_CHECK_NUMBER,INT_SIZE
    MAX_CHECK_NUMBER = int(m)
    INT_SIZE = int(n)

def findIteration():
    print('Calculating number of iterations in collatz conjecture')
    print('Highest input : %d' % (MAX_CHECK_NUMBER))
    print('Integer Size : %d' % (INT_SIZE))

    dataHeading = ('X','Iteration','Integer Overflow','First Overflow Index','Overflow Number')
    dataTable = list()
    for i in range(1,MAX_CHECK_NUMBER+1):
        seq = Collatz.collatzSequence(i);
        numRounds = len(seq)
        isOverflow,overflowIndex,overflowNum = checkIntegerOverflow(seq)
        dataRow = [i,numRounds]
        if isOverflow:
            dataRow.extend(['overflow',overflowIndex,overflowNum])
        dataTable.append(dataRow)
        print(i,end='\r')
    f = writeDataCSV(dataTable,dataHeading)
    print('Data File : ' + f)

def findIteration_fast():
    global MAX_CHECK_NUMBER
    print('Calculating number of iterations in collatz conjecture')
    print('Highest input : %d' % (MAX_CHECK_NUMBER))
    print('Integer Size : %d' % (INT_SIZE))
    
    dataHeading = ('X','Iteration','Integer Overflow','First Overflow Index','Overflow Number')
    dataTable = list()
    int_size_mask = (1<< INT_SIZE) - 1
    MAX_CHECK_NUMBER = MAX_CHECK_NUMBER & int_size_mask
    print_mask = ((1 << 20)-1)
	
    for i in range(1,MAX_CHECK_NUMBER+1):
        n = i & int_size_mask
        numRounds = 0
        while n > 1:
            if (n & 1) == 1:
                n = 3*n + 1
            else:
                n = n // 2
            numRounds += 1
            n = n & int_size_mask
        if (i & print_mask) == 0:    
            print(i,end="\r")
		
        dataRow = [i,numRounds]
        dataTable.append(dataRow)
        #print(i,end="\r")
            
    f = writeDataCSV(dataTable,dataHeading)
    print('Data File : ' + f)
        

def checkIntegerOverflow(seq):
    for index,num in enumerate(seq):
        if num >= pow(2,INT_SIZE):
            return True,index,num
    return False,0,0

def writeDataCSV(data,heading = None):
    fileName = "data\{}_{}_{}.csv".format(DATA_CSV_NAME,MAX_CHECK_NUMBER,INT_SIZE)
    with open(fileName,'w',newline='') as f:
        writer = csv.writer(f)
        if heading: writer.writerow(heading)
        writer.writerows(data)
    return fileName

#----------------------------------------

if __name__ == '__main__':
    main();