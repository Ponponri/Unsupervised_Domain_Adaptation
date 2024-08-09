import torch
import cv2
import numpy as np
import os
import argparse
import json
from tqdm import tqdm

#handle json error
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

#inference image
def inference(filename):
	file = os.path.join(args.input_dir,filename)
	img0 = cv2.imread(file)
	h,w = img0.shape[:2]
	# Inference
	results = model(file)
	
	my_list = []
	for i in range(len(results.pandas().xyxy[0]['xmin'])):
		#print(results.pandas().xyxy[0])
		x1 = float(results.pandas().xyxy[0]['xmin'][i])
		y1 = float(results.pandas().xyxy[0]['ymin'][i])
		x2 = float(results.pandas().xyxy[0]['xmax'][i])
		y2 = float(results.pandas().xyxy[0]['ymax'][i])
		class_name = results.pandas().xyxy[0]['name'][i]
		# class_id = map_list[results.pandas().xyxy[0]['class'][i]]
		class_id = results.pandas().xyxy[0]['class'][i]
		confidence = float(results.pandas().xyxy[0]['confidence'][i])
		label = str(class_name) + ' ' + str(round(confidence,3))
		if(confidence >= 0.35):
			'''
			cv2.rectangle(img0,(x1,y1),(x2,y2),(255,255,255),1,cv2.LINE_AA)
			cv2.rectangle(img0,(x1,y1-20),(x2,y1),(255,255,255),cv2.FILLED)
			cv2.putText(img0,label,(x1,y1-5),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,0,0),1,cv2.LINE_AA)
			cv2.rectangle(img0,(int(x1),int(y1)),(int(x2),int(y2)),(255,255,255),1,cv2.LINE_AA)
			cv2.rectangle(img0,(int(x1),int(y1-2)),(int(x2),int(y1)),(255,255,255),cv2.FILLED)
			cv2.putText(img0,label,(int(x1),int(y1-7)),cv2.FONT_HERSHEY_SIMPLEX,0.5,(255,255,255),1,cv2.LINE_AA)
			'''
			my_list.append([filename,x1,y1,x2,y2,class_id,float(confidence),h,w])
	if(len(my_list) == 0):
		my_list.append([filename,-1])
	return img0, my_list

#get parameters
parser = argparse.ArgumentParser()
parser.add_argument('--input_dir', default = './programs/hw3_dataset/fog/images/train') 
parser.add_argument('--output_dir', default = './programs/hw3_dataset/fog')
parser.add_argument('--weights', default = './programs/ConfMix/runs/train/hw3/weights/best.pt')
args = parser.parse_args()

# Create output folder
if(os.path.isdir(args.output_dir) == False):
    os.system(f'mkdir {args.output_dir}')

#load model
try:
	model = torch.hub.load('programs/ConfMix', 'custom', path=args.weights, source = 'local')
except:
	model = torch.hub.load('../ConfMix', 'custom', path=args.weights, source = 'local')

#inference
print('start inference!')
all_list = []	
for filename in tqdm(os.listdir(args.input_dir)):
	# print(filename)
	if(filename[-4:] == '.jpg' or filename[-4:] == '.png'):
		img0, my_list = inference(filename)
		all_list.append(my_list)

#convert results to json file
json_dump = {}

for i in range(len(all_list)):
	file_name ='fog/val/'+all_list[i][0][0]
	class_id = []
	bbox = []
	confidence = []
	
	with open(os.path.join(args.output_dir,all_list[i][0][0][:-4]+'.txt'),'w') as f:
		for j in range(len(all_list[i])):
			if(all_list[i][j][1] == -1):
				continue 
			bbox.append([all_list[i][j][1],all_list[i][j][2],all_list[i][j][3],all_list[i][j][4]])
			class_id.append(all_list[i][j][5])
			confidence.append(all_list[i][j][6])
			cx=(all_list[i][j][1]+all_list[i][j][3])/(2*all_list[i][j][8])
			cy=(all_list[i][j][2]+all_list[i][j][4])/(2*all_list[i][j][7])
			ww=(all_list[i][j][3]-all_list[i][j][1])/all_list[i][j][8]
			hh=(all_list[i][j][4]-all_list[i][j][2])/all_list[i][j][7]
			f.write(f'{all_list[i][j][5]} {cx} {cy} {ww} {hh}\n')
	
	# for j in range(len(all_list[i])):
	# 	if(all_list[i][j][1] == -1):
	# 		continue 
	# 	bbox.append([all_list[i][j][1],all_list[i][j][2],all_list[i][j][3],all_list[i][j][4]])
	# 	class_id.append(all_list[i][j][5])
	# 	confidence.append(all_list[i][j][6])

# 	json_dump.update({file_name:{'boxes':bbox,'labels':class_id,'scores':confidence}})

# with open(os.path.join(args.output_dir,'uda_train.coco.json'),'w') as f:
# 	json.dump(json_dump,f,cls=NpEncoder,indent=2)
	
