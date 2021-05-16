// collatz rounds counter
#include<iostream>
#include <fstream>
#include<conio.h>

int main()
{
	unsigned long long MAX_CHECK_NUMBER = 4294967295ul;
	//unsigned long long MAX_CHECK_NUMBER = 100ul;
	int INT_SIZE = 32;
	
	unsigned int n,print_mask,avgIteration;
	unsigned long long i,numRounds,maxIteration = 0,totalIterationCount=0;
	
	print_mask = ((1 << 20)-1);

    std::cout<<"Calculating number of iterations in collatz conjecture"<<std::endl;
    std::cout<<"Highest input : "<< MAX_CHECK_NUMBER<<std::endl;
    std::cout<<"Integer Size : "<<INT_SIZE<<std::endl;
	
	std::fstream ff;
	if(!ff.is_open())
		std::cout<<"no file"<<std::endl;
	
    for(i=1ul; i < MAX_CHECK_NUMBER; i+=1ul)
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
		
        if((i & print_mask) == 0){    
            std::cout<<i<<"\r";
			if(i > 4294967290ul)
			{
				if(!ff.is_open())
					ff.open("resultklklj.txt",std::ios::out);
				ff<<"cur = "<<i<<"Max iteration = "<<maxIteration<<" , avg Iteration = "<<avgIteration<<" , rest total = "<<totalIterationCount<<std::endl<<std::flush;
			}
		}
	}
	ff.close();
	
	std::cout<<"Max iteration = "<<maxIteration<<" , avg Iteration = "<<avgIteration<<" , rest total = "<<totalIterationCount<<std::endl;
	getch();
}