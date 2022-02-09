# Automatic Panelist Detection (AMOS WS 2021)
 <!--- ![team_logo](/Deliverables/sprint-01-team-logo.png) ---> 
 <p align="center">
 <img src="/Deliverables/sprint-01-team-logo.png" width="300" height="300">
 </p>
The goal of this project is to create a cheap yet efficient device to optimize television audience measurement. This will be achieved by automatically detecting and recognizing panelists using pre-trained computer vision models and an RGB and infrared camera. All household panelists can be registered in a local database to facilitate the recognition process. Alongside gender and age, attentiveness and emotions will also be assessed. To account for user privacy, the gathered data is anonymized and sent to a GfK server. The device is not only non-intrusive but also time and power-efficient. It should also work under diffficult lighting conditions.

## Project Setup
- Clone this project to your local disk.
- Create and enable your python virtual enviroment.
- Run `pip install -r requirements.txt`.

## Run Program
The Automatic Panelist Detection program can be started using the following commands:

    cd Implementation
    python main.py

The logged data can be received either via a REST api or via the MQTT protocol. This can be specified by setting the `API` parameter in the `Implementation/main.py` file.
For MQTT, the `Implementation/api/transmission.py` file needs to be modified and your MQTT broker, username and password should be provided there.
The `CAMERA` parameter in the `gui/gui.py file` can be modified to specify which camera should be used.

## Create Performance Reports
Performance reports for using different images and recognition models can be created automatically using the following command:

    cd Implementation
    python benchmark.py

This creates two reports: One for the detection benchmark and one for the recognition as well as the age, gender, and emotion detection benchmark.
Both reports are saved as .xlsx (containing the tested images) and .csv files.

The images used for both benchmarks can be specified in the respective JSON files `Implementation/test images/detection_benchmark.json` and `Implementation/test images/recognition_benchmark.json`.
These files also include the corresponding labels.

The benchmarks can be run for different scaled versions of the given images. The image scales can be set by changing the `IMG_SCLAE` parameter in the `Implementation/benchmark.py` file.

## Generate Statistics
User statistic can be generated based on the logged data using the following command:

    cd Implementation/statistics
    python calculate_statistics.py

This stores various user statistics in the `Implementation/statistics` directory. It also shows plots with the generated data.

For more information click [here](https://www.youtube.com/watch?v=dQw4w9WgXcQ).
