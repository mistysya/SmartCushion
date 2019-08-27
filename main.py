import json
import time
import requests
import datetime

class SmartCushion():
    def __init__(self):
        pass

    def run(self):
        self.sensor_datas = self.get_sensor_data()
        self.send_sensor_data_to_platform()
        '''
        self.sitting_result = self.get_sitting_result()
        # self.send_sitting_result_to_web(sitting_result)
        if self.is_sitting_result_wrong(self.sitting_result):
            self.give_shock()
        self.user_condition_detect()
        '''
        pass

    def get_sensor_data(self):
        # for test
        import random
        sensor_data = []
        for _ in range(8):
            sensor_data.append(random.randint(0,20000))
        print(sensor_data)
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
        device_path = "/bigdata/v1/prediction/modelID"
        params = {'modelId':'string', 'X-API-KEY':'string'}
        # get latest 30 data from sensor_data
        # remove peak data
        # get average of latest 20 data
        data = {'feeatures': []}
        sitting_result = requests.get(url + device_path, params=params, data=data)
        return sitting_result

    # try to use subscription
    # def send_sitting_result_to_web(self):
    #     pass

    def is_sitting_result_wrong(self, sitting_result):
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