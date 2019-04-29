#ifndef FILTER_
#define FILTER_
#define SAT_VALUE 4095
#define MULT_SCALE 100

//Filter API definition

//Variables for internal calculations. f_ stands for filter
extern unsigned char f_Q;	//Amount of past output values taken into account
extern unsigned char f_P;	//Amount of past input values taken into account
extern signed short f_a[]; //Coefficients for past output values only
extern signed short f_b[]; //Coefficients for current and past input values
extern signed short f_output[]; //Contains  all PAST output values
extern signed short f_input[];  //Contains  all PAST input values

//Complementary functions
signed short mult(signed short a,signed short b,signed short n); //Multiplies a and b, then the result is divided by n

//Methods
unsigned short eval_filter(unsigned short new_input); //Calc a new output based on a new input



#endif