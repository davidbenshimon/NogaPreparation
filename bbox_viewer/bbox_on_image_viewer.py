import cv2
import glob
from bs4 import BeautifulSoup

class Entity():
    def __init__(self, name, xmin, xmax, ymin, ymax, difficult, truncated):
        self.name = name
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.difficult = difficult
        self.truncated = truncated


class Data():
    def __init__(self, img_file, ano_file):
        self.image_name = img_file
        self.annotation_path =  ano_file
        self.annotations = self.load_masks()

    def load_masks(self):
        annotations = []
        xml_content = open(self.annotation_path).read()
        bs = BeautifulSoup(xml_content, 'xml')
        objs = bs.findAll('object')
        for obj in objs:
            #obj_name = obj.findChildren('name')[0].text
            obj_name = obj.findChildren('class')[0].text
            if obj_name == 'null':
                continue
            if obj.findChildren('difficult')[0].contents[0]=='null':
                continue
            difficult = int(obj.findChildren('difficult')[0].contents[0])
            #truncated = int(obj.findChildren('truncated')[0].contents[0])
            truncated = 0
            bbox = obj.findChildren('bndbox')[0]
            xmin = int(bbox.findChildren('xmin')[0].contents[0])
            ymin = int(bbox.findChildren('ymin')[0].contents[0])
            xmax = int(bbox.findChildren('xmax')[0].contents[0])
            ymax = int(bbox.findChildren('ymax')[0].contents[0])
            annotations.append(Entity(obj_name, xmin, xmax, ymin, ymax, difficult, truncated))
        return annotations


def process_image(image_data):
    image = cv2.imread(image_data.image_path)
    image = cv2.putText(image, image_data.image_name, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    for ann in image_data.annotations:
        box_color = (0, 255, 0)  #Green
        if ann.difficult or ann.truncated:
            box_color = (0, 0, 255) #Red
        image = cv2.rectangle(image, (ann.xmin, ann.ymin), (ann.xmax, ann.ymax), box_color, 2)
        image = cv2.putText(image, ann.name, (ann.xmin, ann.ymin), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    return image


def visualize_bbox_on_images(root_dir):
    files = glob.glob(root_dir+'*.jpg')
    for f in files:
        img_file = f
        anno_file = f. replace("jpg","xml")
        image_data = Data(img_file, anno_file)
        image_data.image_path = img_file
        image = process_image(image_data)

        cv2.imshow('image', image)
        cv2.waitKey(0)

def visualize_bbox_on_images(img_dir, ano_dir):
    images = glob.glob(img_dir+'*.jpg')
    for f in images:
        img_file = f
        anno_file = f.replace(img_dir,ano_dir).replace("jpg","xml")
        image_data = Data(img_file, anno_file)
        image_data.image_path = img_file
        image = process_image(image_data)
        image = cv2.resize(image, (900, 900))
        cv2.imshow('image', image)

        cv2.waitKey(0)

ano_dir = '/media/ddd/Seagate Expansion Drive/fromElop/Noga/Carlton_120718/Coaps/After_Noon/500/FOV_1.65/sample_13/VOC2012/Annotations/'
image_dir = '/media/ddd/Seagate Expansion Drive/fromElop/Noga/Carlton_120718/Coaps/After_Noon/500/FOV_1.65/sample_13/VOC2012/JPEGImages/'
visualize_bbox_on_images(image_dir,ano_dir)