from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import os

""" The function 'calculate()' is the starting point of the calculation process. """

paths = {'user_stats': './statistics/user_stats.csv', 'gender_stats': './statistics/gender_stats.csv',
         'age_stats': './statistics/age_stats.csv', 'watchtime_by_day': './statistics/watchtime_day_stats.csv'}


# Clean/delete statistics files
def init():
    for p in paths:
        if os.path.exists(paths[p]):
            f = open(paths[p], "w+")
            f.close()


# Save row to user_stats file
def save_in_stats(id, gender, age, avg_min_per_day):
    file_path = paths['user_stats']
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


# Save row to gender_stats file
def save_in_gender_stats(id, gender, avg_age, avg_min_per_day):
    file_path = paths['gender_stats']
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


# Save row to age_stats file
def save_in_age_stats(id, age, avg_min_per_day):
    file_path = paths['age_stats']
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


# Save row to age_stats file
def save_to_avg_watchtime_per_day(id, day, watchtime_in_min):
    file_path = paths['watchtime_by_day']
    with open(file_path, 'a+', newline='') as csvfile:
        fieldnames = ['id', 'day', 'watchtime_in_min']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=',', quotechar='|',
                                quoting=csv.QUOTE_MINIMAL)

        if os.stat(file_path).st_size == 0:
            # file is empty, add header
            writer.writeheader()

        writer.writerow({
            'id': id,
            'day': day,
            'watchtime_in_min': watchtime_in_min
        })


# Plot all stats files
def plot_statistics():
    # Plot user stats
    with open(paths['user_stats'], 'r') as csvfile:
        x = []
        y = []
        csvfile.readline()
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(row[0])
            y.append(float(row[3]))

        plt.clf()
        plt.bar(x, y, color='g', width=0.72, label='Watchtime')
        plt.xlabel('User id')
        plt.ylabel('Watchtime in min')
        plt.title('Watchtime by user per day')
        plt.legend()
        plt.show()

    # Plot gender stats
    with open(paths['gender_stats'], 'r') as csvfile:
        x = []
        y = []
        csvfile.readline()
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(row[1])
            y.append(float(row[2]))

        plt.bar(x, y, color='r', width=0.72, label='Watchtime')
        plt.xlabel('Gender')
        plt.ylabel('Watchtime in min')
        plt.title('Watchtime by gender per day')
        plt.legend()
        plt.show()
        plt.clf()

    # Plot age stats
    with open(paths['age_stats'], 'r') as csvfile:
        x = []
        y = []
        csvfile.readline()
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            x.append(row[1])
            y.append(float(row[2]))

        plt.bar(x, y, color='b', width=0.72, label='Watchtime')
        plt.xlabel('Age')
        plt.ylabel('Watchtime in min')
        plt.title('Watchtime by age per day')
        plt.legend()
        plt.show()
        plt.clf()

    # Plot watchtime/day stats
    with open(paths['watchtime_by_day'], 'r') as csvfile:
        x = []
        y = []
        csvfile.readline()
        plots = csv.reader(csvfile, delimiter=',')
        ploted_days = 7
        counter = 0
        for row in plots:
            if counter == ploted_days:
                break
            x.append(row[1])
            y.append(float(row[2]))
            counter = counter + 1

        plt.bar(x, y, color='y', width=0.72, label='Watchtime')
        plt.xlabel('Day')
        plt.ylabel('Watchtime in min')
        plt.title('Total watchtime per day')
        plt.legend()
        plt.show()
        plt.clf()


# TODO: Watchtime by user per day
# How should the avg per day be calculated ?

# All "calculate" functions save the data in csv files using the save_... functions
def calculate_watchtime_by_user(print_to_console):
    # Get all unique ids from the logs
    sheet = pd.read_csv('./logs.csv', delimiter=',')
    if sheet.empty:
        print('There is not enough data to calculate statistics!')
        return
    users_id = np.sort(sheet['id'].unique())
    for i in users_id:
        # Get all logs for user with id i
        user_logs = sheet[sheet['id'] == i].sort_values(by=['timestamp'])
        if len(user_logs) <= 1 and print_to_console:
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

        # Now save the entry in the user_stats.csv
        avg_day = float("{0:.3f}".format(total_watchtime / len(log_days) / 60))
        save_in_stats(i, user_logs.iloc[0]['gender'], user_logs.iloc[0]['age'], avg_day)

        if print_to_console:
            print("-- User_id: ", i, "---------------------------------------------------")
            print("-- avg min per day: ", avg_day)
            print("-- avg min per week: ", avg_day * 7)
            print("-- avg min per month: ", avg_day * 7 * 4)
            print("------------------------------------------------------------------")


