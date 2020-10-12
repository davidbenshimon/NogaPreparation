import os
from shutil import copyfile
from pathlib import Path
import shutil
import xml.etree.ElementTree as ET

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


def convert_annotation(image_id, classes, m_jpegs, m_anos):
    in_file = open(m_anos + "/" + image_id + ".xml")
    out_file = open(m_jpegs + "/" + image_id+".txt", 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    having_objects = False
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes:
            continue
        if difficult=='Null' or  difficult=='null' or (int(difficult) != 0 and int(difficult) != 1):
            continue
        having_objects = True
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
    return having_objects


def gen_yolo_anos(classes, root_directory,m_jpegs,m_anos):
    train_file = open(root_directory + "train.txt", 'w')
    test_file = open(root_directory + "test.txt", 'w')
    counter = 1
    for fl in os.listdir(m_anos):
        counter += 1
        image_id = fl.split(".")[0]
        having_objects = convert_annotation(image_id, classes, m_jpegs, m_anos)
        if not having_objects:
            continue
        if int(counter) % 4 != 0:
            train_file.write(m_jpegs + image_id + ".jpg" + '\n')
        else:
            test_file.write(m_jpegs + image_id + ".jpg" + '\n')
        print(image_id)
    train_file.close()

def main():
    rd = '/home/ddd/dddyolo/nogaTiny2classes/'
    mpegs = '/home/ddd/dddyolo/nogaTiny2classes/merged_jpegs/'
    anos = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_anos_big_dim_slices/'
    classes = ['car','person']
    gen_yolo_anos(classes, rd, mpegs, anos)

main()