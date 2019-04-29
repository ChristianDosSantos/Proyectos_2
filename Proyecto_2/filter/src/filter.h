#ifndef FILTER_
#define FILTER_

//Filter API definition

//Variables for internal calculations. f_ stands for filter
extern unsigned char f_Q;	//Amount of past output values taken into account
extern unsigned char f_P;	//Amount of past input values taken into account
extern unsigned short f_a[]; //Coefficients for past output values only
extern unsigned short f_b[]; //Coefficients for current and past input values
extern unsigned short f_output[]; //Contains  all PAST output values
extern unsigned short f_input[];  //Contains  all PAST input values

//Methods
unsigned short eval_filter(unsigned short new_input); //Calc a new output based on a new input


#endif