/*
 * File:   pwm_config.c
 * Author: Silviu
 *
 * Created on March 22, 2019, 4:12 PM
 */


#include <xc.h>
#include "bit_config.h"
#include "config.h"
#include "stdint.h"
#include "pwm_config.h"

#define servo_to_diff 55

void steering(uint8_t dty_left, uint8_t dty_right);


float  rez_adc_A,tens_A,Ibat,rez_adc_U,Ubat,tens;

void steering(uint8_t dty_left, uint8_t dty_right)
{
    uint8_t buffer;
	if(dty_left>100)
    {
        dty_left=100;
    }
       
    if(dty_right > 100)
    {
        dty_right=100;
    }
       

	buffer=dty_left*1.7; 
	CCPR1L=buffer/2;  
    buffer = dty_right*1.7;
	CCPR2L=buffer/2;  
    
    // valoarea din pwm si face o fct pt 100 putere maxima
    //left
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
    void steering_angle(uint8_t received_angle)
    {
        uint8_t my_angle_a = 0;
        uint8_t my_angle_b = 0;
        my_angle_a = (received_angle * servo_to_diff)/100;
        my_angle_b = 100 - my_angle_a;
        steering(my_angle_a, my_angle_b);
    }