#
def calculate_watchtime_by_gender(print_to_console):
    sheet = pd.read_csv(paths['user_stats'], delimiter=',')
    idg = 0
    for g in ['w', 'm', 'n']:
        group_logs = sheet[sheet['gender'] == g]
        avg_watchtime = float("{0:.3f}".format(group_logs['avg_min_per_day'].sum() / len(group_logs)))
        avg_age = group_logs['age'].sum() / len(group_logs)
        save_in_gender_stats(idg, g, avg_age, avg_watchtime)
        idg = idg + 1
        if print_to_console:
            print("-- Gender: ", g, " ----------------------------------------------------")
            print("-- avg age: ", avg_age)
            print("-- avg min per day: ", avg_watchtime)
            print("-- avg min per week: ", avg_watchtime * 7)
            print("-- avg min per month: ", avg_watchtime * 7 * 4)
            print("------------------------------------------------------------------")


#
def calculate_watchtime_by_age(print_to_console):
    sheet = pd.read_csv(paths['user_stats'], delimiter=',')
    ages = np.sort(sheet['age'].unique())
    ida = 0
    for k in ages:
        age_logs = sheet[sheet['age'] == k]
        avg_watchtime = float("{0:.3f}".format(age_logs['avg_min_per_day'].sum() / len(age_logs)))
        save_in_age_stats(ida, k, avg_watchtime)
        ida = ida + 1
        if print_to_console:
            print("-- Age: ", k, " -----------------------------------------------------")
            print("-- avg watchtime: ", avg_watchtime)
            print("------------------------------------------------------------------")


#
def calculate_avg_watchtime_per_day():
    # Get all unique ids from the logs
    sheet = pd.read_csv('./logs.csv', delimiter=',')
    if sheet.empty:
        print('There is not enough data to calculate statistics!')
        return

    # Get watchtime for every day and add it to total_watchtime
    log_days = sheet['timestamp'].str.replace(r'\s.*', '', regex=True)
    log_days = np.sort(log_days.unique())

    users_id = np.sort(sheet['id'].unique())
    max_time_diff = 60 * 6  # Max. difference in sec between two logs to count
    id = 0
    for day in log_days:
        total_watchtime = 0
        one_day_logs = sheet[sheet['timestamp'].str[0:10] == day].sort_values(by=['timestamp'])
        for i in users_id:
            one_user_logs = one_day_logs[one_day_logs['id'] == i]
            if one_user_logs.empty or len(one_user_logs) < 2:
                continue

            k = 0
            j = 1
            first_log = datetime.strptime(one_user_logs.iloc[0]['timestamp'], '%Y-%m-%d %H:%M:%S')
            while True:
                tmp_log = datetime.strptime(one_user_logs.iloc[k]['timestamp'], '%Y-%m-%d %H:%M:%S')
                next_log = datetime.strptime(one_user_logs.iloc[j]['timestamp'], '%Y-%m-%d %H:%M:%S')

                if j < len(one_user_logs) - 1:
                    if (next_log - tmp_log).seconds < max_time_diff:
                        j = j + 1
                        k = k + 1
                    else:
                        total_watchtime = total_watchtime + (tmp_log - first_log).seconds
                        first_log = datetime.strptime(one_user_logs.iloc[j]['timestamp'], '%Y-%m-%d %H:%M:%S')
                        j = j + 1
                        k = k + 1
                else:
                    total_watchtime = total_watchtime + (next_log - first_log).seconds
                    break

        # Now save the entry in the test_stats.csv
        avg_day = float("{0:.4f}".format(total_watchtime / 60))
        save_to_avg_watchtime_per_day(id, day, avg_day)
        id = id + 1


# Starting point
def calculate(print_to_console=False, plot_stats=True):
    # Cleanup
    # delete all existing _stats.csv files
    init()

    # Calculate avg for all users with the info from the logs and store it in user_stats.csv
    # The next two functions (by_gender/by_age) have to be executed after this one!
    calculate_watchtime_by_user(print_to_console)

    # Now in a new csv save the data for watchtime by gender, and store it in gender_stats.csv
    calculate_watchtime_by_gender(print_to_console)

    # In a new csv save the data for watchtime by age, and store it in age_stats.csv
    calculate_watchtime_by_age(print_to_console)

    # Calculate watching time per day
    calculate_avg_watchtime_per_day()

    if plot_stats:
        plot_statistics()
