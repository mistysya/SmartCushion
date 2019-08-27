import sys
import time
import numpy as np
import train
from utils.sensor_data_collector import SensorDataCollector

model = train.Train('train')
model.run()
model.train()

sensor_collector = SensorDataCollector()
sensor_data = sensor_collector.get_sensor_data()
sensor_data = [sensor_data]
y_test_predicted = model.forest.predict(sensor_data)
print(y_test_predicted)
