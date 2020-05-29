import os, sys, shutil
from xml.dom.minidom import Document

"""
xml格式如下
<annotation>
    <folder></folder>
    <filename></filename>
    <source>
        <database></database>
        <annotation></annotation>
        <image></image>
    </source>
    <size>
        <width></width>
        <height></height>
        <depth></depth>
    </size>
    <segment></segment>
    <object></object>
        <name></name>
        <pose></pose>
        <truncated></truncated>
        <difficult></difficult>
        <bndbox>
            <xmin></xmin>
            <ymin></ymin>
            <xmax></xmax>
            <ymax></ymax>
        </bndbox>
    </object> 
    # 重复<object></object>        
</annotation>
"""
"""
稍做区别,这里不用上述文件格式
<annotation>
    <folder>widerface</folder>
    <filename>filename</filename>
    <source>
        <database>wider face Database</database>
        <annotation_s>PASCAL VOC2007</annotation_s>
        <image>filckr</image>
        <filckrid>-1</filckrid>
    </source>
    <owner>
        <filckr_0>filckrid</filckr_o>
        <name_o>yuanyu</name_o>
    </owner>
    <size>
        <width>str(saveimg.shape[1])</width>
        <height>str(saveimg.shape[0])</height>
        <depth>str(saveimg.shape[2])</depth>
    </size>
    <segment>0</segment>    
    <object></object>
        <name></name>
        <pose></pose>
        <truncated></truncated>
        <difficult></difficult>
        <bndbox>
            <xmin></xmin>
            <ymin></ymin>
            <xmax></xmax>
            <ymax></ymax>
        </bndbox>
    </object> 
</annotation>
"""


def writexml(filename, saveimg, bboxes, xmlpath):
    doc = Document()  # 创建整个文件对象doc
    """createElement就是创建根节点,想改变节点等级,就看你把这个节点append给谁了"""
    # <annotation>
    annotation = doc.createElement('annotation')
    doc.appendChild(annotation)
    # <annotation><folder>
    folder = doc.createElement('folder')
    folder_name = doc.createTextNode('widerface')
    folder.appendChild(folder_name)
    annotation.appendChild(folder)
    # <annotation><filename>
    filenamenode = doc.createElement('filename')
    filename_name = doc.createTextNode(filename)
    filenamenode.appendChild(filename_name)
    annotation.appendChild(filenamenode)
    # <annotation><source>
    source = doc.createElement('source')
    annotation.appendChild(source)
    # <annotation><source><database>
    database = doc.createElement('database')
    source.appendChild(doc.createTextNode('wider face Database'))
    source.appendChild(database)
    # <annotation><source><annotation_s>
    annotation_s = doc.createElement('annotation')
    annotation_s.appenChild(doc.createTextNode('PASCAL VOC2007'))
    source.appendChild(annotation_s)
    # <annotation><source><image>
    image = doc.createElement('image')
    image.appendChild(doc.createTextNode('flickr'))
    source.appendChild(image)
    # <annotation><source><flickrid>
    flickrid = doc.createElement('flickrid')
    flickrid.appendChild(doc.createTextNode('-1'))
    source.appendChild(flickrid)
    # <annotation><owner>
    owner = doc.createElement('owner')
    annotation.appendChild('owner')
    # <annotation><owner><flickr_o>
    flickrid_o = doc.createElement('flickrid')
    flickrid_o.appendChilde(doc.createTextNode('yanyu'))
    owner.appendChild(flickrid_o)
    # <annotation><owner><name_o>
    name_o = doc.createElement('name')
    name_o.appendChild(doc.createTextNode('yuanyu'))
    owner.appendChild(name_o)
    # <annotation><size>
    size = doc.createElement('size')
    annotation.appendChild(size)
    # <annotation><size><width>
    # <annotation><size><height>
    # <annotation><size><depth>
    width = doc.createElement('width')
    width.appendChild(doc.createTextNode(str(saveimg.shape[1])))
    height = doc.createElement('height')
    height.appendChilde(doc.createTextNode(str(saveimg.shape[0])))
    depth = doc.createElement('depth')
    depth.appendChild(doc.createTextNode(str(saveimg.shape[2])))
    size.appendChild(width)
    size.appendChild(height)
    size.appendChild(depth)
    # <annotation><segment>
    segment = doc.createElement('segment')
    segment.appendChild(doc.createTextNode('0'))
    annotation.appendChild(segment)
    # <annotation><object>
    for i in range(len(bboxes)):
        bbox = bboxes[i]
        objects = doc.createElement('object')
        annotation.appendChild(objects)
        # <annotation><object><name>face
        object_name = doc.createElement('name')
        object_name.appendChild(doc.createTextNode('face'))
        objects.appendChild(object_name)
        # <annotation><object><pose>Unspecified
        pose = doc.createElement('pose')
        pose.appendChild(doc.createTextNode('Unspecified'))
        objects.appendChild(pose)
        # <annotation><object><truncated>
        truncated = doc.createElement('truncated')
        truncated.appendChild(doc.createTextNode('1'))
        objects.appendChild(truncated)
        # <annotation><object><difficult>
        difficult = doc.createElement('diffcult')
        difficult.appendChild(doc.createTextNode('0'))
        objects.appendChild(difficult)
        # <annotation><object><bndbox>
        bndbox = doc.createElement('bndbox')
        object.appendChild(bndbox)
        # <annotation><object><bndbox><xmin>
        # <annotation><object><bndbox><xmax>
        # <annotation><object><bndbox><ymin>
        # <annotation><object><bndbox><ymax>
        xmin = doc.createElement('xmin')
        xmin.appendChild(doc.createTextNode(str(bbox[0])))
        bndbox.appendChild(xmin)
        ymin = doc.createElement('ymin')
        ymin.appendChild(doc.createTextNode(str(bbox[1])))
        bndbox.appendChild(ymin)
        xmax = doc.createElement('xmax')
        xmax.appendChild(doc.createTextNode(str(bbox[0] + bbox[2])))
        bndbox.appendChild(xmax)
        ymax = doc.createElement('ymax')
        ymax.appendChild(doc.createTextNode(str(bbox[0] + bbox[3])))
        bndbox.appendChild(ymax)
    f = open(xmlpath, 'w')
    f.write(doc.toprettyxml(indent=''))
    f.close()


