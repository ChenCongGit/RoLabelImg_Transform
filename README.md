# RoLabelImg_Transform
该项目是针对行文本检测框标签(旋转矩形检测框)两种表示形式的转化(txt和xml)。

## 文本检测框
文本检测常用的标注形式有水平矩形框、旋转矩形框、任意四边形框、任意多边形框、其他形式(如文本蛇)等，如下图所示。
![](/相关图片/常用文本检测框标注形式.png "常用文本检测框标注形式")

该项目针对其中文本检测使用最多的旋转矩形框表示形式进行读写，转化。旋转矩形框与常规的目标检测bounding box不同，在它的基础上添加了旋转角度，对常规水平检测框进行旋转。

旋转矩形框通常有两种表示形式:
 1. 中心点坐标、宽、高、旋转角度，常采用xml文件保存
 2. 矩形四个角点的坐标，通常直接使用txt文件简单保存(如ICDAR2015数据集)

## 中心-旋转角表示
以下面一个检测框为例:
```
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
```
xml文件保存了旋转检测框的类别(wenben)、中心点坐标(cx,cy)、宽高(w,h)、旋转角(angle)

## 矩形角点坐标表示
以下面一个检测框为例:
```
x1,y1,x2,y2,x3,y3,x4,y4,labelname
```
txt文件中的每一行都如上所示，x1,y1,x2,y2,x3,y3,x4,y4分别是四个角点的横纵坐标，labelname是检测框的类别

## 两种表示方式转换
具体计算公式如下:
```
x1 = cx-w/2*cos(theta)+h/2*sin(theta)
y1 = cy-h/2*cos(theta)-w/2*sin(theta)
x2 = cx-w/2*cos(theta)+h/2*sin(theta)
y2 = cy-h/2*cos(theta)+w/2*sin(theta)
x3 = cx+w/2*cos(theta)-h/2*sin(theta)
y3 = cy+h/2*cos(theta)-w/2*sin(theta)
x4 = cx+w/2*cos(theta)+h/2*sin(theta)
y4 = cy+h/2*cos(theta)+w/2*sin(theta)
```
其中theta与角度angle有关，当angle小于pi/2时，theta等于angle，当angle大于pi/2时，theta等于angle-pi。

## 代码程序
### 准备环境
该程序需要以下依赖包:
 - python3.6
 - opencv-python 4.1.0.25
 - lxml 4.4.0

### txt转xml
将需要转换的图像文件放入`img`文件夹，txt检测框文件放入`txt`文件夹，运行`get_list.py`得到转换列表`txt_to_xml_list.txt`，然后运行`txt_to_xml.py`，在`xml`文件夹中得到同名的xml格式标签文件
```
python RoLabelImg_Transform/get_list.py --model='txt_to_xml' --input_path='./RoLabelImg_Transform/txt/'
python RoLabelImg_Transform/txt_to_xml.py
```
### xml转txt
将需要转换的图像文件放入`img`文件夹，xml检测框文件放入`xml`文件夹，运行`get_list.py`得到转换列表`xml_to_txt_list.txt`，然后运行`xml_to_txt.py`，在`txt`文件夹中得到同名的txt格式标签文件
```
python RoLabelImg_Transform/get_list.py --model='xml_to_txt' --input_path='./RoLabelImg_Transform/xml/'
python RoLabelImg_Transform/xml_to_txt.py
```

### txt检测框可视化
对txt文件检测框进行可视化，运行`visualize.py`文件，可视化后的图像保存在`visualized_img`文件夹中
```
python RoLabelImg_Transform/visualize.py
```
