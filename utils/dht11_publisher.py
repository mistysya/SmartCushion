#!/usr/bin/python3
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
#|R|a|s|p|b|e|r|r|y|P|i|.|c|o|m|.|t|w|
#+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
# Copyright (c) 2019, raspberrypi.com.tw
# All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.
#
# cht_json_publish.py
# Publish sensor data to CHT IoT Platform via MQTT protocol
#
# Author : sosorry
# Date   : 2019/08/07

import paho.mqtt.client as mqtt
import numpy as np
import time
import json
import Adafruit_DHT
import configparser 

config = configparser.ConfigParser()
config.read('../cht.conf')
projectKey = config.get('device-key', 'projectKey')
deviceId   = config.get('device-key', 'deviceId')
dht11Id    = config.get('device-key', 'dht11Id')

host = "iot.cht.com.tw"

topic = '/v1/device/' + deviceId + '/rawdata'
print(topic)

user, password = projectKey, projectKey

client = mqtt.Client()
client.username_pw_set(user, password)
client.connect(host, 1883, 60)

for i in range(100):
    humidity, temperature = Adafruit_DHT.read_retry(11, 18)
    # humd = str(int(humidity))
    # temp = str(int(temperature))
    humd = int(humidity)
    temp = int(temperature)
    t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

    payload = [{"id":dht11Id,"value":[humd, temp], "time":t}]
    print(payload)
    client.publish(topic, "%s" % ( json.dumps(payload) ))
    time.sleep(1)

