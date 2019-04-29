#include "filter.h"


//Complementary functions
signed short  mult(signed short a,signed short b,signed short n){
	return (a*b)/n;
}

//---------------------------------------------------------

//Methos implementation file
unsigned short eval_filter(unsigned short new_input){


	//Define new output variable
	unsigned short new_output=0;

	//Calc output
	new_output+=mult(f_b[0],new_input,MULT_SCALE);
	for (unsigned char i = 0; i < f_P; i++)
		new_output+=mult(f_b[i+1],f_input[i],MULT_SCALE);
			
	for (unsigned char i = 0; i < f_Q; i++)
		new_output-=mult(f_a[i],f_output[i],MULT_SCALE);

	//Saturation for 12 bits
	if(new_output > SAT_VALUE)
		new_output = SAT_VALUE;	

	//Update mem
	for(unsigned char i = f_P-1; i >0 ; i--)
		f_input[i]=f_input[i-1];
	f_input[0]=new_input;

	for(unsigned char i = f_Q-1; i >0 ; i--)
		f_output[i]=f_output[i-1];
	f_output[0]=new_output;


	return new_output;
}