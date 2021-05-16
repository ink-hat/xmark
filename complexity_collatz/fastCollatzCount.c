// collatz rounds counter
#include<stdio.h>
#include<conio.h>

void main()
{
	unsigned long long MAX_CHECK_NUMBER = 4294967295ul;
	int INT_SIZE = 32;
	
	unsigned int i,n,print_mask,avgIteration;
	unsigned long long numRounds,maxIteration = 0,totalIterationCount=0;
	
	print_mask = ((1 << 20)-1);

    printf("Calculating number of iterations in collatz conjecture\n");
    printf("Highest input : %llu\n", MAX_CHECK_NUMBER);
    printf("Integer Size : %d\n",INT_SIZE);
	
    for(i=1; i <= MAX_CHECK_NUMBER; i++)
	{
        n = i;
        numRounds = 0;
        while(n > 1)
		{
            if(n & 1)
                n = 3*n + 1;
            else
                n = n / 2;
            numRounds += 1;
		}
			
		totalIterationCount += numRounds;
		
		if(numRounds > maxIteration)
			maxIteration = numRounds;
		
		if(totalIterationCount >= MAX_CHECK_NUMBER)
		{
			avgIteration++;
			totalIterationCount -= MAX_CHECK_NUMBER;
		}
		
        if((i & print_mask) == 0)    
            printf("%d\r",i);
	}
	
	printf("Max iteration = %llu , avg Iteration = %u , rest total = %llu ",maxIteration,avgIteration,totalIterationCount);
	getch();
}