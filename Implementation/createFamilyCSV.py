import pandas as pd


col_names = ['First Name', 'Last Name', 'Age', 'Gender', 'Photo']

data_1 = {'ID': [0], 'First Name': "Max", 'Last Name': "Mustermann", 'Age': 30, 'Gender': 'm', 'Photo': "/home/airtrake/Bilder/family.jpeg", 'E-Mail': "musterman@hotmail.de"}

family = pd.DataFrame(data_1)
family.to_csv('./database/family.csv', index=False)

print(family)