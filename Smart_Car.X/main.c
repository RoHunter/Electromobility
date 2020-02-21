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

char str_V[8],str_A[8];
float  rez_adc_A,tens_A,Ibat,rez_adc_U,Ubat,tens;
unsigned int cor,TMR,distanta;
unsigned long timp_us = 0;

void interrupt serial(void)
{
        char str_V[8],str_A[8];// valoarea tensiunii si curentului
        float i,j;

        if (RC1IF==1)//intrerupere seriala
    {
        int flag=0;
        
        flag=RCREG1;
        
        switch(flag)
        {
            case 0x66://forward
                RIGHT=LEFT=60;
                DIR1=DIR2=1;
                BRAKE=0;
                break;
                
            case 0x53://stop
                RIGHT=LEFT=0;
                BRAKE=1;
                break;
                
            case 0x4c:// left
                RIGHT=80;
                LEFT= 30;
                BRAKE=0;
                break;
                
            case 0x52://right
                LEFT=80;
                RIGHT=20;
                BRAKE=0;
                break;  
                
            case 0x42://back
                RIGHT=LEFT=60;
                DIR1=DIR2=0;
                BRAKE=0;
                break; 
                
            case 0x49://rotatie A
                LEFT=70;
                RIGHT=70;
                BRAKE=0;
                 DIR1=1;
                 DIR2=0;
                break;
                
  
                
                case 0x7a://blue(b)
                RIGHT=LEFT=0;
                BRAKE=1;
                YELLOW=1;
                BLUE=1;
                RED=0;
                break;
                
                case 0x48://red(y)
                RIGHT=LEFT=0;
                BRAKE=1;
                YELLOW=1;
                RED=1;
                BLUE=0;
                break;
                
                case 0x61://a req current
                i=read_Ibat();  
                sprintf(str_A, "%.2f", i);
                USARTWriteString(str_A);
                break;
                
                case 0x76://v req tens
                j=read_Ubat();
                sprintf(str_V, "%.1f", j);
                USARTWriteString(str_V);
                break;
                
                case 0x6F://SENZOR US
                YELLOW=1;   
                break; 
                
                case 0x82://A fuel
                RIGHT=LEFT=0;
                BRAKE=1;
                __delay_ms(2000);
                RIGHT=LEFT=30;
                break; 
                
                case 0x81://B PC(trecere de pietoni)
                RIGHT=LEFT=0;
                BRAKE=1;
                __delay_ms(1000);
                RIGHT=LEFT=30;
                BRAKE=0;
                break; 
               
                case 0x80://C PARK
                 RIGHT=LEFT=0;
                BRAKE=1;
                __delay_ms(2000);
                while(1)
                {
                    __delay_ms(2000);   
                }
                break; 
                
                case 0x44://STOP
                RIGHT=LEFT=0;
                BRAKE=1;
                __delay_ms(3000);
                RIGHT=LEFT=30;
                break; 
                
                case 0x47://G
                    DIR1=1;
                    DIR2=0;
                RIGHT=LEFT=140;
                break; 
                
 
        }
    }
    RC1IF=0;// loop

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
    
    




    
