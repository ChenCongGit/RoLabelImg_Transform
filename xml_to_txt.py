#coding:utf-8 

"""
每一张图片的label信息保存在一个文本文件中，每一行记录一个旋转bndbox信息
<object>
    <type>robndbox</type>
    <name>wenben</name>
    <pose>Unspecified</pose>
    <truncated>0</truncated>
    <difficult>0</difficult>
    <robndbox>
        <cx>860.5666</cx>
        <cy>734.5734</cy>
        <w>644.8657</w>
        <h>52.3775</h>
        <angle>3.031593</angle>
    </robndbox>
</object>
其中cx, cy表示bndbox的中心点坐标(坐标系方向左上角为原点，向右为x正方向，向下为y正方向);
h和w是字符块的高和宽;
angle是旋转角度信息，这里得注意，roLabelImg标注得到的旋转角度值规则：首先是画一个水平bndbox,
此时的angle=0，如果你往顺时针方向旋转，得到的角度值是一个弧度单位的正值。按照这种思路，如果往逆时针方向旋转,
得到的角度值应该是一个弧度单位的负值，但实际并不是这样，比如上面的例子，实际角度应该是往逆时针方向旋转了一小点,
但得到的角度值=3.081593，也是正值,假设规定往逆时针方向旋转时角度为负，那么它的角度theta应该是：theta=angle-pi,
"""

import os
import numpy as np

try: 
    import xml.etree.cElementTree as ET 
except ImportError: 
    import xml.etree.ElementTree as ET 
import sys 

import math
 
 
def rotate(angle, x, y):
    """
    基于原点的弧度旋转
    :param angle:   弧度
    :param x:       x
    :param y:       y
    :return:
    """
    rotatex = math.cos(angle) * x - math.sin(angle) * y
    rotatey = math.cos(angle) * y + math.sin(angle) * x
    return rotatex, rotatey
 
def xy_rorate(theta, x, y, centerx, centery):
    """
    针对中心点进行旋转
    :param theta:
    :param x:
    :param y:
    :param centerx:
    :param centery:
    :return:
    """
    r_x, r_y = rotate(theta, x - centerx, y - centery)
    return centerx+r_x, centery+r_y
 
def rec_rotate(x, y, width, height, theta):
    """
    传入矩形的x,y和宽度高度，弧度，转成QUAD格式
    :param x:
    :param y:
    :param width:
    :param height:
    :param theta:
    :return:
    """
    centerx = x + width / 2
    centery = y + height / 2
 
    x1, y1 = xy_rorate(theta, x, y, centerx, centery)
    x2, y2 = xy_rorate(theta, x+width, y, centerx, centery)
    x3, y3 = xy_rorate(theta, x, y+height, centerx, centery)
    x4, y4 = xy_rorate(theta, x+width, y+height, centerx, centery)
 
    return x1, y1, x2, y2, x4, y4,x3, y3


def test(x,y,cx,cy,theta):
    x1_test = cx+(x-cx)*math.cos(theta)-(y-cy)*math.sin(theta)
    y1_test = cy+(y-cy)*math.cos(theta)+(x-cx)*math.sin(theta)
    print('x1_testx1_testx1_testx1_testx1_test',x1_test)
    print('y1_testy1_testy1_testy1_testy1_test',y1_test)


PATH = './RoLabelImg_Transform/'
fr = open(PATH + '/xml_to_txt_list.txt')  #其中包含所有待计算的文件名

xml_path = os.path.join(PATH, 'xml/')
txt_path = os.path.join(PATH, 'txt/')
# print(xml_path)
for line in fr.readlines():
    if line:
        tree = ET.parse(os.path.join(xml_path,line.strip()))     #打开xml文档 
        root = tree.getroot()         #获得root节点  
        filename = root.find('filename').text
        file_object = open(os.path.join(txt_path,filename + ".txt"), 'w') #写文件
        # file_object_log = open(filename + ".log", 'w') #写文件
        flag = False

    for size in root.findall('size'): #找到root节点下的size节点 
        width = size.find('width').text   #子节点下节点width的值 
        height = size.find('height').text   #子节点下节点height的值 

    for object in root.findall('object'): #找到root节点下的所有object节点 
        name = object.find('name').text
        robndbox = object.find('robndbox')
        print(filename)
        cx = float(robndbox.find('cx').text)
        cy = float(robndbox.find('cy').text)
        w = float(robndbox.find('w').text)
        h = float(robndbox.find('h').text)
        angle = float(robndbox.find('angle').text)

        x = cx - w/2
        y = cy - h/2
        if angle<1.57:
            theta = round(angle, 6)
        else:
            theta = round(angle - np.pi, 6)
        x1, y1, x2, y2, x4, y4,x3, y3 = rec_rotate(x, y, w, h, theta)
        x1,y1,x2,y2,x4,y4,x3,y3 = int(x1),int(y1),int(x2),int(y2),int(x4),int(y4),int(x3),int(y3)
        print(filename, x1, y1, x2, y2, x4, y4,x3, y3)

        test(x,y,cx,cy,theta)

        file_object.write(str(x1)+','+str(y1)+','+str(x2)+','+str(y2)+','+str(x4)+','+str(y4)+','+str(x3)+','+str(y3)+','+name)
        file_object.write('\n')
    file_object.close()