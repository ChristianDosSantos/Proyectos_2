#include <iostream>
#include <fstream>
using namespace std;

extern "C"{
	#include "filter.h"
}

//Variables for filter
filter fil; //Instance
unsigned char f_Q=3;             
unsigned char f_P=2; 			 
int f_a[3]={10000,   -19556,    9565};     
int f_b[3]={24,    48,    24};    
int f_output[3]={0}; 
int f_input[3]={0};  



int main(int argc, char * argv[]){

	int n=stoi(argv[1]); // sim time
	int input=10000; //input value

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
