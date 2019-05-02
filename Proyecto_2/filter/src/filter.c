#include "filter.h"
#include <stdio.h>

//Complementary functions
signed short  mult(signed short a,signed short b,signed short n){
	return (a*b)/n;
}


//---------------------------------------------------------


//Methos implementation
void init_filter(filter *x,unsigned char f_Q,unsigned char f_P,signed short *f_a,signed short *f_b,signed short *f_output,signed short *f_input){
	x->f_Q=f_Q;
	x->f_P=f_P;
	x->f_a=f_a;
	x->f_b=f_b;
	x->f_output=f_output;
	x->f_input=f_input;
}

unsigned short eval_filter(filter *x,unsigned short new_input){

	//Define new output variable
	unsigned short new_output=0;

	//Calc output
	new_output+=mult(*x->f_b,new_input,MULT_SCALE);
	for (unsigned char i = 0; i < x->f_P; i++)
		new_output+=mult(*(x->f_b+i+1),*(x->f_input+i),MULT_SCALE);
			
	for (unsigned char i = 0; i < x->f_Q; i++)
		new_output-=mult(*(x->f_a+i),*(x->f_output+i),MULT_SCALE);

	//Saturation for 12 bits
	if(new_output > SAT_VALUE)
		new_output = SAT_VALUE;	

	//Update mem
	for(unsigned char i = x->f_P; i >1 ; i--)
		*(x->f_input+i-1)=*(x->f_input+i-2);
	*x->f_input=new_input;

	for(unsigned char i = x->f_Q; i >1 ; i--)
		*(x->f_output+i-1)=*(x->f_output+i-2);
	*x->f_output=new_output;


	return new_output;
}
