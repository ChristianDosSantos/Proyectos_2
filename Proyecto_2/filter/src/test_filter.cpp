#include <iostream>
#include <fstream>
using namespace std;

extern "C"{
	#include "filter.h"
}

//Variables for filter
unsigned char f_Q=2;             
unsigned char f_P=2; 			 
unsigned short f_a[2]={1,2};     
unsigned short f_b[3]={1,5,2};    
unsigned short f_output[2]={1,0}; 
unsigned short f_input[2]={0,0};  


int main(int argc, char * argv[]){

	int n=stoi(argv[1]); // sim time
	unsigned short input=1; //input value

	//File creation
	ofstream file;
	file.open("test/filter.dat", ios::out | ios::trunc);

	for (int i = 0; i < n; i++){
		file << eval_filter(input);
		if(i<n-1)
			file << ",";
	}	

	return 0;
}
