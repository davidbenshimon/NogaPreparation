import os
from shutil import copyfile
from pathlib import Path
import shutil
import glob
import xml.etree.ElementTree as ET

def get_paths_pairs(root_directory):
    pairs = []
    for dir_name in Path(root_directory).rglob('Annotations'):
        ano = dir_name
        jpeg = str(dir_name).replace('Annotations', 'JPEGImages')
        pair = (ano, jpeg)
        print(pair)
        pairs.append(pair)
    return pairs


def merge_pairs(root_directory, pairs):
    m_jpegs = root_directory + "merged_jpegs"  # jpeg + files
    m_anos = root_directory + "merged_anos"  # xml files
    if os.path.isdir(m_jpegs):
        shutil.rmtree(m_jpegs)
    if os.path.isdir(m_anos):
        shutil.rmtree(m_anos)
    os.mkdir(m_jpegs)
    os.mkdir(m_anos)
    counter = 2000000
    for pair in pairs:
        for fl in os.listdir(pair[1]):
            number = fl.split(".")[0]
            m_file = str(pair[1])+'/'+fl
            a_file = str(pair[0]) + "/" +number+".xml"
            if not os.path.isfile(m_file) or not os.path.isfile(a_file):
                continue
            copyfile(m_file, m_jpegs + '/' + str(counter)+".jpg")
            copyfile(str(pair[0]) + "/" +number+".xml", m_anos + '/' + str(counter) + ".xml")
            print(counter)
            counter += 1
    return m_jpegs, m_anos

def get_classes(pairs):
    classes = {}
    for p in pairs:
        for dir_name in Path(p[0]).rglob('Annotations'):
            xmls = glob.glob(dir_name + '*.xml')
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

def collect_merge():
    rd = '/media/ddd/Seagate Expansion Drive/fromElop/Noga/Carlton_120718/Coaps/'
    paths_pairs = get_paths_pairs(rd)
    #classes = get_classes(paths_pairs)
    #print(classes)
    merge_pairs(rd, paths_pairs)

#collect_merge()
#print(os.listdir('/media/ddd/Seagate Expansion Drive/TinyModelData/Noga/'))
