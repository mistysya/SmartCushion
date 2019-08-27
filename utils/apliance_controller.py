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


class AplianceController():
    def __init__(self):
        projectKey = 'PKMZ48ILXDPEXJN7R7'
        deviceId   = '18351487392'
        self.sensorId    = 'input'

        host = "iot.cht.com.tw"

        self.topic = '/v1/device/' + deviceId + '/rawdata'

        user, password = projectKey, projectKey

        self.client = mqtt.Client()
        self.client.username_pw_set(user, password)
        self.client.connect(host, 1883, 60)
        
        print('Apliance Controller Set')
    def lightOn(self):
        t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

        payload = [{"id":self.sensorId,"value":['1'], "time":t}]
        print('Light on :' + str(payload))
        self.client.publish(self.topic, "%s" % ( json.dumps(payload) ))
    def lightOff(self):
        t = str(time.strftime("%Y-%m-%dT%H:%M:%S"))

        payload = [{"id":self.sensorId,"value":['0'], "time":t}]
        print('Light on :' + str(payload))
        self.client.publish(self.topic, "%s" % ( json.dumps(payload) ))


if __name__ == '__main__':
    aplianceController = AplianceController()
    aplianceController.lightOn()
    time.sleep(2)
    aplianceController.lightOff()

