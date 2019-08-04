import os

txt_path = '/RoLabelImg_Transform/txt'
img_path = '/RoLabelImg_Transform/img'
for i in range(len(os.listdir(txt_path))):
    img_dir = os.listdir(img_path)[i]
    txt_dir = os.listdir(txt_path)[i]
    if img_dir.split('.')[0] != txt_dir.split('.')[0]:
        source_path = os.path.join(txt_path,txt_dir)
        target_path = os.path.join(txt_path,img_dir.split('.')[0]+'.txt')    
        os.rename(source_path,target_path)