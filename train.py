import sklearn
import sys
import json
import requests
import datetime
import numpy as np

from sklearn import cross_validation, ensemble, preprocessing, metrics

pose_table = {'normal': 0,
              'humpback': 1,
              'lie': 2,
              'right': 3,
              'left': 4,
              'one-third': 5}

class Train():
    def __init__(self, file_name):
        self.data = []
        self.file_name = file_name
        pass
    
    def run(self):
        self.load_data()

    def load_data(self):
        file_path = sys.path[0] + '\\' + self.file_name + '.npy'
        data = np.load(file_path)
        self.data = data.astype(int)

    def train(self):
        X = self.data[:,:-1]
        Y = self.data[:, -1]
        X_train, X_test, y_train, y_test = cross_validation.train_test_split(X, Y, test_size=0.3)

        # 建立 random forest 模型
        forest = ensemble.RandomForestClassifier(n_estimators = 100)
        forest_fit = forest.fit(X_train, y_train)

        # 預測
        y_test_predicted = forest.predict(X_test)

        # 績效
        accuracy = metrics.accuracy_score(y_test, y_test_predicted)
        print(accuracy)

if __name__ == '__main__':
    pose_type = sys.argv[1]
    print(pose_type)
    train_modle = Train(pose_type)
    train_modle.run()
    train_modle.train()
