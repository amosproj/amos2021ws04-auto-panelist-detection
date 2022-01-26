import pandas as pd
import os


class Database:
    def __init__(self):
        self.db_file = './../database/family.csv'

    # Changing database path
    def set_env(self):
        self.db_file = './database/family.csv'

    # Add new entry to databse
    def add_family_entry(self, idx, name, age, gender, fixed=True):
        if not os.path.isfile(self.db_file):
            old_df = pd.DataFrame()
        else:
            old_df = pd.read_csv(self.db_file)

        # Set iteration to 0 if the new data is fixed (user input)
        if fixed:
            new_data = {'ID': [idx], 'Nickname': name, 'Age': age, 'Gender': gender, 'Iteration': 0}
        # Set iteration to 1 if the new data is not fixed (not a user input)
        else:
            new_data = {'ID': [idx], 'Nickname': name, 'Age': age, 'Gender': gender, 'Iteration': 1}

        new_df = pd.DataFrame(new_data)
        m_df = old_df.append(new_df)
        m_df.to_csv(self.db_file, index=False)

    # Update entry based on name and return corresponding id
    def update_family_entry(self, name, age, gender, fixed=True):
        old_df = pd.read_csv(self.db_file)
        old_id = old_df[old_df['Nickname'] == name].ID.item()

        # If input from user: data should be fixed -> it = 0
        if fixed:
            it = 0
        # If input not from user: data should be updated with every iteration -> increase iteration count by 1
        else:
            it = old_df[old_df['Nickname'] == name].Iteration.item() + 1

        old_df = old_df[old_df.Nickname != name]

        new_data = {'ID': [old_id], 'Nickname': name, 'Age': age, 'Gender': gender, 'Iteration': it}
        new_df = pd.DataFrame(new_data)
        m_df = old_df.append(new_df)
        m_df.to_csv(self.db_file, index=False)

        return id

    # Update name in database
    def update_name(self, old_name, new_name):
        old_df = pd.read_csv(self.db_file)

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
        m_df.to_csv(self.db_file, index=False)

    # Returns True if name exists in database
    def check_member_exists(self, name):
        if not os.path.isfile(self.db_file):
            return False
        df = pd.read_csv(self.db_file)
        return name in df.Nickname.values

    # Returns id, age, gender, and iteration based on name
    def get_member(self, name):
        df = pd.read_csv(self.db_file)
        try:
            idx = df.index[df['Nickname'] == name].tolist()[0]
            entries = df.iloc[idx, :]
        except IndexError:
            print('{} was detected but not found in the database.'.format(name))
            entries = [0, name, 0, 0, 0]
        return entries[0], entries[2], entries[3], entries[4]

    # Returns a list of all used ids
    def get_ids(self):
        df = pd.read_csv(self.db_file)
        return df.ID.values
