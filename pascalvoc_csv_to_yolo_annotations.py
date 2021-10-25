from glob import glob
import os
import pickle
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm
import cv2
import csv


def resize_img(img, scale_percent=50):
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)
    return img_resized


##### Define input variables #######
CWD = os.getcwd()
IMG_FOLDER = os.path.join(CWD, 'input_images')
IMG_EXT = '.jpg'
ANNOT_EXT = '.xml'
OUT_FOLDER = os.path.join(IMG_FOLDER, 'yolo_annot')
IMG_TAGS = ['train','test']
rect_offset = 5
####################################

if not os.path.OUT_FOLDER(OUT_FOLDER):
    os.makedirs(IMG_FOLDER)

image_paths = glob(os.path.join(IMG_FOLDER, '*'+IMG_EXT))

for img_tag in IMG_TAGS:
    csv_name = img_tag + '_labels' + ANNOT_EXT
    df = pd.read_csv(os.path.join(IMG_FOLDER, csv_name))
    # print(df.head())
    
    # Do not open image again if it was previously opened
    old_name = None
    counter = 0
    for index, row in tqdm(df.iterrows()):
        new_name = row['filename']
        if new_name == old_name:
            counter += 1
        else:
            try:
                txt_file.close()
            except:
                pass

            txt_filename = os.path.join(OUT_FOLDER, new_name.split('.')[0] + '.txt')
            txt_file =  open(txt_filename, "w")
            
            old_name = new_name
            counter = 0

        img_w = row['width']
        img_h = row['height']

        x = "{:.6f}".format(round(((row['xmin'] + row['xmax']) // 2) / img_w, 6))
        y = "{:.6f}".format(round(((row['ymin'] + row['ymax']) // 2) / img_h, 6))
        w = "{:.6f}".format(round((row['xmax'] - row['xmin']) / img_w, 6))
        h = "{:.6f}".format(round((row['ymax'] - row['ymin']) / img_h, 6))

        assert (all(float(i) <= 1 for i in [x,y,w,h]) == True)

        # cv2.rectangle(img, (row['xmin'], row['ymin']), (row['xmax'], row['ymax']), (0,255,0), 10)
        # cv2.circle(img, (int((row['xmin'] + row['xmax'])/2), int((row['ymin'] + row['ymax'])/2)), 20, (255,0,255),-1)

        # # <x> <y> <width> <height>
        txt_file.write(' '.join([str(0), x, y, w, h]))
        txt_file.write('\n')

    # txt_file.close()
    cv2.destroyAllWindows()