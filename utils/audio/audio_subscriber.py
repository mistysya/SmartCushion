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

import paho.mqtt.client as mqtt
import configparser 
import json

config = configparser.ConfigParser()
config.read('cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
sensorId    = config.get('device-key', 'sensorId')

host = "iot.cht.com.tw"
topic = '/v1/device/' + deviceId + '/sensor/' + sensorId + '/rawdata'

def on_connect(client, userdata, flags, rc):
    print("Audio connected with result code: {}".format(str(rc)))
    client.subscribe(topic)

def on_message(client, userdata, msg):
#    print(msg.payload)
    json_array = json.loads(str(msg.payload)[2:-1])
#    print(json_array['value'])
    if json_array['value'][0] == '0':
        print('Close')
    elif json_array['value'][0] == '1':
        print('Open')
    else:
        print('[ERROR]' + jsson_array['value'][0])

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

user, password = projectKey, projectKey
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

client.loop_forever()

