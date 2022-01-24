from datetime import datetime, timedelta
import pandas as pd
import numpy as np
import csv
import os


def init():
    # Clean statistics files
    paths = ['./statistics/general_statistics.csv', './statistics/gender_statistics.csv',
             './statistics/age_statistics.csv']
    for p in paths:
        if os.path.exists(p):
            f = open(p, "w+")
            f.close()


def save_in_statistics(id, gender, age, avg_min_per_day):
    file_path = './statistics/general_statistics.csv'
    with open(file_path, 'a+', newline='') as csvfile:
        fieldnames = ['id', 'gender', 'age', 'avg_min_per_day']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)

        if os.stat(file_path).st_size == 0:
            # file is empty, add header
            writer.writeheader()

        writer.writerow({
            'id': id,
            'gender': str(gender)[0].lower(),
            'age': age,
            'avg_min_per_day': avg_min_per_day
        })


def save_in_gender_statistics(id, gender, avg_age, avg_min_per_day):
    file_path = './statistics/gender_statistics.csv'
    with open(file_path, 'a+', newline='') as csvfile:
        fieldnames = ['id', 'gender', 'avg_age', 'avg_min_per_day']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)

        if os.stat(file_path).st_size == 0:
            # file is empty, add header
            writer.writeheader()

        writer.writerow({
            'id': id,
            'gender': gender,
            'avg_age': avg_age,
            'avg_min_per_day': avg_min_per_day
        })


def save_in_age_statistics(id, age, avg_min_per_day):
    file_path = './statistics/age_statistics.csv'
    with open(file_path, 'a+', newline='') as csvfile:
        fieldnames = ['id', 'age', 'avg_min_per_day']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)

        if os.stat(file_path).st_size == 0:
            # file is empty, add header
            writer.writeheader()

        writer.writerow({
            'id': id,
            'age': age,
            'avg_min_per_day': avg_min_per_day
        })


def calculate(print_data=False):
    # Cleanup
    init()

    # Get all unique ids from the logs
    sheet = pd.read_csv('./logs.csv', delimiter=',')
    users_id = np.sort(sheet['id'].unique())
    for i in users_id:
        # Get all logs for user with id i
        user_logs = sheet[sheet['id'] == i].sort_values(by=['timestamp'])
        if len(user_logs) <= 1 and print_data:
            print("-- User_id: ", i, " avg time is unknown ------------------------------")

        # Get watchtime for every day and add it to total_watchtime
        log_days = user_logs['timestamp'].str.replace(r'\s.*', '', regex=True)
        log_days = log_days.unique()
        total_watchtime = 0
        for j in log_days:
            one_day_logs = user_logs[user_logs['timestamp'].str[0:10] == j]
            first_log = datetime.strptime(one_day_logs.iloc[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
            last_log = datetime.strptime(one_day_logs.iloc[-1]['timestamp'], '%Y-%m-%d %H:%M:%S')
            total_watchtime = total_watchtime + (last_log - first_log).seconds

        # Now save the entry in the general_statistics.csv
        avg_day = float("{0:.3f}".format(total_watchtime / len(log_days) / 60))
        save_in_statistics(i, user_logs.iloc[0]['gender'], user_logs.iloc[0]['age'], avg_day)

        if print_data:
            print("-- User_id: ", i, "---------------------------------------------------")
            print("-- avg min per day: ", avg_day)
            print("-- avg min per week: ", avg_day * 7)
            print("-- avg min per month: ", avg_day * 7 * 4)
            print("------------------------------------------------------------------")

    # Now in a new csv save the data for watchtime by gender
    new_sheet = pd.read_csv('./statistics/general_statistics.csv', delimiter=',')
    idg = 0
    for g in ['w', 'm', 'n']:
        group_logs = new_sheet[new_sheet['gender'] == g]
        avg_watchtime = float("{0:.3f}".format(group_logs['avg_min_per_day'].sum() / len(group_logs)))
        avg_age = group_logs['age'].sum() / len(group_logs)
        save_in_gender_statistics(idg, g, avg_age, avg_watchtime)
        idg = idg + 1
        if print_data:
            print("-- Gender: ", g, " ----------------------------------------------------")
            print("-- avg age: ", avg_age)
            print("-- avg min per day: ", avg_watchtime)
            print("-- avg min per week: ", avg_watchtime * 7)
            print("-- avg min per month: ", avg_watchtime * 7 * 4)
            print("------------------------------------------------------------------")

    # Finally in a new csv save the data for watchtime by age
    another_sheet = pd.read_csv('./statistics/general_statistics.csv', delimiter=',')
    ages = np.sort(another_sheet['age'].unique())
    ida = 0
    for k in ages:
        age_logs = another_sheet[another_sheet['age'] == k]
        avg_watchtime = float("{0:.3f}".format(age_logs['avg_min_per_day'].sum() / len(age_logs)))
        save_in_age_statistics(ida, k, avg_watchtime)
        ida = ida + 1
        if print_data:
            print("-- Age: ", k, " -----------------------------------------------------")
            print("-- avg watchtime: ", avg_watchtime)
            print("------------------------------------------------------------------")
