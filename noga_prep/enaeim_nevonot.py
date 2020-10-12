import os
import xml.etree.ElementTree as ET
import image_bbox_slicer as ibs
import cv2
import glob
import os.path
from os import path
import shutil

def remove_non_jpg_files():
    xmls = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos/'
    for fname in os.listdir(xmls):
        if not fname.endswith('.xml'):
            print(fname)
            os.remove(xmls+fname)
    jpegs = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big/'
    #anos = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos/'
    for fname in os.listdir(jpegs):
        if not fname.endswith('.xml'):
            print(fname)
            os.remove(jpegs+fname)

def change_class_to_name():
    rd = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big/'
    for fname in os.listdir(rd):
        if fname.endswith('.xml'):
            in_file = rd + fname
            tree = ET.parse(in_file)
            root = tree.getroot()
            for cls in root.iter('class'):
                cls.tag='name'
            tree.write(rd + fname)

def fix_names_in_xmlfiles():
    an_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_anos_big_dim_slices/'
    counter=0
    for fname in os.listdir(an_dst):
        in_file = an_dst + fname
        tree = ET.parse(in_file)
        if tree.find('.//filename').text != fname.replace("xml","jpg"):
            tree.find('.//filename').text = fname.replace("xml","jpg")
            tree.write(in_file)
            counter+=1
            print(counter)

def fix_img_size_in_xmlfiles():
    an_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_anos_big_dim_slices/'
    im_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_jpegs_big_dim_slices/'
    for img in os.listdir(im_dst):
        print(img)
        im = cv2.imread(im_dst + img)
        xmlfile = an_dst + img.replace("jpg","xml")
        tree = ET.parse(xmlfile)
        h, w, c = im.shape
        tree.find('.//width').text = str(w)
        tree.find('.//height').text = str(h)
        tree.write(xmlfile)

def get_size_of_images():
    jpegs = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs_anos/'
    images = glob.glob(jpegs + '*.jpg')
    sizes = {}
    for img in images:
        im = cv2.imread(img)
        h, w, c = im.shape
        if (h,w) in sizes.keys():
            sizes[(h,w)] += 1
        else:
            sizes[(h, w)] = 1
    print(sizes)

def slice_pictures():
    im_src = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs_big/'
    an_src = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big/'
    im_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs_big_slices/'
    an_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big_slices/'
    slicer = ibs.Slicer()
    slicer.config_dirs(img_src=im_src, ann_src=an_src, img_dst=im_dst, ann_dst=an_dst)
    slicer.keep_partial_labels = False
    slicer.ignore_empty_tiles = False
    slicer.save_before_after_map = False
    slicer.slice_by_size(tile_size=(660, 660), tile_overlap=0)

def remove_files_without_couple():
    to_remove=[]
    im_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_jpegs_big_dim_slices/'
    an_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_anos_big_dim_slices/'
    images = glob.glob(im_dst + '*.jpg')
    xmls = glob.glob(an_dst + '*.xml')
    print("going over jpegs...")
    for img in images:
        if not os.path.exists(an_dst + img.split('/')[-1].replace('jpg','xml')):
            print(img)
            to_remove.append(img)
    print("going over xmls...")
    for xml in xmls:
        if not os.path.exists(im_dst + xml.split('/')[-1].replace('xml','jpg')):
            print(xml)
            to_remove.append(xml)
    print (len(to_remove))
    for x in to_remove:
        os.remove(x)

def get_classes():
    root_dir = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos/'
    xmls = glob.glob(root_dir + '*.xml')
    classes = {}
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        for obj in root.iter('object'):
            cls= obj.find('name').text
            if cls in classes.keys():
                classes[cls] += 1
            else:
                classes[cls]=1
    return classes

def remove_empty_images():
    an_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big/'
    im_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs_big/'
    xmls = os.listdir(an_dst)
    to_remove=[]
    for xml in xmls:
        tree = ET.parse(an_dst + xml)
        root = tree.getroot()
        ret = root.find("object")
        print(xml + "|" + str(ret))
        if ret is None:
            to_remove.append(xml)
    print(len(to_remove))
    for f in to_remove:
        os.remove(an_dst + f)
        os.remove(im_dst + f.replace("xml", "jpg"))

def fix_classes_names():
    root_dir = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big/'
    switcher = {'motorcycle': 'motorcycle', 'Motorbike': 'motorcycle', 'rider': 'motorcycle',
                 'person': 'person', 'man': 'person', 'people': 'person', 'Man': 'person',
                'truck': 'car', 'Truck': 'car', 'pick-up': 'car','bus': 'car', 'cement mixer': 'truck',
                'car': 'car',   'Car': 'car','van': 'car', 'tank': 'car', 'blurred_car': 'car'
                }
    xmls = glob.glob(root_dir + '*.xml')
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        for obj in root.iter('object'):
            name = obj.find('name').text
            obj.find('name').text = switcher.get(name)
        tree.write(xml)

def remove_if_not_in_class(classes):
    root_dir = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos/'
    xmls = glob.glob(root_dir + '*.xml')
    non_relevant = []
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        to_remove= True
        for obj in root.iter('object'):
            if obj.find('name').text in classes:
                to_remove=False
                break
        if to_remove:
            non_relevant.append(xml)
    print(len(non_relevant))
    for f in non_relevant:
        os.remove(f)
        os.remove(f.replace("xml", "jpg").replace('merged_anos','merged_jpegs'))

def rename():
    ss = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs_anos_augment/'
    files = os.listdir(ss)
    for f in files:
        #a=f.split('.')
        #os.rename(ss+f, ss + a[0]+'_111'+ '.' + a[1] )
        print (f)


def copy_files():
    target_dir = '/home/ddd/dddyolo/nogaTiny2classes/merged_jpegs/'
    im_src = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_jpegs_big_dim_slices/'
    #an_dst = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/BigDim/merged_anos_big_dim_slices/'
    counter = + 1
    for img in os.listdir(im_src):
        shutil.copyfile(im_src + img, target_dir+img)
        counter += 1
        print(counter)


def seperate_big_images():
    an_source = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos/'
    im_source = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs/'
    an_target = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_anos_big/'
    im_target = '/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/merged_jpegs_big/'
    images = os.listdir(im_source)
    for file in images:
        im = cv2.imread(im_source + file)
        h, w, c = im.shape
        if h in [2160, 1080, 1920]:
            shutil.move(im_source + file, im_target + '111_' + file)
            xmlfile = file.replace('jpg','xml')
            shutil.move(an_source + xmlfile, an_target + '111_' + xmlfile)


#seperate_big_images()
#prepare_folder_high_dim()
#remove_files_without_couple()
#fix_img_size_in_xmlfiles()
#fix_classes_names()
#print(get_classes())
#add_jpg_to_xml_files()
#get_size_of_images()
slice_pictures()
#prepare_before_yolo()
#fix_img_size_in_xmlfiles()

#change_class_to_name()
#fix_classes_names()
#remove_empty_images()


'''
(546, 720)  : 223,
 (576, 486)  : 351,
 (481, 381)  : 217,
 (512, 640)  : 28181,
 (576, 720)  : 4231, 
 (2160, 3840): 56053,
 (486, 486)  : 695,
 (480, 640)  : 1914,
 (513, 640)  : 20782,
 (1080, 1920): 15070,
 (576, 471)  : 58}
'''