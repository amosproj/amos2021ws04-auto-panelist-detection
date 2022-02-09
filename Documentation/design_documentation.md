# Design Documentation

The code is located in the `Implementation` directory. The Automatic Panelist Detection Software can be started using the `main.py` file. In this file, both the graphical user interface
and the API are started. Files that belong to the API are located in the `api` directory. The GUI is created
in the `gui/gui.py` file. Alongside displaying information about the detected people, this module handles the processing of the captured
images. For this purpose, it uses the detection and recognition functions defined in the `detection/detection.py` file.
The GUI module also provides the feature to manually update the predicted data such as the user's age. It is responsible for
storing both the manual and the predicted information of users in the user database which is the csv file `database/family.csv`. 
The communication with the database happens using the `database.py` file. It also updates
the database with every new prediction. Furthermore, it stores images of all users in the `database` directory.
With every new prediction, the GUI module calls the logging function located in the `detection/logging.py` file.
This creates a new entry in the `log.csv` file.

Benchmark reports can be created using the `benchmark.py` file. Similar to the main program it uses the detection and recognition functions defined in the `detection/detection.py` file.

Statistics can be calculated using the `statistics/calculate_statistics.py` file. For calculating the statistics it uses the `logs.csv` file that is created during the detection process.

Tests are located in the `tests.py` file that also uses the detection and recognition functions defined in the `detection/detection.py` file.