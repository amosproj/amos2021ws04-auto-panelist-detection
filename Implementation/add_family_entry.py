import pandas as pd
import os

col_names = ['ID', 'First Name', 'Last Name', 'Age', 'Gender']


def add_family_entry(idx, fName, lName, age, gender):
    if not os.path.isfile('./database/family.csv'):
        old_df = pd.DataFrame()
    else:
        old_df = pd.read_csv('./database/family.csv')

    new_data = {'ID': [idx], 'First_Name': fName, 'Last_Name': lName, 'Age': age, 'Gender': gender}

    new_df = pd.DataFrame(new_data)

    m_df = old_df.append(new_df)
    m_df.to_csv("./database/family.csv", index=False)


def get_member(name):
    df = pd.read_csv("./database/family.csv")
    idx = df.index[df['First_Name'] == name].tolist()[0]
    entries = df.iloc[idx, :]
    return entries[0], entries[3], entries[4]


# taken from deleted file -savefamilyinformation.py, probably for testing pourposes
def save_family_information():
    add_family_entry("Bernd", "Lütke", 24, 'm', "empty")
    add_family_entry("Sarah", "Lütke", 22, 'w', "empty")
