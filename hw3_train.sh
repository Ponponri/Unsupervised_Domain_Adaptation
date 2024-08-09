org_train_images=$1
org_val_images=$2
org_train_json=$3
org_val_json=$4
fog_train_images=$5
fog_val_images=$6
fog_val_json=$7

echo "Create folders"
mkdir -p ./programs/hw3_dataset/org/images/train
mkdir -p ./programs/hw3_dataset/org/images/val

mkdir -p ./programs/hw3_dataset/org/labels/train
mkdir -p ./programs/hw3_dataset/org/labels/val

mkdir -p ./programs/hw3_dataset/fog/images/train
mkdir -p ./programs/hw3_dataset/fog/images/val

mkdir -p ./programs/hw3_dataset/fog/labels/train
mkdir -p ./programs/hw3_dataset/fog/labels/val

echo "Copy images to folders"
echo "Copy org images"
cp  ${org_train_images}/* ./programs/hw3_dataset/org/images/train
cp  ${org_val_images}/*   ./programs/hw3_dataset/org/images/val
echo "Copy fog images"
cp  ${fog_train_images}/* ./programs/hw3_dataset/fog/images/train
cp  ${fog_val_images}/*   ./programs/hw3_dataset/fog/images/val
echo "Copy json files"
cp  $org_train_json   ./programs/hw3_dataset/org/train.coco.json
cp  $org_val_json     ./programs/hw3_dataset/org/val.coco.json
cp  $fog_val_json     ./programs/hw3_dataset/fog/val.coco.json


echo "Train Source Data"
python ./programs/utils/train_org_sh.py \
        --name "hw3_org" \
        --org_images_train ./programs/hw3_dataset/org/images/train \
        --org_images_val ./programs/hw3_dataset/org/images/val \
        --org_json_train ./programs/hw3_dataset/org/train.coco.json \
        --org_json_val ./programs/hw3_dataset/org/val.coco.json \
        --epoch 160

echo "Train Target Data"
python ./programs/utils/train_uda_sh.py \
        --name "hw3_da" \
        --org_image_train ./programs/hw3_dataset/org/images/train \
        --fog_image_train ./programs/hw3_dataset/fog/images/train \
        --fog_image_val ./programs/hw3_dataset/fog/images/val \
        --fog_json_val ./programs/hw3_dataset/fog/val.coco.json \
        --epoch 30

echo "Done"