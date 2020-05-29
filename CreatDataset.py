import os, sys, shutil
from xml.dom.minidom import Document
"使用python3.7标准环境"
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
    doc = Document() # 创建整个文件对象doc
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
















