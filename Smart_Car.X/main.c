/*
 * File:   main.c
 * Author: Silviu
 *
 * Created on March 22, 2019, 4:11 PM
 */


#include <xc.h>
#include <math.h>
#include <stdio.h>
#include "bit_config.h"
#include "config.h"
#include "pwm_config.h"
#include "usart_pic16.h"
#include <pic18f46k22.h>
#define ECO         PORTBbits.RB4
#define TRIG        LATBbits.LB3
#define DIR1        LATDbits.LD1
#define DIR2        LATDbits.LD2
#define BRAKE       LATDbits.LD0
#define BLUE        LATEbits.LE1
#define RED         LATEbits.LE2
#define YELLOW      LATEbits.LE0
#define QI          PORTAbits.RA6
#define THERMAL     PORTAbits.RA7
#define LEFT        CCPR1L
#define RIGHT       CCPR2L

void steering_angle(uint8_t received_angle);

char str_V[8],str_A[8];
float  rez_adc_A,tens_A,Ibat,rez_adc_U,Ubat,tens;
unsigned int cor,TMR,distanta;
unsigned long timp_us = 0;

void interrupt serial(void)
{
    //char str_V[8],str_A[8];// valoarea tensiunii si curentului
    //float i,j;

    if(RC1IF==1)//intrerupere seriala
    {
        RC1IF=0;// loop
        uint8_t angle_from_pi=0; 
        angle_from_pi=RCREG1;
        steering_angle(angle_from_pi);
     }              
}

void main(void) 
{
    config();
    pwm_config();
    adc_config();
    eusart_config();
    BRAKE=0;
    DIR1=1;
    DIR2=DIR1;
    RIGHT=LEFT=0;
    TMR1=TMR3=0;
    __delay_ms(100);

    while(1)
    {

   __delay_ms(1000);
        if(THERMAL==1)
        {
            RC1IF==1;
            RIGHT=LEFT=0;
            BRAKE=1;
        }
    }
    
 
}  
    
    




    
