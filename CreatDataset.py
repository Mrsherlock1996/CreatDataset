import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join
import random

classes=["nomask","mask"]


def clear_hidden_files(path):
    dir_list = os.listdir(path)
    for i in dir_list:
        abspath = os.path.join(os.path.abspath(path), i)
        if os.path.isfile(abspath):
            if i.startswith("._"):
                os.remove(abspath)
        else:
            clear_hidden_files(abspath)

def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id): #把xml文件转成txt文件
    in_file = open('Annotations\%s.xml' %image_id)
    out_file = open('labels\%s.txt' %image_id, 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:  #这里是排除和mask与no mask标签无关的object
            continue
        cls_id = classes.index(cls)   #得到mask或nomask标签索引
        xmlbox = obj.find('bndbox')   #寻找boundingbox的信息,构建信息列表 b 同时转换成float类型
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        #print("image_id = %s\n" %image_id)
        bb = convert((w,h), b)   # 由于boundingbox的坐标信息和数据集的有出入,所以进行数据修改
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n') #写入一行到txt文件, 这么写是因为数据集或网络结构的要求
    in_file.close()
    out_file.close()


#创建VOC文件夹,这里的程序决定你的脚本放到哪个文件夹中运行,我选择了在VOC2007中执行,所以不必添加下文的两个路径


# wd = os.getcwd()
wd = os.getcwd()
print(str(wd))
#这里wd=C:\Users\xujin\Documents\YOLO4\darknet-master\build\darknet\VOCdevkit\VOC2007
work_space_dir = wd
print("work_space_dir: ")
print(work_space_dir)
#我已经创建好了Annotation和JPEGImages文件夹不需要判断了,免得出错
# if not os.path.isdir(work_space_dir):
#     os.mkdir(work_space_dir)
#work_space_dir = os.path.join(work_space_dir, "VOC2007/")
# if not os.path.isdir(work_space_dir):
#     os.mkdir(work_space_dir)
annotation_dir = os.path.join(work_space_dir, "Annotations\\")
print("annotation_dir")
print(str(annotation_dir))
# if not os.path.isdir(annotation_dir):
#         os.mkdir(annotation_dir)
# clear_hidden_files(annotation_dir)
image_dir = os.path.join(work_space_dir, "JPEGImages\\")
print("image_dir")
print(str(image_dir))
# if not os.path.isdir(image_dir):
#         os.mkdir(image_dir)
# clear_hidden_files(image_dir)
VOC_file_dir = os.path.join(work_space_dir, "ImageSets\\")
if not os.path.isdir(VOC_file_dir):
        os.mkdir(VOC_file_dir)
VOC_file_dir = os.path.join(VOC_file_dir, "Main\\")
if not os.path.isdir(VOC_file_dir):
        os.mkdir(VOC_file_dir)
print(str(VOC_file_dir))

#创建四个txt空文本
train_file = open(os.path.join(wd, "2007_train.txt"), 'w')
test_file = open(os.path.join(wd, "2007_test.txt"), 'w')
train_file.close()
test_file.close()
VOC_train_file = open(os.path.join(work_space_dir, "ImageSets\Main\\train.txt"), 'w')

VOC_test_file = open(os.path.join(work_space_dir, "ImageSets\Main\\test.txt"), 'w')

VOC_train_file.close()
VOC_test_file.close()

#我已经创建好了
# if not os.path.exists('VOCdevkit/VOC2007/labels'):
#     os.makedirs('VOCdevkit/VOC2007/labels')
train_file = open(os.path.join(wd, "2007_train.txt"), 'a')
test_file = open(os.path.join(wd, "2007_test.txt"), 'a')
VOC_train_file = open(os.path.join(work_space_dir, "ImageSets\Main\\train.txt"), 'a')
voc_train_file_path = os.path.join(wd, "ImageSets\Main\\train.txt")
print(str(voc_train_file_path))
VOC_test_file = open(os.path.join(work_space_dir, "ImageSets\Main\\test.txt"), 'a')

list = os.listdir(image_dir) # list image files
probo = random.randint(1, 100)
print("Probobility: %d" % probo)
for i in range(0,len(list)):
    path = os.path.join(image_dir,list[i])
    if os.path.isfile(path):
        image_path = image_dir + list[i]
        voc_path = list[i]
        (nameWithoutExtention, extention) = os.path.splitext(os.path.basename(image_path))
        (voc_nameWithoutExtention, voc_extention) = os.path.splitext(os.path.basename(voc_path))
        annotation_name = nameWithoutExtention + '.xml'
        annotation_path = os.path.join(annotation_dir, annotation_name)
    probo = random.randint(1, 100)
    #print("Probobility: %d" % probo)
    if(probo < 80):
        if os.path.exists(annotation_path):
            train_file.write(image_path + '\n')
            VOC_train_file.write(voc_nameWithoutExtention + '\n')
            convert_annotation(nameWithoutExtention)
    else:
        if os.path.exists(annotation_path):
            test_file.write(image_path + '\n')
            VOC_test_file.write(voc_nameWithoutExtention + '\n')
            convert_annotation(nameWithoutExtention)
train_file.close()
test_file.close()
VOC_train_file.close()
VOC_test_file.close()
