#!/usr/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import boto3
import json
import picamera
import time

reader = SimpleMFRC522()
sns = boto3.client('sns')

def read_rfid_tag():

        try:
                print('Place tag on RFID reader: ')
                tagid, userid = reader.read()
                print(f'Processing read event...')
                formatted_userid = userid.replace(" ", "")
                return formatted_userid
        finally:
                GPIO.cleanup()

def take_picture():

    camera = picamera.PiCamera()
    print("Taking picture in 5 seconds")
    time.sleep(5)
    camera.rotation=180
    camera.capture('example.jpg')

def upload_photo(userid):
    try:
        s3 = boto3.resource('s3', region_name='us-east-1')
        BUCKET = "rasberry-bucket"

        s3.Bucket(BUCKET).upload_file("example.jpg", f"{userid}-capture.jpg")

    except:
        print("Error processing login event, no user ID found on RFID tag.")
        return

user = read_rfid_tag()
take_picture()
upload_photo(user)