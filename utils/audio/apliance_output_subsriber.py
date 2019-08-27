#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2019, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# cht_json_subscribe.py
# Subscribe topic from CHT IoT Platform via MQTT protocol
#
# Author : sosorry
# Date   : 2019/08/07
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import configparser 
import json
import os
import time

channels = 4

config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'audioDeviceId')
audioSensorId    = config.get('device-key', 'audioOutputSensorId')

host = "iot.cht.com.tw"
topic = '/v1/device/' + deviceId + '/sensor/' + audioSensorId + '/rawdata'

def on_connect(client, userdata, flags, rc):
    print("Audio connected with result code: {}".format(str(rc)))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    json_array = json.loads(str(msg.payload)[2:-1])
    print(json_array['value'])
    if json_array['value'][0] == '1':
        print('Washing machine done')
        os.system('aplay washing.wav')
        GPIO.output(channels, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(channels, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(channels, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(channels, GPIO.LOW)
        print("Stop vibration")

GPIO.setmode(GPIO.BCM)

GPIO.setup(channels, GPIO.OUT)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

user, password = projectKey, projectKey
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

client.loop_forever()

