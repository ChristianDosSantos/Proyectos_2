#include "filter.h"

//Complementary functions
int mult(int a,int b,int n){
	return (a*b)/n;
}


//---------------------------------------------------------

//Methods implementation
void init_filter(filter *x,unsigned char f_P,int *f_b,int *f_input){
	x->f_P=f_P;	
	x->f_b=f_b;
	x->f_input=f_input;
}

int  eval_filter(filter *x,int new_input){

	//Define new output variable
	int new_output=0;
	unsigned char i;

	//Calc output
	new_output+=mult(*x->f_b,new_input,MULT_SCALE);
	for (i = 0; i < x->f_P; i++)
		new_output+=mult(*(x->f_b+i+1),*(x->f_input+i),MULT_SCALE);
			
	//Update mem
	for(i = x->f_P; i >1 ; i--)
		*(x->f_input+i-1)=*(x->f_input+i-2);
	*x->f_input=new_input;


	if(new_output<0)
		new_output=0;

	return  new_output;
}
