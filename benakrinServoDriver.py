#ben.akrin.com/?p=9158
import RPi.GPIO as GPIO
import pigpio
import time

servo = 13

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)

print("0 degrees")
pwm.set_servo_pulsewidth(servo, 500);
time.sleep(3)

print("90 degrees")
pwm.set_servo_pulsewidth(servo, 1500);
time.sleep(3)

print("180 degrees")
pwm.set_servo_pulsewidth(servo, 2500);
time.sleep(3)

pwm.set_PWM_dutycycle(servo, 0)
pwm.set_PWM_frequency(servo, 0)