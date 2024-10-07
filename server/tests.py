from django.test import TestCase
# Create your tests here.
import pickle
import csv
import os
import numpy as np
DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# testfilename =  open(DIR+'/server/static/server/model/testmodel.csv', 'r')
# testfile = csv.DictReader(testfilename)
# frequencytest = []
# robustnesstest = []
# testLabel = []
# for col in testfile:
#     frequencytest.append(float(col['Frequency']))
#     robustnesstest.append(float(col['Robustness']))
#     testLabel.append(int(col['Label']))
# testData = np.column_stack((frequencytest,robustnesstest))

# loaded_model = pickle.load(open('server\knnfacemodel.pkl', 'rb'))
# result = list(loaded_model.predict(testData))
# print(testLabel)
# print(result)
class Client:
    def __init__(self, username):
        self.stress_range = [username]
        self.points = [username]
    
    def get(self):
        return {
            'stress_range':self.stress_range,
            'points':self.points}
    
    def clear(self):
        self.stress_range = []
        self.points = []
    

scope_user = {}   
    
def abc():
    if 'giabao' not in scope_user:
        scope_user['giabao'] = Client('a')
        scope_user['hung'] = Client('b')
        scope_user['giabao'].points.append(5)
    return scope_user['giabao'].get()
def cde():
    return scope_user['giabao'].points
abc()
print(cde())
print(scope_user)
del scope_user['hung']
print(scope_user)
scope_user['giabao'].clear()
scope_user['giabao'].points = 6
print(scope_user['giabao'].points)
# a = {}

# a['test'] = [4,5,6]
# print(a['test'][0])
# import os

# from pathlib import Path
# BASE_DIR = Path(__file__).resolve().parent.parent
# DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE = os.path.join(BASE_DIR, 'server\static')
print(os.path.isfile(DIR+'/server/static/server/model/testmdel.csv'))
# for i in range(0,8):
#     if (os.path.isfile(DIR+'/server/static/server/data/{}_{}.csv'.format('giabao07', i)) == False):
#         with open(DIR+'/server/static/server/data/{}_{}.csv'.format('giabao07', i), 'w', newline='') as f:
#             writer = csv.writer(f)
#             writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
#             f.close()
row = {"Frame":3, "Value":4}
# f = open(DIR+'/server/static/server/data/0.csv', 'a', newline='')
# for i in range(0,10):
#     writer = csv.DictWriter(f, fieldnames=row.keys())
#     writer.writerow(row)