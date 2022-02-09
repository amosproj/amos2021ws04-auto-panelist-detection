# User/Design/Build Documentation 
  Here is the User/Design/Build Documentation for AMOS Project Auto-Panelist-Detection

## User Documentation


The set up of the panelist-detection-device requires only a few simple steps:

-   First you have to connect the device to the electrical outlet.
-   Then that you use the other cable to connect the device to the TV.

If you did these two steps correctly, a green light should appear on the device if you start the TV. This means the device is turned on and is already diligently detecting panelists.

**IMPORTANT**: Adjust the device in a way that the built-in-camera is facing in the same direction as the TV and nothing is blocking its view!

You don't have to set the system manually, the camera detects all faces in front of the TV and registers every new and unrecognized face. The device continues to detect panelists until the TV is turned off. If that’s the case, the green light as well as the camera turns off.

## Design Documentation
- Architecture Design
<p align="center">
<img height="150" src="https://github.com/amosproj/amos2021ws04-auto-panelist-detection/blob/main/Documentation/Design_pipeline.jpg?raw=true">
</p>

Our architecture consists of 5 different components. The first component is responsible for taking frames from the camera every 10 seconds and it should provide it in a way that it can be processed to the next component. Additionally there should be no quality loss in the process. The second component is responsible for the face detection. We are using the face recognition model provided by Adam Geitgey. The model uses dlib's state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on the "Labeled Faces in the Wild" benchmark.

After the detection, the faces will be provided to the third component which will crop the face and processes it to the next component. The fourth component is responsible for extracting further informations from the provided frame such as age, gender, emotion and attentiveness etc. . In our last component these informations will be saved locally in a database and later on, the user information will be sent to Gfk Servers anonymously.

- Code Design

Our project has different components. We use OpenCV for Capture the Frame. And Insightface 0.5 for deep face detection. For the face recognition, we use the model from Adam Geitgey.  At the same time we are looking for more efficient modules, because we want the whole thing to work on a Raspberry Pi 4 with 4GB RAM.

We have designed a Remote module for user login. Firstly, a frame capture is made for further use. OpenCV facilitate the face detection. If the face can be recognized, then the person is logged in. If not, it will be added to the database and the user will be asked to register. We also get the number of people who have been detected and how many were recognized, if they are not recognized, people are asked to register. We are currently in the process of recognizing the age, gender and emotions of the users.

Our Database is assumed to be a CSV File, in which we save Name, Age, Gender, Email and Photo of the users. Another task is we will be to send this information to GFK in encrypted form.


## Build and Deploy Documentation


Initially we are going to work on the Raspberry Pi model 4 with 4GB RAM. The programming language of the project is Python. First of all, we need to set up the Pi board with a 64 Bit OS for better TensorFlow and PyTorch support. Currently we are using the release of **raspios-bullseye-arm64** ([https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2021-11-08/](https://downloads.raspberrypi.org/raspios_arm64/images/raspios_arm64-2021-11-08/)) on the Pi board. By using the Raspberry Pi Imager (https://www.raspberrypi.com/software/), the OS files can be flashed into a SD card that is going to be inserted to the Pi board later.

  

Once the Pi board have booted successfully, a Python interpreter (version >= 3.7) will be required to be installed on the Pi board. As the **raspios-bullseye-arm64** comes out with integrated Python 3.9, then we only need to configure the python virtual environment for the project. To do that, just follow the instructions below:

  

-   Clone the project to local disk.
-   Create and enable your python virtual environment.
-   Run `pip install -r requirements.txt` to install all the required libraries.

  

Some modules must be manually installed for the raspberry pi, find the download links for them below:

tensorflow-2.8.0-cp39-cp39-linux_aarch64.whl: [Download Link](https://tubcloud.tu-berlin.de/s/tMqKL287gpx9XZ2) ( Provided by [Q-engineering](https://qengineering.eu/install-tensorflow-2.7-on-raspberry-64-os.html))

torch-1.10.0a0+git36449ea-cp39-cp39-linux_aarch64.whl: [Download Link](https://tubcloud.tu-berlin.de/s/2KiicgnmKo2wpX6) (Provided by [Q-engineering](https://github.com/Qengineering/PyTorch-Raspberry-Pi-64-OS))

Once the runtime environment setup is done, then just cd into Implementation folder and type `python main.py` to execute the script, which will start to monitor the panellist in front of the TV all the time unless the power supply ideally from the TV() is interrupted.

In the productive scenario, the program should be executed automatically when the power supply is provided to the device.

