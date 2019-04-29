#include "filter.h"


//Methos implementation file
unsigned short eval_filter(unsigned short new_input){


	//Define new output variable
	unsigned short new_output=0;

	//Calc output
	new_output+=f_b[0]*new_input;
	for (unsigned char i = 0; i < f_P; i++)
		new_output+=f_b[i+1]*f_input[i];
			
	for (unsigned char i = 0; i < f_Q; i++)
		new_output-=f_a[i]*f_output[i];
		
	//Update mem
	for(unsigned char i = f_P-1; i >0 ; i--)
		f_input[i]=f_input[i-1];
	f_input[0]=new_input;

	for(unsigned char i = f_Q-1; i >0 ; i--)
		f_output[i]=f_output[i-1];
	f_output[0]=new_output;	


	return new_output;
}