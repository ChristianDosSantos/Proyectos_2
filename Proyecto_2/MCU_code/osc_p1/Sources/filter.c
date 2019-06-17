#include "filter.h"

//Complementary functions
signed short  mult(signed short a,signed short b,signed short n){
	return (a*b)/n;
}

//---------------------------------------------------------

//Methods implementation
void init_filter(filter *x,unsigned char f_Q,unsigned char f_P,signed short *f_a,signed short *f_b,signed short *f_output,signed short *f_input){
	x->f_Q=f_Q;
	x->f_P=f_P;
	x->f_a=f_a;
	x->f_b=f_b;
	x->f_output=f_output;
	x->f_input=f_input;
}

signed short eval_filter(filter *x,signed short new_input){

	//Define new output variable
	signed short new_output=0;
	unsigned char i;

	//Calc output
	new_output+=mult(*x->f_b,new_input,MULT_SCALE);
	for (i = 0; i < x->f_P; i++)
		new_output+=mult(*(x->f_b+i+1),*(x->f_input+i),MULT_SCALE);
			
	for (i = 0; i < x->f_Q; i++)
		new_output-=mult(*(x->f_a+i),*(x->f_output+i),MULT_SCALE);

	//Update mem
	for(i = x->f_P; i >1 ; i--)
		*(x->f_input+i-1)=*(x->f_input+i-2);
	*x->f_input=new_input;

	for(i = x->f_Q; i >1 ; i--)
		*(x->f_output+i-1)=*(x->f_output+i-2);
	*x->f_output=new_output;

	if(new_output<0)
		new_output=0;

	return (unsigned short) new_output;
}
