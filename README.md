# Prepare training dataset for Tensorflow 

## Set up environment
Make sure that all the python dependencies used by the tool are installed for using it. 

 - Install conda or miniconda (refer to the [document](https://conda.io/docs/user-guide/install/linux.html) on how to install it 
 - Run `conda env create -f environment.yml` to create the environment. You can find the `environment.yml` file in the [repo](https://github.com/ichbinblau/tfrecord_generator).
 - Activate the environment by running `source activate tfrecord_dataset`

## Label Images

 - Resize images to unified size. The max width or height of VOC images are 500px. If the image size is too big, it requires larger memory to load these images. You may find it difficult to use a bigger batch size due to memory constraints. Put `resize.py` in the same folder with the images and run `python resize.py`. All the images will be resized and saved in **resized** folder.
 - Go to download the [labelImg](https://github.com/tzutalin/labelImg) tool from Github
 - Label objects in images
- Keep the images in folder named **JPEGImages** and labels in folder called **Annotations**. The folder structure should be like below. Replace test with any name you want, such as zombie_train_images etc. 

        test_train_images 
        |----JPEGImages
    		    |----0001.jpg
    			 ----0002.jpg
    			 ----...
    			 ----0100.jpg  
        |---Annotations
              |----0001.xml
               ----0002.xml
               ----...
               ----0100.xml  
       test_val_images
       |----JPEGImages
    		    |----0001.jpg
    			 ----0002.jpg
    			 ----...
    			 ----0100.jpg  
        |---Annotations
              |----0001.xml
               ----0002.xml
               ----...
               ----0100.xml  

## Create tensorflow's record file
Labelled training images and annotations are supposed to be converted to record files.  Based on the scripts in this [post](https://github.com/datitran/raccoon_dataset), I made the script more automated. 

 - Check out the [repo](https://github.com/ichbinblau/tfrecord_generator)
 - Copy `test_train_images` and `test_val_images` folder to under the **tfrecord_generator** folder 
 - Change the classes in `map.txt` under **tfrecord_generator** folder. Remove the default classes and add one class per line. eg. 
    zombie
    person
    bigfoot
 - Run script `./create_record.sh test` . Replace `test` with the prefix of the training images folder name. For instance, if the training and evaluation folder named "test2_train_images" and "test2_val_images", replace the parameter with `test2` instead of `test`.
 - Voila, you will see two record files named `test_train.record` and `test_val.record`respectively in the same folder
 
 
You can find more info on how to enable GPU graphic card and how to train models in these two wiki pages.
- [Install tensorflow gpu 1.6 for Ubuntu 16.04](https://github.com/ichbinblau/tfrecord_generator/wiki/Install-tensorflow-gpu-1.6-for-Ubuntu-16.04)
- [Train your own model with SSD MobileNet](https://github.com/ichbinblau/tfrecord_generator/wiki/Train-your-own-model-with-SSD-MobileNet)

