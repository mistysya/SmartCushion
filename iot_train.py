import sys
import json
import requests
import datetime
import numpy as np

pose_table = {'test': 0}

class Train():
    def __init__(self, file_name):
        self.data = []
        self.file_name = file_name
        self.pose_name = file_name
        pass
    
    def run(self):
        self.load_data()
        print(self.data[0])
        for i in range(len(self.data)):
            print(self.data[i])
            self.send_sensor_data_to_platform(self.data[i])

    def send_sensor_data_to_platform(self, sensor_data):
        url = "https://iot.cht.com.tw/iot/v1"
        device_path = "/device/18351549814/rawdata"
        headers = {'CK':'PKVRB0L9OF0CMISRNT', 'device_id':'18351549814'}
        current_time = datetime.datetime.now().isoformat()
        iot_format_datas = []
        for index in range(len(sensor_data) - 1):
            data = {'id':'sensor_' + str(index + 1),
                    'time':current_time,
                    'value':[str(sensor_data[index])]}
            iot_format_datas.append(data)
        data = {'id':'pose',
                'time':current_time,
                'value':[str(sensor_data[-1])]}
        iot_format_datas.append(data)
        print(iot_format_datas)
        print()
        # r = requests.post(url + device_path, json=iot_format_datas, headers=headers)
        #print(r)
        #print(r.text)

    def load_data(self):
        file_path = sys.path[0] + '\\' + self.file_name + '.npy'
        data = np.load(file_path)
        self.data = data.astype(int)
        pass
    
    def delete_sensor_data(self):
        url = "https://iot.cht.com.tw/iot/v1"
        device_path = "/device/18351549814/rawdata"
        current_time = datetime.datetime.now().isoformat()
        for index in range(7):
            headers = {'CK':'PKVRB0L9OF0CMISRNT',
                       'device_id':'18351549814',
                       'sensor_id':'sensor_' + str(index + 1),
                       'start':'2019-08-25T23:55:00Z',
                       'end':current_time}
            r = requests.post(url + device_path, headers=headers)
        
        headers = {'CK':'PKVRB0L9OF0CMISRNT',
                    'device_id':'18351549814',
                    'sensor_id':[str(sensor_data[-1])],
                    'start':'2019-08-25T23:55:00Z',
                    'end':current_time}
        r = requests.post(url + device_path, headers=headers)

if __name__ == '__main__':
    pose_type = sys.argv[1]
    print(pose_type)
    train_data_upload = Train(pose_type)
    # train_data_upload.run()
    train_data_upload.delete_sensor_data()
