import pandas as pd
import os

db_file = './../database/family.csv'


def set_env():
    global db_file
    db_file = './database/family.csv'


def add_family_entry(idx, name, age, gender):
    if not os.path.isfile(db_file):
        old_df = pd.DataFrame()
    else:
        old_df = pd.read_csv(db_file)

    new_data = {'ID': [idx], 'Nickname': name, 'Age': age, 'Gender': gender}
    new_df = pd.DataFrame(new_data)
    m_df = old_df.append(new_df)
    m_df.to_csv(db_file, index=False)


def update_family_entry(name, age, gender):
    old_df = pd.read_csv(db_file)
    old_id = old_df[old_df['Nickname'] == name].ID.item()
    old_df = old_df[old_df.Nickname != name]

    new_data = {'ID': [old_id], 'Nickname': name, 'Age': age, 'Gender': gender}
    new_df = pd.DataFrame(new_data)
    m_df = old_df.append(new_df)
    m_df.to_csv(db_file, index=False)

    return id


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
        entries = [0, name, 0, '']
    return entries[0], entries[2], entries[3]


def get_ids():
    df = pd.read_csv(db_file)
    return df.ID.values


# taken from deleted file -savefamilyinformation.py, probably for testing pourposes
def save_family_information():
    add_family_entry("Bernd", "Lütke", 24, 'm', "empty")
    add_family_entry("Sarah", "Lütke", 22, 'w', "empty")
