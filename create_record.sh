#!/bin/bash

function die(){
 echo "$1"
 exit 1
}

if [ "$#" == "0" ]; then
    die "Error: plz provide name."
fi

train_images=$1"_train_images"
val_images=$1"_val_images"
train_annotation_path=$train_images"/Annotations"
train_image_path=$train_images"/JPEGImages"
val_annotation_path=$val_images"/Annotations"
val_image_path=$val_images"/JPEGImages"
train_label_file=$1"_train_labels.csv"
val_label_file=$1"_val_labels.csv"
train_record=$1"_train.record"
val_record=$1"_val.record"
class_map="map.txt"

function gen_csv(){

    if [ ! -d "$train_images" -o ! -d "$val_images" ]; then
        die "Plz check if the folder $train_images and $val_images exist."
    fi
        
    if [ ! -d "$train_annotation_path" -o ! -d "$val_annotation_path" ]; then
        die "Plz check if the folder $train_annotation_path and $val_annotation_path exist."
    fi
    
    rm -f $train_label_file
    rm -f $val_label_file

    python xml_to_csv.py --annotation_path $train_annotation_path --csv_output $train_label_file || die "Failed to create csv file for $train_annotation_path"
    python xml_to_csv.py --annotation_path $val_annotation_path --csv_output $val_label_file || die "Failed to create csv file for $val_annotation_path" 
         
}

function gen_tfrecord(){
        
    if [ ! -f "$class_map" ]; then 
        die "Provide a map.txt file with all the classes for the training."
    fi
    
    python generate_tfrecord.py --csv_input $train_label_file  --output_path=$train_record --image_path=$train_image_path || die "Failed to generate tfrecord for $train_image_path"
    python generate_tfrecord.py --csv_input $val_label_file  --output_path=$val_record --image_path=$val_image_path || die "Failed to generate tfrecord for $val_image_path" 
}

gen_csv
gen_tfrecord
