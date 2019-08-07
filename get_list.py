import os
import argparse


parser = argparse.ArgumentParser(description="DeepLab-ResNet Network")
parser.add_argument("--model", type=str, default='txt_to_xml', help="")
parser.add_argument("--input_path", type=str, default='./RoLabelImg_Transform/txt/', help="")
args = parser.parse_args()


if args.model == 'txt_to_xml':
    txt_path = args.input_path
    txt_list_path = './RoLabelImg_Transform/{}_list.txt'.format(args.model)

    dir_list = [dir for dir in os.listdir(txt_path) if dir.split('.')[1] == 'txt']

    with open(txt_list_path, 'w') as fw:
        for dir in dir_list:
            fw.write(dir)
            fw.write('\n')

elif args.model == 'xml_to_txt':
    xml_path = args.input_path
    txt_list_path = './RoLabelImg_Transform/{}_list.txt'.format(args.model)

    dir_list = [dir for dir in os.listdir(xml_path) if dir.split('.')[1] == 'xml']

    with open(txt_list_path, 'w') as fw:
        for dir in dir_list:
            fw.write(dir)
            fw.write('\n')

else:
    raise ValueError("model only txt_to_xml and xml_to_txt")

