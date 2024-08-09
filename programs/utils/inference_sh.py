import os 
import glob
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--test_data', type=str, default='../../datasets/hw3_dataset/fog/public_test')
parser.add_argument('--output_yaml', type=str, default='./my_data.yaml')
parser.add_argument('--output_json', type=str, default='./pred.json')
parser.add_argument('--img', type=int, default=1280)
parser.add_argument('--weights', type=str, default='./programs/weights/epoch29.pt')
args = parser.parse_args()

# Glob
# rootdir = args.test_data
# dir_list = ''
# for path in glob.glob(f'{rootdir}/*/', recursive=True):
#     dir_list += (path+',')
# print(f'dir_list:{dir_list}')

# Create test data yaml 
print('Create test data yaml')
os.system(f'python programs/utils/create_yaml.py \
          --test_data {args.test_data} \
          --output_yaml ./programs/ConfMix/data/test_data.yaml')

# Inference test data
print('Inference test data')
os.system('cd')
os.system(f'python programs/ConfMix/uda_detect.py \
          --task test \
          --weights ./programs/weights/epoch29.pt \
          --batch 1 --img {args.img} --weights {args.weights} \
          --data test_data.yaml \
          --output_json {args.output_json} \
          ')


