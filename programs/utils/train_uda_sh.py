import os 
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--org_image_train', type=str, default='../../datasets/hw3_dataset/org/train')
parser.add_argument('--fog_image_train', type=str, default='../../datasets/hw3_dataset/fog/train')
parser.add_argument('--fog_image_val', type=str, default='../../datasets/hw3_dataset/org/val')
parser.add_argument('--fog_json_val', type=str, default='../../datasets/hw3_dataset/fog/val.coco.json')
parser.add_argument('--name', type=str, default='hw3')
parser.add_argument('--epoch', type=int, default=3)
parser.add_argument('--weights', type=str, default='./programs/ConfMix/runs/train/hw3/weights/best.pt')
args = parser.parse_args()


# Create train data yaml 
print('Create train data yaml')
os.system(f'python programs/utils/create_yaml.py \
        --train_data ./programs/hw3_dataset/org/images/train \
        --val_data ./programs/hw3_dataset/fog/images/val \
        --uda_data ./programs/hw3_dataset/fog/images/train \
        --output_yaml ./programs/ConfMix/data/hw3_data_da.yaml')

# Create uda val labels (COCO type) 
os.system(f'python programs/utils/json2txt.py \
          --input_json {args.fog_json_val} \
          --output_dir ./programs/hw3_dataset/fog/labels/val')

# file_lists = os.listdir('./programs/ConfMix/runs/train')
file_lists = glob.glob('./programs/ConfMix/runs/train/hw3_org*')
print(file_lists)
file_lists.sort(key=lambda fn: os.path.getmtime(fn))

my_weight = os.path.join(file_lists[-1],'weights/last.pt')
print(my_weight)

# Inference uda train pseudo labels (COCO type) 
os.system(f'python programs/utils/detect_yolov5.py \
          --input_dir {args.fog_image_train} \
          --output_dir ./programs/hw3_dataset/fog/labels/train \
          --weights {my_weight}')

# Train source model
print('Train source model')
save_period = (int(args.epoch)+1)//3
if(save_period < 1):
    save_period = 1
save_period = str(save_period)

os.system(f'python programs/ConfMix/uda_train.py \
          --name {args.name} \
          --weights {my_weight} \
          --batch 4 \
          --img 1280 \
          --save-period {save_period} \
          --epoch {args.epoch} \
          --data hw3_data_da.yaml')


