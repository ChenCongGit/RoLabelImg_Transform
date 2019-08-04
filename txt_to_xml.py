#coding:utf-8 

"""
每一张图片的所有检测框信息都保存在一个txt文件中
txt文件中的每一行代表一个bbox检测框，其值分别为[x1,y1,x2,y2,x3,y3,x4,y4,labelname]
我们需要将其转化为下面xml形式:
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

x1 = cx+(x-cx)*math.cos(theta)-(y-cy)*math.sin(theta) = cx-w/2*cos(theta)+h/2*sin(theta)
y1 = cy+(y-cy)*math.cos(theta)+(x-cx)*math.sin(theta) = cy-h/2*cos(theta)-w/2*sin(theta)
x2 = cx-w/2*cos(theta)+h/2*sin(theta)
y2 = cy-h/2*cos(theta)+w/2*sin(theta)
x3 = cx+w/2*cos(theta)-h/2*sin(theta)
y3 = cy+h/2*cos(theta)-w/2*sin(theta)
x4 = cx+w/2*cos(theta)+h/2*sin(theta)
y4 = cy+h/2*cos(theta)+w/2*sin(theta)

其中等号左边的变量已知，求解cx,cy,w,h,theta，x,y和cx,cy满足x = cx - w/2, y = cy - h/2
"""

import os
import cv2
import math
import codecs
import numpy as np
from lxml import etree
from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement

PATH = './RoLabelImg_Transform/'

def get_angle(x1,y1,x2,y2,x3,y3,x4,y4):
    if x2-x1 != 0 and x4-x3 != 0:
        theta = (math.atan((y2-y1)/(x2-x1)) + math.atan((y4-y3)/(x4-x3)))/2
    else:
        theta = np.pi/2

    if theta >= 0:
        angle = theta
    else:
        angle = theta + np.pi
    return angle,theta


def get_w_and_h(x1,y1,x2,y2,x3,y3,x4,y4):
    w = math.sqrt((x2-x1)**2+(y2-y1)**2)
    h = math.sqrt((x1-x3)**2+(y1-y3)**2)
    return w,h


def get_x_and_y(x1,y1,x2,y2,x3,y3,x4,y4,theta,w,h):
    cx = (x2+x3)/2
    cy = (y2+y3)/2
    x = cx - w/2
    y = cy - h/2
    return x,y,cx,cy


def test(x,y,cx,cy,theta):
    x1_test = cx+(x-cx)*math.cos(theta)-(y-cy)*math.sin(theta)
    y1_test = cy+(y-cy)*math.cos(theta)+(x-cx)*math.sin(theta)
    print('x1_testx1_testx1_testx1_testx1_test',x1_test)
    print('y1_testy1_testy1_testy1_testy1_test',y1_test)


