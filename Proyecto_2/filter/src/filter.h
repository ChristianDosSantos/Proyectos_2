#ifndef FILTER_
#define FILTER_
#define MULT_SCALE 10000

//Filter API definition

//Filter datatype, holds relevat info about a filter instance properties. f_ stands for filter
typedef struct{
	unsigned char f_Q;	//Amount of past output values taken into account
	unsigned char f_P;	//Amount of past input values taken into account
	int* f_a; //Coefficients for past output values only
	int* f_b; //Coefficients for current and past input values
	int* f_output; //Contains  all PAST output values
	int* f_input;  //Contains  all PAST input values
} filter;


//Complementary functions
static inline signed short mult(int a,int b,int n); //Multiplies a and b, then the result is divided by n

//Methods

//Init method
void init_filter(filter *x,unsigned char f_Q,unsigned char f_P,int *f_a,int *f_b,int *f_output,int *f_input);

//Evaluate filter output method
signed short eval_filter(filter *x,int new_input); //Calc a new output based on a new input



#endif