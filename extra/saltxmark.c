#include<stdio.h>
#include<stdlib.h>
#include<math.h>
#include<time.h>
typedef struct termType {
    int coefficient, exponent;
} termType;

typedef struct poly {
    termType terms[100];
    int noOfTerms;
} poly;

/*Polynomial Addition*/
poly * addPoly(poly *p1, poly *p2) {
    int i, j, k, l;
    poly *p3 = malloc(sizeof (poly));

    for (i = 0, j = 0, k = 0; ((i < p1->noOfTerms)&&(j < p2->noOfTerms)); k++) {
        if (p1->terms[i].exponent == p2->terms[j].exponent) {
            p3->terms[k].coefficient = p1->terms[i].coefficient + p2->terms[j].coefficient;
            p3->terms[k].exponent = p1->terms[i].exponent;
            i++;
            j++;
        } else if (p1->terms[i].exponent < p2->terms[j].exponent) {
            p3->terms[k].coefficient = p1->terms[i].coefficient;
            p3->terms[k].exponent = p1->terms[i].exponent;
            i++;
        } else {
            p3->terms[k].coefficient = p2->terms[j].coefficient;
            p3->terms[k].exponent = p2->terms[j].exponent;
            j++;
        }
    }

    if (i < p1->noOfTerms) {
        for (l = i; l < p1->noOfTerms; l++, k++) {
            p3->terms[k].coefficient = p1->terms[l].coefficient;
            p3->terms[k].exponent = p1->terms[l].exponent;
        }
    } else {
        for (l = j; l < p2->noOfTerms; l++, k++) {
            p3->terms[k].coefficient = p2->terms[l].coefficient;
            p3->terms[k].exponent = p2->terms[l].exponent;
        }
    }
    p3->noOfTerms = k;

    return p3;
}

/*Multiply polynomial with constant*/
poly * mulPoly(poly *p, int q) {
int i, j, k, l;
    poly *p4 = malloc(sizeof (poly));

    for (i = 0, k = 0; i < p->noOfTerms; k++) {
        
            p4->terms[k].coefficient = p->terms[i].coefficient * q;
            p4->terms[k].exponent = p->terms[i].exponent;
            i++;
    }
 p4->noOfTerms = k;

    return p4;
}

/*Divide polynomial with constant*/
poly * divPoly(poly *p, int r) {
int i, j, k, l;
    poly *p6 = malloc(sizeof (poly));

    for (i = 0, k = 0; i < p->noOfTerms; k++) {
        
            p6->terms[k].coefficient = p->terms[i].coefficient / r;
            p6->terms[k].exponent = p->terms[i].exponent;
            i++;
    }
 p6->noOfTerms = k;

    return p6;
}

/*Subtract polynomial with constant*/
poly * subPoly(poly *p, int t) {
int i,l, k;
    poly *p7 = malloc(sizeof (poly));
    for (i=0, k = 0; i < p->noOfTerms; k++) {   
        if(p->terms[i].exponent==0) {
            p7->terms[k].coefficient = p->terms[i].coefficient - t;
            p7->terms[k].exponent = p->terms[i].exponent;
            i++;
    }
else {
       p7->terms[k].coefficient = p->terms[i].coefficient;
       p7->terms[k].exponent = p->terms[i].exponent;
       i++;
}
    }
    p7->noOfTerms = k;
    return p7;
}

/*Polynomial evaluation*/
int evalPoly(poly *p, int x, int pr) {
int i,k,tm,power,powervalue,termvalue,result=0,ans=0;
 for(i=0,k=0; i < p->noOfTerms; i++) {
  power = p->terms[i].exponent;
  powervalue = pow(x,power);
  termvalue = powervalue * p->terms[i].coefficient ;
  result  += termvalue;
  ans=result%pr;
 }
return ans;
}

/*Modular Multiplicative Inverse*/
int mul_inv(int a, int b)
{
	int b0 = b, t, q;
	int x0 = 0, x1 = 1;
	if (b == 1) return 1;
	while (a > 1) {
		q = a / b;
		t = b, b = a % b, a = t;
		t = x0, x0 = x1 - q * x0, x1 = t;
	}
	if (x1 < 0) x1 += b0;
	return x1;
}

/*Inverse permutation polynomial*/
int inv_perm_poly(int a0,int a1,int a2,int a3,int x)
{
 int a1_inv,b0,b1,b2,b3,pri=16,s_inv;   
 a1_inv=mul_inv(a1,pri);
 b3 = -(pow(a1_inv,4)*a3);
 b2 = -(a2*pow(a1_inv,3)) + (3*a0*a3*pow(a1_inv,4));
 b1 = a1_inv + (2*a0*a2*pow(a1_inv,3)) - (3*a3*pow(a0,2)*pow(a1_inv,4));
 b0 = -(a0*a1_inv) - (pow(a0,2)*pow(a1_inv,3)*a2) + (pow(a0,3)*pow(a1_inv,4)*a3);
 s_inv=(b0+b1*x+b2*x*x+b3*x*x*x) % pri;
 if(s_inv>=1)
	return s_inv;
 else 
	return s_inv+pri;
}

