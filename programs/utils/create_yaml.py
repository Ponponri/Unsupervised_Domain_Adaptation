import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--train_data', type=str, default='#')
parser.add_argument('--val_data', type=str, default='#')
parser.add_argument('--test_data', type=str, default='#')
parser.add_argument('--uda_data', type=str, default='#')
parser.add_argument('--output_yaml', type=str, default='./my_data.yaml')
args = parser.parse_args()


class_str = '\n\nnc: 9 \nnames: [\'none\',\'person\',\'car\',\'truck\',\'bus\',\'rider\',\'motorcycle\',\'bicycle\',\'train\'] \n'


with open(args.output_yaml, 'w') as f:
    f.write('train:\n')
    if(args.train_data !='#'):
        train_datas = args.train_data.split(',| ')
        for train_data in train_datas:
            if(os.path.isabs(train_data) == True):
                f.write('  - '+train_data)
            else:
                f.write('  - ../../'+train_data)
            f.write('\n')
    f.write('\nval:\n')

    if(args.val_data !='#'):
        val_datas = args.val_data.split(',| ')
        for val_data in val_datas:
            if(os.path.isabs(val_data) == True):
                f.write('  - '+val_data)
            else:    
                f.write('  - ../../'+val_data)
            f.write('\n')

    f.write('\ntest:\n')
    if(args.test_data !='#'):
        test_datas = args.test_data.split(',| ')
        for test_data in test_datas:
            if(os.path.isabs(test_data) == True):
                f.write('  - '+test_data)
            else:
                f.write('  - ../../'+test_data)
            f.write('\n')

    f.write('\nuda:\n')
    if(args.uda_data !='#'):
        uda_datas = args.uda_data.split(',| ')
        for uda_data in uda_datas:
            if(os.path.isabs(uda_data) == True):
                f.write('  - '+uda_data)
            else:
                # f.write('  - ../../'+uda_data)
                f.write('  - '+uda_data)
            f.write('\n')

    f.write(class_str)