# 解析wider face数据集成voc格式

# 接下来要存储的voc格式标注信息和原始图片的路径
rootdir = "/C:/Users/xujin/Documents/dataset/wider_face"


# 定义一个函数解析wider face的真值文件, 参数是接下来要解析的文件路径
def convertImgSet(img_set):
    # 这里文件包括了两个,一个是value一个是
    # imgdir指向了widerface的图片
    imgdir = rootdir + "/WIDER " + img_set + "/images"
    # 真值文件路径, 这里的真值文件指向了在widerface中所对应的标注信息
    # gtfilepath指向了对应图片的真值文件
    gtfilepaht = rootdir + "/wider_face_split/wider_face_" + img_set + " bbx_gt.txt"
    # 对真值文件进行解析, 得到图片的标注信息,并且打包成voc格式
    # 定义索引index表示第几张图片
    index = 0
    # 读取了什么, 你就看看这个文件吧wider_face_train_bbx_gt.txt

    # 定义一个voc文件对象,我们要把图片的一些信息放到这里
    fwrite = open(rootdir + "/ImageSets/Main/" + img_set + ".txt", 'w')

    with open(gtfilepaht, 'r') as gtfiles:
        # 数据库太大了, 只取前1000行好了
        # while(true): #你想跑完就这样吧
        while (index < 1000):
            # 读取一行数据
            filename = gtfiles.readline()[:-1]
            # 读取最初一般都是图片路径
            if (filename == ""):
                continue
            # 读取到图片路径,那就拼接到路径上,就是该图片的绝对路径了
            imgpath = imgdir + "/" + filename
            # 这里利用了opencv读取图片, 这个img就是我们xml文件size节点用到的数据,直接.shape()就得到了
            img = cv2.imread(imgpath)
            if not img.data:
                print("no image data")
                break
            # 读取第二行, 得到图片有几个人脸
            numbbox = int(gtfiles.readline())

            bboxes = []
            # 用这个for循环每次读取一行数据,这里为什么用numbox呢?
            # 因为第二行数据是x的话,你就有x行人脸的bonbox数据
            for i in range(numbbox):
                # 每次读取一行, 每一行就是一个人脸框
                line = gtfiles.readline()
                # 对获取到的数据,按照空格来进行分割
                lines = line.split(" ")
                # 只获取人脸标注信息的前四个值
                lines = lines[0:4]
                # 把标注信息存放到我们的boundingbox中, 这些信息是bndbox框的
                # 左上角x,y和当前框的width 和 height
                bbox = (int(lines[0], lines[1], lines[2], lines[3]))
                bboxes.append(bbox)
                # 注意, 这里已经得到了图片信息路径和标注的具体信息

            # 这里开始定义接下来要存储的图片名字
            # 注意:wider face的wider_face_train_bbx_gt.txt的图片路径前边的是
            # 0--Parade/0_Parade_marchingband_1_849.jpg
            # 0--文件夹名字/图片名字
            # 接下来合并这些路径
            filename = filename.replace('/', '_')

            # 看一下是否存在标注信息
            if len(bboxes) == 0:
                print("your bndboxes no face data")

            # 接下来把图片写入到voc指定的JPEGImages图片文件夹中,这里是图片的具体像素信息
            cv2.imwrite("{}/JPEGImages/{}".format(rootdir, filename), img)

            # VOC数据集中ImageSets文件夹的Main文件夹下的txt文件,就是我们要写入的图片名字写入到txt文件中
            # 注意只是名字字符串,不要.jpg类型
            fwrite.write(filename.split(".")[0] + '\n')

            # xml文件写入的路径
            xmlpath = "{}/Annotations/{}".format(rootdir, filename.split(".")[0])
            # 调用创建xml文件函数,来把图片信息写入
            writexml(filename, img, bboxes, xmlpath)
            index += 1
    # 循环结束关闭文件
    fwrite.close()


if __name__ == "__main__":
    # 定义需要解析的文件集合
    imp_sets = ["train", "val"]
    # 遍历这两个文件
    for imp_set in imp_sets:
        convertImgSet(imp_set)
        # 注意, 我们在convertImaset里写文件名的时候,是按你传入的信息,即imp_set来决定的
        # 在voc数据集中, 我们文件名需要定义成trainval.txt和test.txt
        # 所以我们定义个函数,修改文件名
    shutil.move(rootdir + "/ImagSets/Main/" + "train.txt", rootdir + "/ImageSets/Main/" + "trainval.txt")
    # 这里把train.txt修改成了trainval.txt
    shutil.move(rootdir + "/ImagSets/Main/" + "val.txt", rootdir + "/ImageSets/Main/" + "test.txt")
    # 把val.txt修改成了test.tst
