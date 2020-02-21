import serial
import time

directie_old=b''
inainte=b'f'
stanga=b'l'
dreapta=b'r'
sstanga=b'L'
ddreapta=b'R'
stop=b's'
detectat_fuel=b'a'
detectat_crosswalk=b'b'
detectat_park=b'c'
detectat_stop=b'd'
               
ser = serial.Serial(            
    port='/dev/serial0',
    baudrate = 19200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    
)


def trimite_serial(directie):
        global ser, directie_old
       # print(b'trimite serial')
        if directie is not  directie_old:
                ser.write(b'directie')
               # print(directie)
                directie_old = directie
