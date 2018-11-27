# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 14:55:43 2015
This script is to convert the txt annotation files to appropriate format needed by YOLO 
@author: Guanghan Ning
Email: gnxr9@mail.missouri.edu
"""

import os
import io
from shutil import copyfile
from os import walk, getcwd
from PIL import Image

classes = ["001","002","003","004","005"]

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
    
    
"""-------------------------------------------------------------------""" 

""" Configure Paths"""
obj='nlut'
cls = "005"
wd = getcwd()
mypath = os.path.join(wd,"Labels",cls)
outpath = os.path.join(wd,obj,"dataset")
label_path=os.path.join(wd,obj,"annotations")

if cls not in classes:
    exit(0)
cls_id = classes.index(cls)
list_file = io.open('%s/%s_list.txt'%(wd, cls), 'w',newline='\n')

""" Get input text file list """
txt_name_list = []
for (dirpath, dirnames, filenames) in walk(mypath):
    txt_name_list.extend(filenames)
    break
print(txt_name_list)

""" Process """
for txt_name in txt_name_list:
    # txt_file =  o.open("Labels/stop_sign/001.txt", "r")
    
    """ Open input text files """
    txt_path = os.path.join(mypath,txt_name)
    print("Input:" + txt_path)
    txt_file = open(txt_path, "r")
    lines = txt_file.read().split('\r\n')   #for ubuntu, use "\r\n" instead of "\n"
    
    """ Open output text files """
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    if not os.path.exists(label_path):
        os.makedirs(label_path)
    txt_outpath = os.path.join(outpath,txt_name)
    print("Output:" + txt_outpath)
    txt_outfile = io.open(txt_outpath, "w",newline='\n')
    
    
    """ Convert the data to YOLO format """
    ct = 0
    for line in lines:
        #print('lenth of line is: ')
        #print(len(line))
        #print('\n')
        if(len(line) >= 2):
            ct = ct + 1
            print(line)
            elems = line.split('\n')[1].split(' ')
            print(elems)
            xmin = elems[0]
            xmax = elems[2]
            ymin = elems[1]
            ymax = elems[3]
            #
            img_path = str('%s/images/%s/%s.JPG'%(wd, cls, os.path.splitext(txt_name)[0]))
            xml_path = os.path.join(wd,"AnnotationsXml",str(cls),os.path.splitext(txt_name)[0]+".xml")
            print(img_path)
            #t = magic.from_file(img_path)
            #wh= re.search('(\d+) x (\d+)', t).groups()
            im=Image.open(img_path)
            w= int(im.size[0])
            h= int(im.size[1])
            #w = int(xmax) - int(xmin)
            #h = int(ymax) - int(ymin)
            # print(xmin)
            print(w, h)
            b = (float(xmin), float(xmax), float(ymin), float(ymax))
            bb = convert((w,h), b)
            print(bb)
            txt_outfile.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')
            new_img_path = os.path.join(outpath,"{0}.jpg".format(os.path.splitext(txt_name)[0]))
            new_xml_path = os.path.join(label_path,"{0}.xml".format(os.path.splitext(txt_name)[0]))
            copyfile(img_path, new_img_path)
            copyfile(xml_path, new_xml_path)


    """ Save those images with bb into list"""
    if(ct != 0):
        list_file.write('%s/images/%s/%s.JPG\n'%(wd, cls, os.path.splitext(txt_name)[0]))
                
list_file.close()