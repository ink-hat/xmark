#include<stdio.h>

void main()
{
	unsigned int k;
	do
	{
		printf("enter No: ");
		scanf("%u",&k);
		printf("signed version : %d\n",k);
	}while(k != 0);
}