import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--org_images_train', type=str, default='../../datasets/hw3_dataset/org/train')
parser.add_argument('--org_images_val', type=str, default='../../datasets/hw3_dataset/org/val')
parser.add_argument('--org_json_train', type=str, default='../../datasets/hw3_dataset/org/train.coco.json')
parser.add_argument('--org_json_val', type=str, default='../../datasets/hw3_dataset/org/val.coco.json')
parser.add_argument('--name', type=str, default='hw3')
parser.add_argument('--epoch', type=int, default=3)
parser.add_argument('--weights', type=str, default='yolov5m6.pt')
args = parser.parse_args()

# Create train labels (COCO type) 
os.system(f'python programs/utils/json2txt.py \
          --input_json {args.org_json_train} \
          --output_dir ./programs/hw3_dataset/org/labels/train')

# Create val labels (COCO type) 
os.system(f'python programs/utils/json2txt.py \
          --input_json {args.org_json_val} \
          --output_dir ./programs/hw3_dataset/org/labels/val')

# Create train data yaml 
print('Create train data yaml')
os.system(f'python programs/utils/create_yaml.py \
        --train_data ./programs/hw3_dataset/org/images/train \
        --val_data ./programs/hw3_dataset/org/images/val \
        --output_yaml ./programs/ConfMix/data/hw3_data.yaml')

# Train source model
print('Train source model')
os.system(f'python programs/ConfMix/train.py \
          --name {args.name} \
          --weights {args.weights} \
          --batch 8 \
          --img 1280 \
          --epoch {args.epoch} \
          --data hw3_data.yaml \
          ')


