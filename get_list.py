import os

xml_path = './RoLabelImg_Transform/xml/'
txt_list_path = './RoLabelImg_Transform/xml_to_txt_list.txt'

dir_list = [dir for dir in os.listdir(xml_path) if dir.split('.')[1] == 'xml']

with open(txt_list_path, 'w') as fw:
    for dir in dir_list:
        fw.write(dir)
        fw.write('\n')


# txt_path = './RoLabelImg_Transform/txt/'
# txt_list_path = './RoLabelImg_Transform/txt_to_xml_list.txt'

# dir_list = [dir for dir in os.listdir(txt_path) if dir.split('.')[1] == 'txt']

# with open(txt_list_path, 'w') as fw:
#     for dir in dir_list:
#         fw.write(dir)
#         fw.write('\n')