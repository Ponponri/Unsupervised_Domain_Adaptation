# CVPDL HW3
## Target: Implement UDA method that train souce model with labeled souce dataset without fog, and then adapt model to unlabeled target dataset with fog.

# Environment 
- python 3.10
- pytorch 1.13.1
```
pip install -r requirements.txt
```

# Quick Start

## Inference Example: 
- programs/example/cvpdl_hw3_inference.ipynb 
## Download Checkpoints:
```
bash hw3_download.sh
```
## Inference:
```
bash hw3_inference.sh $1 $2 $3
```
- S1: input image folder
- $2: output json result
- $3: select model 

        0: source.pt
        1: epoch10.pt
        2: epoch20.pt
        3: epoch29.pt
        4: best result model
## Results
- The result json file would save at $2

# Detail

1. Change the test data path in test_data.yaml to target folder

2. Inference
```
python programs/ConfMix/uda_detect.py \
          --task test \
          --weights ./programs/weights/epoch29.pt \
          --batch 1 \
          --img 1280 \
          --weights runs/train/hw3_da/weights/last.pt \
          --data test_data.yaml \
          --output_json ./pred.json
```
