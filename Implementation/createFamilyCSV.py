import pandas as pd
import numpy as np


col_names = ['First Name', 'Last Name', 'Age', 'Gender', 'Photo']

data_1 = {'ID': [0], 'First Name': "Max", 'Last Name': "Mustermann", 'Age': 30, 'Gender': 'm', 'Photo': "empty"}

family = pd.DataFrame(data_1)


family.to_csv("family.csv", index=False)

print(family)

