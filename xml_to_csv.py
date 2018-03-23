#!/usr/bin/env python
# encoding: utf-8
"""
Usage:
  # From tensorflow/models/
  # Create csv data:
  python xml_to_csv.py --csv_output=train_labels.csv  --annotation_path=train_images/Annotations
"""

import os
import sys
import glob
import pandas as pd
import tensorflow as tf
import xml.etree.ElementTree as ET

flags = tf.app.flags
flags.DEFINE_string('csv_output', '', 'Path to the CSV output')
flags.DEFINE_string('annotation_path', '', 'Path to input image annotation path')
FLAGS = flags.FLAGS

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        #print(xml_file)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                        int(root.find('size').find('width').text),
                        int(root.find('size').find('height').text),
                        member[0].text,
                        int(member.find('bndbox').find('xmin').text),
                        int(member.find('bndbox').find('ymin').text),
                        int(member.find('bndbox').find('xmax').text),
                        int(member.find('bndbox').find('ymax').text)
                        )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df

def help():
    sys.exit("Usage: python xml_to_csv.py --annotation_path xxx --csv_output xxx")

def main():
    if FLAGS.annotation_path == '' or FLAGS.csv_output == '':
        help()
    image_path = FLAGS.annotation_path
    if not os.path.isdir(image_path):
        sys.exit("Error: invalid annotation path. ")
    xml_df = xml_to_csv(image_path)
    xml_df.to_csv(FLAGS.csv_output, index=None)
    print('Successfully converted xml to csv.')


main()
