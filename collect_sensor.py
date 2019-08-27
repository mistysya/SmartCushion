import os
import sys
import time
import json
import numpy as np
from collections import deque

pose_table = {'test': 0}

class CollectSensorData():
    def __init__(self, file_name):
        self.file_name = file_name
        self.pose_type = pose_table[self.file_name]
        self.sensor_data = []
        self.history_data = np.zeros((1, 8))
        self.history_average_data = np.zeros((1, 8))
    
    def save(self):
        data = []
        file_path = sys.path[0] + '\\' + self.file_name + '.npy'
        if os.path.isfile(file_path):
            print("npy file exist.")
            data = np.load(file_path)
            data = np.vstack((data, self.history_average_data[1:,:]))
        else:
            print("npy file doesn't exist.")
            data = self.history_average_data[1:,:]
        np.save(file_path, data)
        np.savetxt(sys.path[0] + '\\' + self.file_name + '.txt', data, delimiter=',', fmt='%d') 

    def get_sensor_data(self):
        import random
        raw_data = []
        for _ in range(7):
            raw_data.append(random.randint(0,20000))
        raw_data.append(self.pose_type)
        self.sensor_data = raw_data
        print('Sensor : {0}'.format(raw_data))
        self.history_data = np.vstack((self.history_data, raw_data))
        return raw_data

    def remove_peak_value(self):
        pass

    def get_average_data(self):
        numpy_data = []
        numpy_data = self.history_data[-10:, :]
        average_data = np.mean(numpy_data, axis=0)
        average_data = average_data.astype(int)
        self.history_average_data = np.vstack((self.history_average_data, average_data))
        print('Average: {0}'.format(average_data))
        return average_data

if __name__ == "__main__":
    print('start')
    file_name = sys.argv[1]
    seconds = sys.argv[2]
    collector = CollectSensorData(file_name)
    for i in range(5, 0, -1):
        print('Collector will start in {0} seconds.'.format(str(i)))
        time.sleep(1)
    print()
    for i in range(10):
        collector.get_sensor_data()
        time.sleep(1)
    for i in range(int(seconds)):
        print()
        collector.get_sensor_data()
        collector.get_average_data()
        time.sleep(1)
    collector.save()
