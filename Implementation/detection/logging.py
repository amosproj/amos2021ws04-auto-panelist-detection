import csv
import os
from datetime import datetime


class Logger:
    @staticmethod
    def log(idx, gender, age, emotion, attentiveness):
        with open('logs.csv', 'a+', newline='') as csvfile:
            fieldnames = ['timestamp', 'id', 'gender', 'age', 'emotion', 'attentiveness']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            if os.stat("logs.csv").st_size == 0:
                # file is empty, add header
                writer.writeheader()

            writer.writerow({
                'timestamp': '{:%Y-%m-%d %H:%M:%S}'.format(datetime.now()),
                'id': idx,
                'gender': gender,
                'age': age,
                'emotion': emotion,
                'attentiveness': attentiveness,
            })
