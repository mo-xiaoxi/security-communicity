#include<iostream>
#include<stdio.h>
using namespace std;


int main()  
{  
	FILE *fp1;
	FILE *fp2; 
	int a=0;
	int b=-1;
	//∂¡»Î ˝æ› 
	if((fp1=fopen("count.txt","w"))==NULL)
	{
		printf("Error\n"); 
	} 
	fprintf(fp1,"%d",a);
	fclose(fp1);
	
	
	if((fp2=fopen("s_count.txt","w"))==NULL)
	{
		printf("Error\n"); 
	} 
	fprintf(fp2,"%d",b);
	fclose(fp2); 
  
   
    return 0;  
}
  

