The **BUP20: Sweet Pepper Dataset** was captured at the University of Bonn's campus Klein-Altendorf (CKA) in a commercial glasshouse. The authors propose a novel field agnostic monitoring technique that is able to operate on two different robots, in arable farmland or a glasshouse (horticultural setting). Instance segmentation forms the backbone of this approach from which object location and class, object area, and yield information can be obtained.

Note, similar **BUP20: Sweet Pepper Dataset** datasets are also available on the [DatasetNinja.com](https://datasetninja.com/):

- [BUP19: Sweet Pepper Dataset](https://datasetninja.com/bup19)

## Motivation

Farmers require a wealth of diverse and intricate information to make informed agronomic decisions related to crop management, including intervention tasks. Traditionally, this information is gathered by farmers traversing their fields or greenhouses, a process that is often time-consuming and potentially expensive. In recent years, there has been a notable surge in the adoption of robotic platforms, driven by advancements in artificial intelligence. However, these platforms are typically specialized for specific settings, such as arable farmland, or their algorithms are tailored to a singular platform, resulting in a substantial gap between existing technology and the needs of farmers.

In the realm of agricultural automation, researchers have primarily utilized broad inputs like temperature, lighting, and CO2, which serve as inputs to AI-based approaches controlling outputs like lighting and nutrients for the crop. However, there is a clear opportunity for improvement by providing more frequent and detailed inputs regarding the crop's condition.

From the perspective of stakeholders, namely farmers, monitoring plants and their ecosystem is pivotal for making well-informed management decisions. In the absence of robotics or automation, farmers must physically inspect their farms multiple times, paying close attention to critical indicators such as crop or fruit count, as well as the presence of weeds, pests, or diseases. Robotic platforms have the potential to both automate and enhance these observations, undertaking repetitive tasks with a high degree of precision.

<img src="https://github.com/dataset-ninja/bup20/assets/120389559/5f4dcb95-20fc-4afc-8bfa-356d60c8712b" alt="image" width="1000">

<span style="font-size: smaller; font-style: italic;">The agnostic monitoring algorithm provides up-to-date information to the farmer based on instance segmentation with ripeness or species information and area estimation. This assists in making more informed management decisions such as weeding or harvesting using a tracking-via-segmentation approach for yield estimation. The approach is evaluated on two robotic platforms PATHoBot (LEFT) and BonnBot-I (RIGHT) which work in significantly different environments: glasshouse or arable fields. Area estimation values are in m2.</span>

## Dataset description

There are two critical aspects to the BUP20 dataset. First, it has labeled instance segmentation masks and full temporal sequences for tracking. Second, it has important robot and scene information, such as registered depth images, camera parameters, and wheel ***odometry*** information. It consists of non-overlapping annotated images. The sweet pepper dataset was captured at the University of Bonn's campus Klein-Altendorf (CKA) in a commercial glasshouse. Images were captured on an Intel RealSense 435i camera (Intel Corporation, Santa Clara, California, USA.) with a resolution of 1280 × 720. The BUP20 dataset captured two different cultivars: Mavera (green-yellow) and Allrounder (green-red). While green dominates, there is a rich representation of all the sub-classes.

| Name        | Abbreviation | Train | Validation | Evaluation |
|-------------|--------------|-------|------------|------------|
| BUP20       |              |       |            |            |
| Red         | Rd           | 158   | 52         | 100        |
| Yellow      | Yl           | 318   | 98         | 181        |
| Green       | Gn           | 2774  | 1285       | 1466       |
| Mixed Red   | Mr           | 100   | 62         | 70         |
| Mixed Yellow| My           | 189   | 101        | 143        |


<span style="font-size: smaller; font-style: italic;">Sweet pepper dataset (BUP20).</span>

To quantitatively assess the tracking algorithm's performance, they conducted additional annotation of the data. Utilizing the provided video sequences, three annotators systematically tallied the occurrences of the five sub-classes in the image sequences, ensuring each sweet pepper was accounted for only once. This meticulous process yielded ground truth data, encompassing counts for each sub-class across an entire row.

The annotation of the BUP20 dataset presented challenges due to the potential appearance of fruit in the images from distant rows. Annotators were instructed to utilize the heat rails, situated approximately 1.05 meters from the sensor, as a reference guide. Fruits appearing beyond this reference point were excluded from the count. Despite this guideline, determining fruit location, coupled with challenges such as juvenile peppers resembling leaves and varying degrees of occlusion, introduced some ambiguity in the annotations.

| Row   | Red | Yellow | Green | Mixed Red | Mixed Yellow | Total |
|-------|-----|--------|-------|-----------|--------------|-------|
| 24-R4 | 10  | 17     | 212   | 6         | 15           | 260   |
| 24-R5 | 10  | 6      | 157   | 8         | 21           | 202   |
| 01-R4 | 13  | 24     | 231   | 9         | 15           | 292   |
| 01-R5 | 6   | 26     | 158   | 4         | 7            | 201   |
| 01-R6 | 11  | 13     | 192   | 11        | 12           | 239   |


<span style="font-size: smaller; font-style: italic;">The yield counts for the BUP20 dataset were derived from the mean and rounded values provided by three annotators, encompassing both the validation and evaluation rows.</span>