import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)

class ServoController:
    def __init__(self, servo_pin=18):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        self.servo_pin = servo_pin
        GPIO.setup(self.servo_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_pin, 50)  # 50Hz PWM
        self.pwm.start(0)

        self.lock = threading.Lock()

    def set_angle(self, angle):
        duty = self.angle_to_duty_cycle(angle)
        GPIO.output(self.servo_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        time.sleep(0.5)
        GPIO.output(self.servo_pin, False)
        self.pwm.ChangeDutyCycle(0)

    def angle_to_duty_cycle(self, angle):
        duty_cycle = (angle + 90) / 18 + 2.5
        return duty_cycle

    def move_to_variety(self, variety):
        with self.lock:
            if variety == "Criollo":
                print("[Servo] Moving to 0° (Criollo)")
                self.set_angle(0)
                time.sleep(5)
            elif variety == "Forastero":
                print("[Servo] Moving to +90° (Forastero)")
                self.set_angle(90)
                time.sleep(5)
                self.set_angle(0)
            elif variety == "Trinitario":
                print("[Servo] Moving to -90° (Trinitario)")
                self.set_angle(-90)
                time.sleep(5)
                self.set_angle(0)
            else:
                print("[Servo] Unknown variety - no movement.")

    def cleanup(self):
        self.pwm.stop()
        GPIO.cleanup()
