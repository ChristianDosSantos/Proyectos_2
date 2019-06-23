/* ###################################################################
**     Filename    : main.c
**     Project     : osc_p1
**     Processor   : MC9S08QE128CLK
**     Version     : Driver 01.12
**     Compiler    : CodeWarrior HCS08 C Compiler
**     Date/Time   : 2017-02-13, 19:36, # CodeGen: 0
**     Abstract    :
**         Main module.
**         This module contains user's application code.
**     Settings    :
**     Contents    :
**         No public methods
**
** ###################################################################*/
/*!
** @file main.c
** @version 01.12
** @brief
**         Main module.
**         This module contains user's application code.
*/         
/*!
**  @addtogroup main_module main module documentation
**  @{
*/         
/* MODULE main */


/* Including needed modules to compile this module/procedure */
#include "Cpu.h"
#include "Events.h"
#include "AS1.h"
#include "AD1.h"
#include "TI1.h"
#include "Bit3.h"
#include "EInt1.h"
#include "EInt2.h"
#include "Bit1.h"
#include "Bit2.h"
#include "Bit4.h"
/* Include shared modules, which are used for whole project */
#include "PE_Types.h"
#include "PE_Error.h"
#include "PE_Const.h"
#include "IO_Map.h"
#include "functions.h"
#include "filter.h"

/* User includes (#include below this line is not maintained by Processor Expert) */

//Global variables
 volatile bool tick=0; //Timer flag
 
 //Channels data 
 unsigned short analogCh1;
 unsigned short analogCh2;
 unsigned long data=0;
 bool clk=0;
 
 //AS Com
 word Sent; //data block sent
 byte err; 
 
 //Filters
 filter fil1; //Instance
 unsigned char f_P1=10; 			 
 char f_b1[11]={2,3,7,12,17,18,17,12,7,3,2};   
 char f_input1[10]={0};     
   
 
 filter fil2; //Instance
 unsigned char f_P2=10; 			 
char f_b2[11]={2,3,7,12,17,18,17,12,7,3,2};   
char f_input2[10]={0};     
   
 
 //Filter enable
 bool filter_en=1;
 
 //Sleep mode enable
 bool sleep_mode_en=1;

void main(void)
{
  /* Write your local variable definition here */
 
	

  /*** Processor Expert internal initialization. DON'T REMOVE THIS CODE!!! ***/
  PE_low_level_init();
  /*** End of Processor Expert internal initialization.                    ***/

  /* Write your code here */
  
  //Enable stuff
  AS1_Enable(); //Serial com 
  TI1_Enable(); //Timer
  AD1_Enable(); // ADC
  
  //Filters init
  init_filter(&fil1,f_P1,f_b1,f_input1);
  init_filter(&fil2,f_P2,f_b2,f_input2);
  
  //Init sleep mode
  
    
  while(1){
	  	  
	  if(tick){
		  tick=0; //Reset flag
		  
		  //Read channels		  
		  AD1_MeasureChan(1,0);
		  AD1_GetChanValue(0,&analogCh1);
		  AD1_MeasureChan(1,1);
		  AD1_GetChanValue(1,&analogCh2);
		  		  
		  //Filter processing		  
		  if(filter_en){			  
			  analogCh1=eval_filter(&fil1,analogCh1);
			  analogCh2=eval_filter(&fil2,analogCh2);			  
		  }			  		  
		  //Set packet		  
		  make_packet(analogCh1,analogCh2,filter_en,sleep_mode_en,&data);		  
		  //Send data
		  do
			  err=AS1_SendBlock((byte*) &data,sizeof(data),&Sent);
		  while(err!=ERR_OK);	
		  
		  //Clock
		  Bit3_PutVal(clk);
		  clk= !clk;
		  
		  //Filter enable
		  filter_en=Bit2_GetVal() > 0;
		  
		  //Sleep mode
		  sleep_mode_en=Bit4_GetVal() > 0;
		  Bit1_PutVal(sleep_mode_en);
	  } 	  
	  	  
  }  
  
  /* For example: for(;;) { } */

  /*** Don't write any code pass this line, or it will be deleted during code generation. ***/
  /*** RTOS startup code. Macro PEX_RTOS_START is defined by the RTOS component. DON'T MODIFY THIS CODE!!! ***/
  #ifdef PEX_RTOS_START
    PEX_RTOS_START();                  /* Startup of the selected RTOS. Macro is defined by the RTOS component. */
  #endif
  /*** End of RTOS startup code.  ***/
  /*** Processor Expert end of main routine. DON'T MODIFY THIS CODE!!! ***/
  for(;;){}
  /*** Processor Expert end of main routine. DON'T WRITE CODE BELOW!!! ***/
} /*** End of main routine. DO NOT MODIFY THIS TEXT!!! ***/

/* END main */
/*!
** @}
*/
/*
** ###################################################################
**
**     This file was created by Processor Expert 10.3 [05.09]
**     for the Freescale HCS08 series of microcontrollers.
**
** ###################################################################
*/
