#include "filter.h"

//Complementary functions
char mult(char a,char b,char n){
	return (a*b)/n;
}


//---------------------------------------------------------

//Methods implementation
void init_filter(filter *x,unsigned char f_P,char *f_b,char *f_input){
	x->f_P=f_P;	
	x->f_b=f_b;
	x->f_input=f_input;
}

int  eval_filter(filter *x,unsigned short new){

	//Define new output variable
	char new_input= (char) new;
	char new_output=0;
	unsigned char i;

	//Calc output
	new_output+=mult(*(x->f_b),new_input,MULT_SCALE);
	for (i = 0; i < x->f_P; i++)
		new_output+=mult(*((x->f_b)+i+1),*((x->f_input)+i),MULT_SCALE);
			
	//Update mem
	for(i = x->f_P; i >1 ; i--)
		*((x->f_input)+i-1)=*((x->f_input)+i-2);
	*x->f_input=new_input;


	if(new_output<0)
		new_output=0;
	
		

	return   new_output;
}
