/*
 * File:   pwm_config.c
 * Author: Silviu
 *
 * Created on March 22, 2019, 4:12 PM
 */


#include <xc.h>
#include "bit_config.h"
#include "config.h"
int c,dty_car;
float  rez_adc_A,tens_A,Ibat,rez_adc_U,Ubat,tens;

void left(int dty_car)
{
	if(dty_car>100)
    {
    dty_car=100;
    }
    
	c=dty_car*1.7; 
	CCPR2L=c;
    
    // valoarea din pwm si face o fct pt 100 putere maxima
    //left
	
}
void right(int dty_car)
{
	if(dty_car>100)
    {
    dty_car=100;
    }
    
	c=dty_car*1.7; 
	CCPR1L=c;  
	//right
}

  float read_Ibat(void)//citire curent de iesire
{
    ADCON0=0b00000011;//RA0
    __delay_ms(10);
    ADCON0bits.GO=1;
    __delay_ms(10);
    rez_adc_A=ADRESH;
    tens_A=rez_adc_A*0.012890625;// variabila in care salvez valoarea zecimala a curentuli
    Ibat=tens_A;
        if(Ibat>10)
    {
        __delay_ms(10);
        CCPR1L=0; // protectie la supracurent
        CCPR2L=0;
        while(1)
        {
            __delay_ms(100);
        }
    }
    return Ibat;
}
    
    float read_Ubat(void)//citire valoare tensinue de iesire
{
    ADCON0=0b00000111;//RA1
    __delay_ms(10);
    ADCON0bits.GO=1;
    __delay_ms(10);
    rez_adc_U=ADRESH;
    tens=rez_adc_U*0.012890625; 
    Ubat=tens/0.2;// z1/z1+z2*v1
    if(Ubat>16)
    {
        __delay_ms(10);
        CCPR1L=0;
        CCPR2L=0;
        while(1)
        {
  //protectie supra tensiune
        }
    }
     if(Ubat<10)
    {
        __delay_ms(10);
        CCPR1L=0;
        CCPR2L=0;
        while(1)
        {
  
        }//protectoe subalimentare(tensiune))
    }
    return Ubat;
}
