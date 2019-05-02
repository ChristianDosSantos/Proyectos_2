#include <iostream>
#include <fstream>
using namespace std;

extern "C"{
	#include "filter.h"
}

//Variables for filter
filter fil; //Instance
unsigned char f_Q=1;             
unsigned char f_P=0; 			 
signed short f_a[1]={-97};     
signed short f_b[1]={24};    
signed short f_output[1]={0}; 
signed short f_input[0];  





int main(int argc, char * argv[]){

	int n=stoi(argv[1]); // sim time
	unsigned short input=10; //input value

	init_filter(&fil,f_Q,f_P,f_a,f_b,f_output,f_input);
	
	//File creation
	ofstream file;
	file.open("test/filter.dat", ios::out | ios::trunc);

	for (int i = 0; i < n; i++){
		file << eval_filter(&fil,input);
		if(i<n-1)
			file << ",";
	}
	


	return 0;
}
