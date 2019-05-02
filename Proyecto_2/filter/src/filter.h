#ifndef FILTER_
#define FILTER_
#define SAT_VALUE 4095
#define MULT_SCALE 100

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
signed short mult(signed short a,signed short b,signed short n); //Multiplies a and b, then the result is divided by n

//Init function
void init_filter(filter *x,unsigned char f_Q,unsigned char f_P,signed short *f_a,signed short *f_b,signed short *f_output,signed short *f_input);

//Methods
unsigned short eval_filter(filter *x,unsigned short new_input); //Calc a new output based on a new input



#endif