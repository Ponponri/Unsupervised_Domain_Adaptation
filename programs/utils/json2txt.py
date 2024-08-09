import json
import os
import argparse
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--input_json', type=str, default='../../datasets/hw3_dataset/org/train.cococ.json')
parser.add_argument('--output_dir', type=str, default='./programs/hw3_dataset/org/labels/train')
args = parser.parse_args()


with open(args.input_json, 'r') as f:
    str_json = f.read()

parsedjson = json.loads(str_json)

if(os.path.isdir(args.output_dir) == False):
    os.system(f'mkdir {args.output_dir}')

for j in range(len(parsedjson['images'])):
    file_name = parsedjson['images'][j]['file_name'].split('/')[-1][:-4] + '.txt'
    with open(os.path.join(args.output_dir,file_name), 'w') as f:
        height = parsedjson['images'][j]['height']
        width = parsedjson['images'][j]['width']
        image_id = parsedjson['images'][j]['id']
        #print(image_id)
        for k in range(len(parsedjson['annotations'])):
            if(image_id == parsedjson['annotations'][k]['image_id']):
                #print(parsedjson['annotations'][k])
                xx = parsedjson['annotations'][k]['bbox'][0] + int(parsedjson['annotations'][k]['bbox'][2] / 2)
                yy = parsedjson['annotations'][k]['bbox'][1] + int(parsedjson['annotations'][k]['bbox'][3] / 2)
                ww = parsedjson['annotations'][k]['bbox'][2]
                hh = parsedjson['annotations'][k]['bbox'][3]

                xx = round(xx / width, 5)
                yy = round(yy / height, 5)
                ww = round(ww / width, 5)
                hh = round(hh / height, 5)

                f.write(str(parsedjson['annotations'][k]['category_id']) + ' ')
                f.write(str(xx) + ' ' + str(yy) + ' ' + str(ww) + ' ' + str(hh) + '\n')
                
