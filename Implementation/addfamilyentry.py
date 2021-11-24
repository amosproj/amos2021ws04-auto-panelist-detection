import pandas as pd

col_names = ['ID', 'First Name', 'Last Name', 'Age', 'Gender', 'Photo']


def addfamilyentry(ID, fName, lName, age, gender, photo):
    old_df = pd.read_csv('./database/family.csv')

    new_data = {'ID': [ID], 'First Name': fName, 'Last Name': lName, 'Age': age, 'Gender': gender,
                'Photo': photo}

    new_df = pd.DataFrame(new_data)

    m_df = old_df.append(new_df)
    m_df.to_csv("./database/family.csv", index=False)

def __init__(self):
    return