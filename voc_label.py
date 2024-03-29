import xml.etree.ElementTree as ET
import os

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


def convert_annotation(ano):
    classes = ["car", "none_relevant", "rider", "person", "motorcycle"]
    in_file = open(ano)
    #out_file = open(target_labels+image_id+".txt", 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        #cls = obj.find('name').text
        cls = obj.find('class').text
        if cls not in classes or int(difficult) == 1:
            continue
        print(cls)
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        #out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
        print(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

ano = '/home/ddd/dddyolo/Noga/Digital_And_A_Half/4K/merged_anos/1800.xml'


convert_annotation(ano)
