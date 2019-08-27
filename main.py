import sys
import json
import time
import train
import operator
import numpy as np
import requests
import datetime
from collections import deque
from utils.sensor_data_collector import SensorDataCollector
from utils.apliance_controller import AplianceController
from utils.motor import Motor

class SmartCushion():
    def __init__(self):
        self.sensor_collector = SensorDataCollector()
        self.apliance_controller = AplianceController()
        self.sitting_history = deque(maxlen=10)
        self.motor = Motor()
        self.leave = True
        self.come = False
        self.sit_time = 0
        self.sleeping_time = 2
        self.exercise_time = 60
        self.model = train.Train('train')
        self.model.run()
        print("Start train model!")
        self.model.train()
        print("Train model completely!")
        pass

    def run(self):
        print("---start---")
        self.sensor_datas = self.get_sensor_data()
        self.send_sensor_data_to_platform()
        if self.detect_no_body():
            self.sitting_result = 6
        else:
            self.sitting_result = self.get_sitting_result()
        self.sitting_history.append(self.sitting_result)
        print(self.sitting_result)
        if self.is_sitting_result_wrong():
            self.give_shock()
        user_condition = self.user_condition_detect()
        if user_condition == 1:
            # turn off light
            self.control_iot_device(1)
        elif user_condition == 2:
            # turn on light
            self.control_iot_device(2)
        elif user_condition == 3:
            # vibration
            for _ in range(3):
                self.active_motor(1)
                time.sleep(1)
            self.sit_time = 0
        else:
            pass
        time.sleep(self.sleeping_time)
        pass

    def get_sensor_data(self):
        sensor_data = self.sensor_collector.get_sensor_data()
        print('Sensor : {0}'.format(sensor_data))
        return sensor_data

    def send_sensor_data_to_platform(self):
        url = "https://iot.cht.com.tw/iot/v1"
        device_path = "/device/18341781264/rawdata"
        headers = {'CK':'PKVRB0L9OF0CMISRNT', 'device_id':'18341781264'}
        current_time = datetime.datetime.now().isoformat()
        iot_format_datas = []
        for index in range(len(self.sensor_datas)):
            data = {'id':'sensor_' + str(index + 1),
                    'time':current_time,
                    'value':[str(self.sensor_datas[index])]}
            iot_format_datas.append(data)
        r = requests.post(url + device_path, json=iot_format_datas, headers=headers)
        print(r)

    def get_sitting_result(self):
        url = "https://iot.cht.com.tw/apis/CHTIoT"
        device_path = "/bigdata/v1/prediction/8i8gk7t7c"
        headers = {'X-API-KEY':'a42252b2-b8dc-4b74-aad1-a46efcbcbb24',
                   'accept':'application/json',
                   'Content-Type':'application/json'}
        send = {'features': self.sensor_datas}
        sitting_result = requests.post(url + device_path, headers=headers, json=send)
        result = sitting_result.json()
        print('Predict from IoT platform:', result['value'])
        result_local = self.model.forest.predict([self.sensor_datas])
        print('Predict from Local:', result_local)
        if int(result_local) != int(result['value']):
            print("IoT & Local are different!!!")
        # return int(result['value'])
        return int(result_local)

    def send_sitting_result_to_web(self, result):
        url = "https://iot.cht.com.tw/iot/v1"
        device_path = "/device/18359721596/rawdata"
        headers = {'CK':'PKVRB0L9OF0CMISRNT', 'device_id':'18359721596'}
        current_time = datetime.datetime.now().isoformat()
        data = {'id':'prediction',
                'time':current_time,
                'value':[result]}
        d = []
        d.append(data)
        r = requests.post(url + device_path, json=d, headers=headers)
        print(r)
        print(r.text)

    def is_sitting_result_wrong(self):
        appear_count = {}
        for i in range(6):
            appear_count[str(i)] = self.sitting_history.count(i)
        maximum = max(appear_count.items(), key=operator.itemgetter(1))[0]
        if appear_count[maximum] > 3:
            self.send_sitting_result_to_web(maximum)
            print("Now pose:", maximum)
            if maximum != '0':
                return True
        else:
            print("Can't detect now pose!!")
        return False

    def give_shock(self):
        self.active_motor(2)
        pass

    def active_motor(self, seconds):
        self.motor.active(seconds)
        pass

    def detect_no_body(self):
        data = 0
        for i in self.sensor_datas:
            if i < 2000:
                data += 0
            else:
                data += i
        if data == 0:
            return True
        else:
            return False

    def user_condition_detect(self):
        # 1: user leave
        # 2: user come
        # 3: user long sit
        history = list(self.sitting_history)

        print('History', history)
        no_body = history[6:]
        print(no_body.count(6))
        if no_body.count(6) == 3 and no_body.count(6) < 4 and self.come == True:
            self.sit_time = 0
            self.leave = True
            self.come = False
            return 1
        elif no_body.count(6) > 0 and no_body.count(6) <= 1 and self.leave == True:
            self.sit_time = 0
            self.come = True
            self.leave = False
            return 2
        else:
            self.sit_time += self.sleeping_time
        if self.sit_time > self.exercise_time:
            return 3
        return 0

    def control_iot_device(self, condition):
        # turn off light
        if condition == 1:
            self.apliance_controller.lightOff()
            pass
        # turn on light
        elif condition == 2:
            self.apliance_controller.lightOn()
            pass
        else:
            pass


if __name__ == "__main__":
    cushion = SmartCushion()
    while True:
        cushion.run()
    # r = cushion.get_sitting_result()
    # print(r)
