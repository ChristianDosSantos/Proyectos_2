#include <iostream>
using namespace std;

extern "C"{
	#include "filter.h"
}

//Variables for filter
unsigned char f_Q=2;             
unsigned char f_P=2; 			 
unsigned short f_a[2]={0,0};     
unsigned short f_b[3]={1,1,1};    
unsigned short f_output[2]={1,0}; 
unsigned short f_input[2]={0,0};  




int main(){

	int n=10;
	unsigned short input=1;
	for (int i = 0; i < n; i++){
	

		cout << "Filter output: " << eval_filter(input) << "\n";	

	}

	return 0;
}
