import sys
import json
import time
import operator
import numpy as np
import requests
import datetime
from collections import deque
from utils.sensor_data_collector import SensorDataCollector

class SmartCushion():
    def __init__(self):
        self.sensor_collector = SensorDataCollector()
        self.sitting_history = deque(maxlen=10)
        pass

    def run(self):
        self.sensor_datas = self.get_sensor_data()
        self.send_sensor_data_to_platform()
        self.sitting_result = self.get_sitting_result()
        self.sitting_history.append(self.sitting_result)
        print(self.sitting_result)
        self.send_sitting_result_to_web()
        '''
        if self.is_sitting_result_wrong(self.sitting_result):
            self.give_shock()
        self.user_condition_detect()
        '''
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
        print(r.text)

    def get_sitting_result(self):
        url = "https://iot.cht.com.tw/apis/CHTIoT"
        device_path = "/bigdata/v1/prediction/dr1bp0qn5"
        headers = {'X-API-KEY':'a42252b2-b8dc-4b74-aad1-a46efcbcbb24',
                   'accept':'application/json',
                   'Content-Type':'application/json'}
        send = {'features': self.sensor_datas}
        sitting_result = requests.post(url + device_path, headers=headers, json=send)
        result = sitting_result.json()
        return int(result['value'])

    def send_sitting_result_to_web(self):
        url = "https://iot.cht.com.tw/iot/v1"
        device_path = "/device/18359721596/rawdata"
        headers = {'CK':'PKVRB0L9OF0CMISRNT', 'device_id':'18359721596'}
        current_time = datetime.datetime.now().isoformat()
        data = {'id':'prediction',
                'time':current_time,
                'value':str(self.sitting_result)}
        r = requests.post(url + device_path, json=data, headers=headers)
        print(r)
        print(r.text)

    def is_sitting_result_wrong(self):
        appear_count = {}
        for i in range(6):
            appear_count[str(i)] = self.sitting_history.count(i)
        maximum = max(appear_count.items(), key=operator.itemgetter(1))[0]
        if appear_count[maximum] > 3:
            
        return True

    def give_shock(self):
        # call active_motor for seconds
        self.active_motor()
        pass

    def active_motor(self):
        pass

    def user_condition_detect(self):
        pass

    def control_iot_device(self):
        pass

    def receive_iot_message(self):
        pass

if __name__ == "__main__":
    cushion = SmartCushion()
    cushion.run()
    # r = cushion.get_sitting_result()
    # print(r)