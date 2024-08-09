# CVPDL HW3 Train
## Target: Implement UDA method that train souce model with labeled souce dataset without fog, and then adapt model to unlabeled target dataset with fog.

# Environment 
- python 3.10
- pytorch 1.13.1
```
pip install -r requirements.txt
```

# Quick Start

## Training Example: 
- programs/example/cvpdl_hw3_train.ipynb (with training source dataset for 1 epoch and target dataset for 1 epoch).
## Command
```
bash hw3_train.sh $1 $2 $3 $4 $5 $6 $7
```

- S1: org_train_images_folder
- $2: org_val_images_folder
- $3: org_train_json_file
- $4: org_val_json_file
- $5: fog_train_images_folder
- $6: fog_val_images_folder
- $7: fog_val_json_file

## Results
- The training model on source domain would save at programs/ConfMix/runs/train/hw3_org{x0}, which x0 is the largest value in the folder or emtpy initially.  
- The training model on target domain would save at programs/ConfMix/runs/train/hw3_da{x1}, which x1 is the largest value in the folder or emtpy initially.

# Detail steps

1. Download Training Dataset

2. Change Folder Architecture To YOLOv5 Style
```
hw3_m11102137/
    programs/
        hw3_dataset/
            org/
                images/
                    train
                    val
                labels/
                    train
                    val
                train.coco.json
                val.coco.json
            fog/
                images/
                    train
                    val
                labels/
                    train
                    val
                val.coco.json 
```

3. Generate coco txt Labels From json Labels
```
python programs/utils/json2txt.py \
        --input_json {org_train_json_file} \
        --output_dir ./programs/hw3_dataset/org/labels/train
python programs/utils/json2txt.py \
        --input_json {org_val_json_file} \
        --output_dir ./programs/hw3_dataset/org/labels/val
python programs/utils/json2txt.py \
        --input_json {fog_val_json_file} \
        --output_dir ./programs/hw3_dataset/fog/labels/val
```

4. Create Source Train Data Yaml File 
```
python programs/utils/create_yaml.py \
        --train_data ./programs/hw3_dataset/org/images/train \
        --val_data ./programs/hw3_dataset/org/images/val \
        --output_yaml ./programs/ConfMix/data/hw3_data.yaml
```

5. Train Source Model
```
python programs/ConfMix/train.py \
        --name hw3_org \
        --batch 4 \
        --img 1280 \
        --epochs 160 \
        --data data/hw3_data.yaml \
        --weights yolov5m6.pt \
        --hyp hyp.scratch-high.yaml
```

6. Gererate Pseudo Labels
```
python programs/utils/detect_yolov5.py \
        --input_dir ./programs/hw3_dataset/fog/images/train \
        --output_dir ./programs/hw3_dataset/fog/labels/train \
        --weights ./programs/ConfMix/runs/train/hw3/weights/best.pt
```

7. Create UDA train Data Yaml File
```
python programs/utils/create_yaml.py \
        --train_data ./programs/hw3_dataset/org/images/train \
        --val_data ./programs/hw3_dataset/fog/images/val \
        --uda_data ./programs/hw3_dataset/fog/images/train \
        --output_yaml ./programs/ConfMix/data/hw3_data_da.yaml
```

8.  Train UDA Model
```
python programs/ConfMix/uda_train.py \
        --name hw3_da \
        --batch 4 \
        --img 1280 \
        --epochs 30 \
        --data data/hw3_data_da.yaml \
        --save-period 10 \
        --weights runs/train/hw3_org/weights/last.pt
```