class CreateXml():
    def __init__(self,foldername,filename,imgSize,databaseSrc='Unknown',localImgPath=None):
        self.foldername = foldername
        self.filename = filename
        self.databaseSrc = databaseSrc
        self.imgSize = imgSize
        self.roboxlist = []
        self.roboxobject = None
        self.localImgPath = localImgPath
        self.verified = False

    def prettify(self, elem):
        """
            Return a pretty-printed XML string for the Element.
        """
        rough_string = ElementTree.tostring(elem, 'utf8')
        root = etree.fromstring(rough_string)
        try:
            return etree.tostring(root, pretty_print=True)
        except TypeError:
            return etree.tostring(root)
    
    def genXML(self):
        """
            Return XML root
        """
        # Check conditions
        if self.filename is None or \
                self.foldername is None or \
                self.imgSize is None:
            return None

        top = Element('annotation')
        top.set('verified', 'yes' if self.verified else 'no')

        folder = SubElement(top, 'folder')
        folder.text = self.foldername

        filename = SubElement(top, 'filename')
        filename.text = self.filename

        localImgPath = SubElement(top, 'path')
        localImgPath.text = self.localImgPath

        source = SubElement(top, 'source')
        database = SubElement(source, 'database')
        database.text = self.databaseSrc

        size_part = SubElement(top, 'size')
        width = SubElement(size_part, 'width')
        height = SubElement(size_part, 'height')
        depth = SubElement(size_part, 'depth')
        width.text = str(self.imgSize[1])
        height.text = str(self.imgSize[0])
        if len(self.imgSize) == 3:
            depth.text = str(self.imgSize[2])
        else:
            depth.text = '1'

        segmented = SubElement(top, 'segmented')
        segmented.text = '0'
        return top

    def addRotatedBndBox(self, cx, cy, w, h, angle, name, difficult):
        robndbox = {'cx': cx, 'cy': cy, 'w': w, 'h': h, 'angle': angle}
        robndbox['name'] = name
        robndbox['difficult'] = difficult
        self.roboxlist.append(robndbox)
        self.roboxobject = robndbox

    def appendObjects(self, top):
        # for each_object in self.roboxlist:
        each_object = self.roboxobject
        object_item = SubElement(top, 'object')
        typeItem = SubElement(object_item, 'type')
        typeItem.text = "robndbox"
        name = SubElement(object_item, 'name')
        try:
            name.text = unicode(each_object['name'])
        except NameError:
            # Py3: NameError: name 'unicode' is not defined
            name.text = each_object['name']
        pose = SubElement(object_item, 'pose')
        pose.text = "Unspecified"
        truncated = SubElement(object_item, 'truncated')
        truncated.text = "0"
        difficult = SubElement(object_item, 'difficult')
        difficult.text = str( bool(each_object['difficult']) & 1 )
        robndbox = SubElement(object_item, 'robndbox')
        cx = SubElement(robndbox, 'cx')
        cx.text = str(each_object['cx'])
        cy = SubElement(robndbox, 'cy')
        cy.text = str(each_object['cy'])
        w = SubElement(robndbox, 'w')
        w.text = str(each_object['w'])
        h = SubElement(robndbox, 'h')
        h.text = str(each_object['h'])
        angle = SubElement(robndbox, 'angle')
        angle.text = str(each_object['angle'])

    def save(self, root, targetFile=None):
        # root = self.genXML()
        # self.appendObjects(root)
        out_file = None
        if targetFile is None:
            out_file = codecs.open(
                os.path.join(PATH,'xml/' + self.filename + '.xml'), 'w', encoding='utf-8')
        else:
            out_file = codecs.open(targetFile, 'w', encoding='utf-8')

        prettifyResult = self.prettify(root)
        out_file.write(prettifyResult.decode('utf8'))
        out_file.close()


fr = open(os.path.join(PATH + '/txt_to_xml_list.txt'))

img_path = os.path.join(PATH, 'img/')
xml_path = os.path.join(PATH, 'xml/')
txt_path = os.path.join(PATH, 'txt/')
for line in fr.readlines():
    if line:
        img_base_name = line.strip().split('.')[0]
        print(img_base_name[4:])
        img = cv2.imread(os.path.join(img_path,img_base_name+'.jpg'))
        create_xml = CreateXml(foldername='pixeliinkimg',
                               filename=line.strip().split('.')[0],
                               imgSize=img.shape,
                               databaseSrc='Unknown',
                               localImgPath=os.path.join(img_path,img_base_name+'.jpg'))
        xml_top = create_xml.genXML()

        fr_line = open(os.path.join(txt_path,line.strip()))
        for bbox_line in fr_line.readlines():
            bbox_list = bbox_line.strip().split(',')
            print(bbox_list)
            lux,luy,rux,ruy,rdx,rdy,ldx,ldy=float(bbox_list[0]),float(bbox_list[1]),\
                                            float(bbox_list[2]),float(bbox_list[3]),\
                                            float(bbox_list[4]),float(bbox_list[5]),\
                                            float(bbox_list[6]),float(bbox_list[7])
            x1,y1,x2,y2,x3,y3,x4,y4 = lux,luy,rux,ruy,ldx,ldy,rdx,rdy
            angle,theta = get_angle(x1,y1,x2,y2,x3,y3,x4,y4)
            w,h = get_w_and_h(x1,y1,x2,y2,x3,y3,x4,y4)
            x,y,cx,cy = get_x_and_y(x1,y1,x2,y2,x3,y3,x4,y4,theta,w,h)
            test(x,y,cx,cy,theta)

            create_xml.addRotatedBndBox(cx,cy,w,h,angle,bbox_list[-1],0)
            create_xml.appendObjects(xml_top)
        create_xml.save(xml_top)

