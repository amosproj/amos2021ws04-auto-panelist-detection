# Build and Deploy Documentation


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