/*main function begins*/
int main()
{
 int key(int x,int m);
 void print(poly *p);
  termType t1, t2, t3, t4, t5, t6, t7, t8, t9, t10, t11, t12;
    poly *p1, *p2, *p3, *p4, *p5, *p6, *p7, *p8, *p9, *p10, *p11, *p12, *p13;
    int a1=9,a2=15,a3=3,a4=4,a5=24,a6=8,q=1,pri=16,c,d;
    int z1,z2,z3,z4,z5,z6,c0,c1,c2,c3;
    int y,x,tmp,r=0,h,i,m;
    
printf("Enter input:");
    scanf("%d",&x);

printf("Enter key:");
    scanf("%d",&m);

    p1 = malloc(sizeof (poly));
    p2 = malloc(sizeof (poly));
    p3 = malloc(sizeof (poly));
    p4 = malloc(sizeof (poly));
    p5 = malloc(sizeof (poly));
    p6 = malloc(sizeof (poly));
    p7 = malloc(sizeof (poly));
    p8 = malloc(sizeof (poly));
    p9 = malloc(sizeof (poly));
    p10 = malloc(sizeof (poly));
    p11 = malloc(sizeof (poly));
    p12 = malloc(sizeof (poly));
    p13 = malloc(sizeof (poly));


    t1.coefficient = 24;
    t1.exponent = 3;
    t2.coefficient = 48;
    t2.exponent = 2;
    t3.coefficient = 28;
    t3.exponent = 1;
    t4.coefficient = 14 ;
    t4.exponent = 0;

    t5.coefficient = 38;
    t5.exponent = 3;
    t6.coefficient = 20;
    t6.exponent = 2;
    t7.coefficient = 46;
    t7.exponent = 1;
    t8.coefficient = 32;
    t8.exponent = 0;

    t9.coefficient = 46;
    t9.exponent = 3;
    t10.coefficient = 32;
    t10.exponent = 2;
    t11.coefficient = 48;
    t11.exponent = 1;
    t12.coefficient = 28; 
    t12.exponent = 0;

    p1->terms[0] = t1;
    p1->terms[1] = t2;
    p1->terms[2] = t3;
    p1->terms[3] = t4;
    p1->noOfTerms = 4;

    p2->terms[0] = t5;
    p2->terms[1] = t6;
    p2->terms[2] = t7;
    p2->terms[3] = t8;
    p2->noOfTerms = 4;
    
    p3->terms[0] = t9;
    p3->terms[1] = t10;
    p3->terms[2] = t11;
    p3->terms[3] = t12;
    p3->noOfTerms = 4;
//calculate s0
    p4 = mulPoly(p1,a4);
    p5 = mulPoly(p3,a5);
    p6 = addPoly(p4,p5);
    p7 = divPoly(p6,a6);
//calculate s1
    p8 = mulPoly(p1,a1);
    p9 = mulPoly(p2,a2);
    p10 = addPoly(p8,p9);
    p11 = divPoly(p10,a3);
    p12 = subPoly(p11,q);
//calculate s=s0+s1
    p13 = addPoly(p7,p12);
//evaluatepolynomials
    z1 = evalPoly(p1,x,pri);
    z2 = evalPoly(p2,x,pri);
    z3 = evalPoly(p3,x,pri);
    z4 = evalPoly(p7,x,pri);
    z5 = evalPoly(p12,x,pri);
    z6 = evalPoly(p13,x,pri); 
 
   c0=p13->terms[3].coefficient % pri;
   c1=(p13->terms[2].coefficient -1) % pri;
   c2=p13->terms[1].coefficient % pri;
   c3=p13->terms[0].coefficient % pri;

/*salted collatz*/

y=key(x,m);
if(m==5) {
 c=inv_perm_poly(c0,c1,c2,c3,y-x-1);
tmp=y;
  if(r==0)
   {
     z6=0;
   }
while(inv_perm_poly(c0,c1,c2,c3,y-x-1)!=x) //substitute s^-1(y-x-1)==x
{
 y=tmp+z1-z6;
 if(y%2==1)
 {
   y=(a1*y+a2*z2)/a3+z4;
 }
 else
 {
   y=(a4*y+a5*z3)/a6+z5;
 }
 tmp=y;
 z6 = evalPoly(p13,x,pri);
 c=inv_perm_poly(c0,c1,c2,c3,y-x-1);
 d=inv_perm_poly(c0,c1,c2,c3,y-15);
r++;
  if(inv_perm_poly(c0,c1,c2,c3,y-15)==x && c==x)//substitute s^-1(y-31)==x
     {
	int var1=10,var2=50,var3;
        var3=var1+var2;
        printf("\nSum = %d\n",var3);
        break;
     }
}
	}
printf("Exit");
}
/*main function end here*/
 
/*print polynomial*/
void print(poly *p) {
    int i, c,pri=16;
    c = 0;
    for (i = 0; i < p->noOfTerms; i++) {
        if (c != 0 && c < p->noOfTerms && p->terms[i].coefficient > 0) {
            printf("+");
        }
        printf("%dx^%d", p->terms[i].coefficient, p->terms[i].exponent);
        c++;
    }
     printf(" mod %d",pri);
}

/*phi function*/
int key(int x,int m)
{
  int s;
    if(x==14 && m==5)
{
 s=3;
}
else {
    s = 2*(x+m)+1;
}
    return s;
}
