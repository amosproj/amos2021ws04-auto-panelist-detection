import pandas as pd
import os

db_file = './../database/family.csv'


def set_env():
    global db_file
    db_file = './database/family.csv'


def add_family_entry(idx, name, age, gender, fixed=True):
    if not os.path.isfile(db_file):
        old_df = pd.DataFrame()
    else:
        old_df = pd.read_csv(db_file)

    if fixed:
        new_data = {'ID': [idx], 'Nickname': name, 'Age': age, 'Gender': gender, 'Iteration': 0}
    else:
        new_data = {'ID': [idx], 'Nickname': name, 'Age': age, 'Gender': gender, 'Iteration': 1}
    new_df = pd.DataFrame(new_data)
    m_df = old_df.append(new_df)
    m_df.to_csv(db_file, index=False)


def update_family_entry(name, age, gender, fixed=True):
    old_df = pd.read_csv(db_file)
    old_id = old_df[old_df['Nickname'] == name].ID.item()

    if fixed:
        it = 0
    else:
        it = old_df[old_df['Nickname'] == name].Iteration.item() + 1

    old_df = old_df[old_df.Nickname != name]

    new_data = {'ID': [old_id], 'Nickname': name, 'Age': age, 'Gender': gender, 'Iteration': it}
    new_df = pd.DataFrame(new_data)
    m_df = old_df.append(new_df)
    m_df.to_csv(db_file, index=False)

    return id


def update_name(old_name, new_name):
    old_df = pd.read_csv(db_file)

    if new_name in old_df.Nickname.values:
        m_df = old_df[old_df.Nickname != old_name]
    else:
        old_id = old_df[old_df['Nickname'] == old_name].ID.item()
        old_age = old_df[old_df['Nickname'] == old_name].Age.item()
        old_gender = old_df[old_df['Nickname'] == old_name].Gender.item()
        old_it = old_df[old_df['Nickname'] == old_name].Iteration.item()

        old_df = old_df[old_df.Nickname != old_name]

        new_data = {'ID': [old_id], 'Nickname': new_name, 'Age': old_age, 'Gender': old_gender, 'Iteration': old_it}
        new_df = pd.DataFrame(new_data)
        m_df = old_df.append(new_df)
    m_df.to_csv(db_file, index=False)


def check_member_exists(name):
    if not os.path.isfile(db_file):
        return False
    df = pd.read_csv(db_file)
    return name in df.Nickname.values


def get_member(name):
    df = pd.read_csv(db_file)
    try:
        idx = df.index[df['Nickname'] == name].tolist()[0]
        entries = df.iloc[idx, :]
    except IndexError:
        print('{} was detected but not found in the database.'.format(name))
        entries = [0, name, 0, 0, 0]
    return entries[0], entries[1], entries[2], entries[3], entries[4]


def get_ids():
    df = pd.read_csv(db_file)
    return df.ID.values
