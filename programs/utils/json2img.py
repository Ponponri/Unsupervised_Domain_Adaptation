import os
import cv2
import json

path = '../datasets/hw1_data/test/'

with open('test_results_detr.json','r') as f:
	json_load = json.load(f)

for k,v in json_load.items():
	img = path + k
	print(k)
