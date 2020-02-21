#include <xc.h>
#include "config.h"
#include <pic18f46k22.h>
#include "usart_pic16.h" 
#include "bit_config.h"

void config(void)
{
    TRISA=0X00;
    TRISB=0X00;
    TRISC=0X00;
    TRISD=0X00;
    TRISE=0Xff;
    
    PORTA=0X00;
    PORTB=0X00;
    PORTC=0X00;
    PORTD=0X00;
    PORTE=0X00;
     
    LATA=0X00;
    LATB=0X00;
    LATC=0X00;
    LATD=0X00;
    LATE=0X00;
    
    ANSELA=0X00;
    ANSELB=0X00;
    ANSELC=0X00;
    ANSELD=0X00;
    ANSELE=0X00;
    TRISDbits.TRISD5;
    TRISDbits.TRISD3;
    
    
    OSCCON=0b01110100;
    OSCTUNEbits.PLLEN=1;

}

void pwm_config(void)
{
    CCPTMRS0=0b00000000;
    CCP2CON=0b00001100; //RC2
    CCP1CON=0b00001100; //RC1
    T2CON=0b01111101;
    PR2=160;
    
    CCPR2L=128;
    CCPR1L=64;
    CCP3CON=0b00001100; //RB5
    CCPR3L=128;
    CCPR1L=0;
    CCPR2L=0;
    CCPR3L=0;

}

void adc_config(void)
{   TRISAbits.RA0=1;
    ANSELAbits.ANSA0=1;
    TRISAbits.RA1=1;
    ANSELAbits.ANSA1=1;
    

    ADCON0=0b00000011;  //RA0
    ADCON1=0b10000000;
    ADCON2=0b00111110;
    ADCON2bits.ADFM=0;

}

void eusart_config(void)
{
    USARTInit(19200);
    USART2Init(2400);
    USART2WriteString("USART initialized!");
    USART2GotoNewLine();
    INTCONbits.GIE=1;
    INTCONbits.PEIE=1;
    PIE3bits.RC2IE=1;
    PIE1bits.RCIE=1;
    

}

