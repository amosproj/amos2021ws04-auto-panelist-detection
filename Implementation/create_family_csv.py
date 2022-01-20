import pandas as pd

col_names = ['First_Name', 'Last_Name', 'Age', 'Gender']

data_1 = {'ID': [0], 'First_Name': "Max", 'Last_Name': "Mustermann", 'Age': 30, 'Gender': 'm'}

family = pd.DataFrame(data_1)
family.to_csv('./database/family.csv', index=False)

print(family)
