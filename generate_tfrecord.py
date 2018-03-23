#!/usr/bin/env python
# encoding: utf-8
"""
Usage:
  # From tensorflow/models/
  # Create train data:
  python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=train.record --image_path=train_images/JPEGImages 

  # Create test data:
  python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=test.record --image_path=test_images/JPEGImages
"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import os
import io
import sys
import pandas as pd
import tensorflow as tf

from PIL import Image
#from object_detection.utils import dataset_util
import dataset_util
from collections import namedtuple, OrderedDict

flags = tf.app.flags
flags.DEFINE_string('csv_input', '', 'Path to the CSV input')
flags.DEFINE_string('output_path', '', 'Path to output TFRecord')
flags.DEFINE_string('image_path', '', 'Path to JPEG image folder')
FLAGS = flags.FLAGS
CLASS_NAMES = "map.txt"

try:
    with open(CLASS_NAMES, 'r') as f:
        label_map = f.readlines()
        #print(label_map)
except IOError as e:
    sys.exit("I/O error({0}): {1}".format(e.errno, e.strerror))
except: #handle other exceptions such as attribute errors
    sys.exit("Unexpected error:", sys.exc_info()[0])


def class_text_to_int(row_label):
    #if row_label == 'zombie':
        #return 1
    #elif row_label == 'person':
        #return 2
    #else:
        #None
    for index, value in enumerate(label_map):
        if row_label == value.strip():
            return index + 1
    return None


def split(df, group):
    data = namedtuple('data', ['filename', 'object'])
    gb = df.groupby(group)
    return [data(filename, gb.get_group(x)) for filename, x in zip(gb.groups.keys(), gb.groups)]


def create_tf_example(group, path):
    with tf.gfile.GFile(os.path.join(path, '{}'.format(group.filename)), 'rb') as fid:
        encoded_jpg = fid.read()
    encoded_jpg_io = io.BytesIO(encoded_jpg)
    image = Image.open(encoded_jpg_io)
    width, height = image.size

    filename = group.filename.encode('utf8')
    image_format = b'jpg'
    xmins = []
    xmaxs = []
    ymins = []
    ymaxs = []
    classes_text = []
    classes = []

    for index, row in group.object.iterrows():
        xmins.append(row['xmin'] / width)
        xmaxs.append(row['xmax'] / width)
        ymins.append(row['ymin'] / height)
        ymaxs.append(row['ymax'] / height)
        classes_text.append(row['class'].encode('utf8'))
        classes.append(class_text_to_int(row['class']))

    tf_example = tf.train.Example(features=tf.train.Features(feature={
        'image/height': dataset_util.int64_feature(height),
        'image/width': dataset_util.int64_feature(width),
        'image/filename': dataset_util.bytes_feature(filename),
        'image/source_id': dataset_util.bytes_feature(filename),
        'image/encoded': dataset_util.bytes_feature(encoded_jpg),
        'image/format': dataset_util.bytes_feature(image_format),
        'image/object/bbox/xmin': dataset_util.float_list_feature(xmins),
        'image/object/bbox/xmax': dataset_util.float_list_feature(xmaxs),
        'image/object/bbox/ymin': dataset_util.float_list_feature(ymins),
        'image/object/bbox/ymax': dataset_util.float_list_feature(ymaxs),
        'image/object/class/text': dataset_util.bytes_list_feature(classes_text),
        'image/object/class/label': dataset_util.int64_list_feature(classes),
    }))
    return tf_example

def usage():
    sys.exit("Usage:python generate_tfrecord.py --csv_input xxx --output_path xxx --image_path xxx")

def main(_):
    writer = tf.python_io.TFRecordWriter(FLAGS.output_path)
    #path = os.path.join(os.getcwd(), 'images')
    #path = os.path.join(os.getcwd(), 'zombie_val_images', 'jpegimages')
    if FLAGS.csv_input == '' or FLAGS.output_path == '' or FLAGS.image_path == '':
        usage()
        
    path = FLAGS.image_path
    if not os.path.isdir(path):
        sys.exit("Error: plz provide a legal image path")
    examples = pd.read_csv(FLAGS.csv_input)
    grouped = split(examples, 'filename')
    for group in grouped:
        tf_example = create_tf_example(group, path)
        writer.write(tf_example.SerializeToString())

    writer.close()
    output_path = os.path.join(os.getcwd(), FLAGS.output_path)
    print('Successfully created the TFRecords: {}'.format(output_path))


if __name__ == '__main__':
    tf.app.run()
