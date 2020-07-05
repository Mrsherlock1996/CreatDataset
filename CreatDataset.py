import os,sys,shutil
from xml.dom.minidom import Document
import cv2 as cv




def writexml(filename, saveimg, bboxes, xmlpath):
    doc = Document()
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)

    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('widerface')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)

    filename = doc.createElement('filename')
    annotation.appendChild(filename)
    filename_name = doc.createTextNode('filename')
    filename.appendChild(filename_name)

    source = doc.createElement('source')
    annotation.appendChild(source)
    database = doc.createElement('database')
    source.appendChild(database)
    database_name = doc.createTextNode('wider face Database')
    database.appendChild(database_name)
    annotation_s = doc.createElement('annotation_s')
    source.appendChild(annotation_s)
    annotation_s_name = doc.createTextNode('PASCAL VOC2007')
    annotation_s.appendChild(annotation_s_name)
    image = doc.createElement('image')
    source.appendChild(image)
    image_name = doc.createTextNode('filckr')
    image.appendChild(image_name)
    filckrid = doc.createElement('filckrid')
    source.appendChild(filckrid)
    filckrid_name = doc.createTextNode('-1')
    filckrid.appendChild(filckrid_name)

    owner = doc.createElement('owner')
    annotation.appendChild(owner)
    filckr_0 = doc.createElement('filckr_0')
    owner.appendChild(filckr_0)
    filckr_0_name = doc.createTextNode('filckrid')
    filckr_0.appendChild(filckr_0_name)
    name_0 = doc.createElement('name_0')
    owner.appendChild(name_0)
    name_0_name = doc.createTextNode('yuanyu')
    name_0.appendChild(name_0_name)

    size = doc.createElement('size')
    annotation.appendChild(size)
    width = doc.createElement('width')
    size.appendChild(width)
    #这里不明白如何读取图片的宽高的
    width.appendChild(doc.createElement(str(saveimg.shape[1])))
    height = doc.createElement('height')
    size.appendChild(height)
    height.appendChild(doc.createTextNode(str(saveimg.shape[0])))
    depth = doc.createElement('depth')
    size.appendChild(depth)
    depth.appendChild(doc.createTextNode(str(saveimg.shape[2])))
    segment = doc.createElement('segment')
    annotation.appendChild(segment)
    segment.appendChild(doc.createTextNode('0'))
    for i in range(len(bboxes)):
        bbox = bboxes[i]
        object = doc.createElement('object')
        annotation.appendChild(object)
        name = doc.createElement('name')
        #这里要注意是每个bbox都是name=face
        name.appendChild(doc.createTextNode('face'))
        #这里也要注意每个textnode怎么来的
        pose = doc.createElement('pose')
        object.appendChild(pose)
        pose.appendChild(doc.createTextNode('Unspecified'))
        truncated = doc.createElement('truncated')
        object.appendChild(truncated)
        truncated.appendChild(doc.createTextNode('truncated'))
        difficult = doc.createElement('difficult')
        object.appendChild(difficult)
        difficult.appendChild(doc.createTextNode('difficult'))
        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        xmin = doc.createElement('xmin')
        xmax = doc.createElement('xmax')
        ymin = doc.createElement('ymin')
        ymax = doc.createElement('ymax')
        bndbox.appendChild(xmin)
        bndbox.appendChild(xmax)
        bndbox.appendChild(ymin)
        bndbox.appendChild(ymax)
        xmin.appendChild(doc.createTextNode(str(bbox[0])))
        xmax.appendChild(doc.createTextNode(str(bbox[0]+bbox[2])))
        ymin.appendChild(doc.createTextNode(str(bbox[1])))
        ymax.appendChild(doc.createTextNode(str(bbox[1]+bbox[3])))
    f = open(xmlpath,'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()
    # 创建xml文件函数此时书写完成

rootdir = "C:/Users/sherlock/Documents/DataSet/wider_face"

# 解析文件路径，提取路径包含的必要信息
# 这里的文件路径具体是两种，分成了test，train，val等，所以采用img_set变量来代替
# "C:/Users/sherlock/Documents/DataSet/wider_face/WIDER_train/images”
# "C:/Users/sherlock/Documents/DataSet/wider_face/WIDER_test/images"
# "C:/Users/sherlock/Documents/DataSet/wider_face/WIDER_val/images"

# 存储了图片真值文件信息
# "C:/Users/sherlock/Documents/DataSet/wider_face/wider_face_split/wider_face_train_bbx_gt.txt"
# "C:/Users/sherlock/Documents/DataSet/wider_face/wider_face_split/wider_face_test_bbx_gt.txt"

def convertImg(img_set):
    print("begin to converImg")
    image_dir = rootdir + "/WIDER_" + img_set +"/images"
    # "C:/Users/sherlock/Documents/DataSet/wider_face/WIDER_train/images"
    gt_file_path = rootdir + "/wider_face_split/wider_face_" + img_set +"_bbx_gt.txt"

    index = 0
    # 创建需要的voc格式中ImageSets/train.txt和test.txt
    # 存放在"C:/Users/sherlock/Documents/DataSet/wider_face/ImageSets/Main/”
    # xml存放在
    # "C:/Users/sherlock/Documents/DataSet/wider_face/Annotation/”
    f_write = open(rootdir + "/ImageSets/Main/" + img_set + ".txt", 'w')

    with open(gt_file_path, 'r') as gtfiles:
        while(1):
            filename = gtfiles.readline()[:-1]
            if(filename == ""):
                break
            image_path = image_dir + '/' + filename # 得到图像具体路径
            # "C:/Users/sherlock/Documents/DataSet/wider_face/WIDER_train/images/0--Parade/0_Parade_marchingband_1_465.jpg"
            number_bndboxes = int(gtfiles.readline())
            bndboxes = []
            for i in range(number_bndboxes):
                parameters = gtfiles.readline()
                param_split_list = parameters.split(" ")
                bbox_param = param_split_list[:4]
                boudingbox = (int(bbox_param[0]),int(bbox_param[1]),int(bbox_param[2]),int(bbox_param[3]))
                bndboxes.append(boudingbox)
            if number_bndboxes == 0:
                print("your bndboxes no face data\n")
                parameters = gtfiles.readline()
                param_split_list = parameters.split(" ")
                bbox_param = param_split_list[:4]
                boudingbox = (int(bbox_param[0]), int(bbox_param[1]), int(bbox_param[2]), int(bbox_param[3]))
                bndboxes.append(boudingbox)
            image_jpg = filename.split('/')[1]
            image_name = image_jpg.split('.')[0] # 得到图像无扩展名名字

            f_write.write(image_name + '\n')  # 得到ImageSets/Main/只存图名的文本
            xmlpath = rootdir + "/Annotation/" + image_name + '.xml'
            img = cv.imread(image_path)
            cv.imwrite("{}/JPEGImages/{}".format(rootdir,image_jpg),img)
            writexml(image_dir+'/'+filename,img,bndboxes,xmlpath)
    print("convertImg has been finished")
    f_write.close()

if __name__ =="__main__":
    data_sets = ["val","train"]
    for set in data_sets:
        convertImg(set)
        print("have been finished", set, "set creat\n")













