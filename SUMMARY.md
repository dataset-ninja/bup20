**BUP19: Sweet Pepper Dataset** is a dataset for instance segmentation, semantic segmentation, object detection, and monocular depth estimation tasks. It is used in the agricultural and robotics industries. 

The dataset consists of 560 images with 29106 labeled objects belonging to 7 different classes including *green*, *yellow*, *mixed yellow*, and other: *red*, *mixed red*, *pepper kp*, and *mixed*.

Images in the BUP20 dataset have pixel-level instance segmentation and bounding box annotations. Due to the nature of the instance segmentation task, it can be automatically transformed into a semantic segmentation task (only one mask for every class). All images are labeled (i.e. with annotations). There are 3 splits in the dataset: *train* (248 images), *test* (186 images), and *val* (126 images). Alternatively, the dataset could be split into 5 row: ***row4*** (126 images), ***row2*** (124 images), ***row3*** (124 images), ***row5*** (124 images), and ***row6*** (62 images), or into 2 date: ***20201001*** (310 images) and ***20200924*** (250 images), or into 5 labeller: ***ramsay*** (10704 objects), ***claus smitt*** (7090 objects), ***chris mccool*** (5852 objects), ***michallhal*** (3342 objects), and ***agr user1*** (2118 objects). Additionally, images are grouped by ***im id***. Also, every image marked with ***odometry*** tag, every image and label contain ***milliseconds*** tag. Explore it in supervisely labeling tool. The dataset was released in 2020 by the University of Bonn, Germany.

Here are the visualized examples for the classes:

[Dataset classes](https://github.com/dataset-ninja/bup20/raw/main/visualizations/classes_preview.webm)
