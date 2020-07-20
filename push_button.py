import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
import picamera

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 17 to be an input pin and set initial value to be pulled low (off)

while True: # Run forever
    if GPIO.input(17) == GPIO.HIGH:
        print("Button was pushed!")
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480)
            camera.start_preview()
            # Camera warm-up time
            time.sleep(2)
            camera.capture('foo.jpg')