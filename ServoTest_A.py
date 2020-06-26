#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time
 
servo = 13
 
# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth
 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
 
pwm.set_PWM_frequency( servo, 50 )

pls_w = 600
try:
    while pls_w < 2401:
        print( "pls_w: ", pls_w )
        pwm.set_servo_pulsewidth( servo, pls_w ) ;
        time.sleep( .025 )
        pls_w = pls_w + 10
        
    pwm.set_PWM_dutycycle(servo, 0)
    pwm.set_PWM_frequency( servo, 0 )        
        

except KeyboardInterrupt: 
# turning off servo
    pwm.set_PWM_dutycycle(servo, 0)
    pwm.set_PWM_frequency( servo, 0 )
