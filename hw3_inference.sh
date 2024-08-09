input_dir=$1
output_json=$2

if [ "$3" = "0" ]
then
    echo "model source!"
    weights="./programs/weights/source.pt"
    img=1280
elif [ "$3" = "1" ]
then
    echo "model epoch10!"
    weights="./programs/weights/epoch10.pt"
    img=1280
elif [ "$3" = "2" ]
then
    echo "model epoch20!"
    weights="./programs/weights/epoch20.pt"
    img=1280
elif [ "$3" = "3" ]
then
    echo "model epoch29!"
    weights="./programs/weights/epoch29.pt"
    img=1280
elif [ "$3" = "4" ]
then
    echo "model best!"
    weights="./programs/weights/epoch29.pt"
    img=2000
else
    echo "Invalid input model!"
    weights="./programs/weights/epoch29.pt"
    img=1280
fi

python ./programs/utils/inference_sh.py --test_data $input_dir --output_json $output_json --weights $weights --img $img 