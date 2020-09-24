# !/usr/bin/env python
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import uuid
import boto3
import json
import picamera
import time

reader = SimpleMFRC522()
sns = boto3.client('sns')

def write_rfid_tag():
    try:
        firstname = input('Please enter your first name: ')
        lastname = input ('Please enter your last name: ')
        print("Now place your tag to write")
        tag_id = reader.write(str(uuid.uuid4()))
        userid = tag_id[1]
        print("Tag written")
        response = [userid, firstname, lastname]
        return response

    except:
        print("There was an error, please try running the script again")
        return

    finally:
        GPIO.cleanup()

def send_user_info_to_sns(userdata):

    message = json.dumps(
        {
            "userId": userdata[0],
            "firstName": userdata[1],
            "lastName": userdata[2]
        })
    sns.publish(
        TopicArn='arn:aws:sns:us-east-1:821383200340:access-project-WriteTag277B833F-16Q1WU28DM2OB',
        Message=message,
        Subject='Write event for {user}'.format(user=userdata[0])
    )

def take_picture():

    camera = picamera.PiCamera()
    print("Taking picture in 3 seconds")
    time.sleep(3)
    camera.rotation =180
    camera.capture('profilepic.jpg')

def upload_profile_photo(userdata):
    s3 = boto3.resource('s3', region_name='us-east-1')
    BUCKET = 'access-project-accessprojectbucketf5590f18-kgo5o74f0pcn'
    s3.Bucket(BUCKET).upload_file("profilepic.jpg", f"{userdata[0]}.jpg")

writeresponse = write_rfid_tag()
take_picture()
send_user_info_to_sns(writeresponse)
upload_profile_photo(writeresponse)