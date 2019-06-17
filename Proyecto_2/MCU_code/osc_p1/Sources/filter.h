#ifndef FILTER_
#define FILTER_
#define MULT_SCALE 10000

//Filter API definition

//Filter datatype, holds relevat info about a filter instance properties. f_ stands for filter
typedef struct{
	unsigned char f_Q;	//Amount of past output values taken into account
	unsigned char f_P;	//Amount of past input values taken into account
	signed short* f_a; //Coefficients for past output values only
	signed short* f_b; //Coefficients for current and past input values
	signed short* f_output; //Contains  all PAST output values
	signed short* f_input;  //Contains  all PAST input values
} filter;


//Complementary functions
signed short mult(signed short a,signed short b,signed short n);


//Methods

//Init method
void init_filter(filter *x,unsigned char f_Q,unsigned char f_P,signed short *f_a,signed short *f_b,signed short *f_output,signed short *f_input);

//Evaluate filter output method
signed short eval_filter(filter *x,signed short new_input); //Calc a new output based on a new input



#endif
