import speech_recognition as sr
import os
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

## 2.5 = 0
## 7.5 = 90
## 12.5 = 180
doorOpened = 7.5
doorClosed = 2.5

servoPin = 12
ledPin = 33
bedroomPin = 35
kitchenPin = 38
GPIO.setup(servoPin, GPIO.OUT)
pwmServo = GPIO.PWM(servoPin, 50)
pwmServo.start(doorClosed)

GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(bedroomPin, GPIO.OUT)
GPIO.setup(kitchenPin, GPIO.OUT)

GPIO.output(ledPin, True)
GPIO.output(kitchenPin, False)
GPIO.output(bedroomPin, False)

r = sr.Recognizer()
##print(sr.Microphone.list_microphone_names())
##mic = sr.Microphone(device_index=2)

## r.adjust_for_ambient_noise(source)

try:
	while True:
		os.system('/usr/bin/arecord --duration=5 -r 16000 -f S16_LE /home/pi/Desktop/temp.wav')

		##with mic as source:
		##	audio = r.listen(source)

		temp = sr.AudioFile('/home/pi/Desktop/temp.wav')
		with temp as source:
			audio = r.record(source)
		
		text = ""
		try:
			text = r.recognize_google(audio)
		except sr.RequestError:
	        	text = "error"
		except sr.UnknownValueError:
	        	text = "error2"

		text = text.lower()

		print(text)
		understood = False

		if ('door' in text and 'open' in text):
			pwmServo.ChangeDutyCycle(doorOpened)
			understood = True

		if ('door' in text and 'close' in text):
			pwmServo.ChangeDutyCycle(doorClosed)
			understood = True

		if ('kitchen' in text):
			if ('on' in text):
				GPIO.output(kitchenPin, True)
				understood = True
				print('kit onnnnn')
			elif ('off' in text):
				GPIO.output(kitchenPin, False)
				understood = True
				print('kit offfff')

		if ('bedroom' in text):
			if ('on' in text):
				GPIO.output(bedroomPin, True)
				understood = True
			elif ('off' in text):
				GPIO.output(bedroomPin, False)
				understood = True

		if (understood == False and text != 'error2'):
			GPIO.output(ledPin, False)
			time.sleep(0.2)
			GPIO.output(ledPin, True)
			time.sleep(0.2)
			GPIO.output(ledPin, False)
			time.sleep(0.2)
			GPIO.output(ledPin, True)
			time.sleep(0.2)
			GPIO.output(ledPin, False)
			time.sleep(0.2)
			GPIO.output(ledPin, True)
			time.sleep(0.2)
			GPIO.output(ledPin, False)
			time.sleep(0.2)
			GPIO.output(ledPin, True)
			time.sleep(0.2)
		

except KeyboardInterrupt:
    pwmServo.stop()
    GPIO.cleanup()
