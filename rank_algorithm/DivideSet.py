import time

import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split



def split_dataset_randomly(filename, test_size=0.1):
    df = pd.read_excel(filename)
    ioc_values = df['ioc_value']
    return train_test_split(ioc_values, test_size=test_size, random_state=int(time.time()))


def split_dataset_average(filename, test_size=0.1, random_state=int(time.time())):
    df = pd.read_excel(filename)
    ioc_values = df['ioc_value']
    categories = df['category']
    unique_categories = categories.unique()
    train_ioc_values = []
    test_ioc_values = []

    for category in unique_categories:
        category_indices = np.where(categories == category)[0]
        category_ioc_values = ioc_values[category_indices]

        train_ioc_values_cat, test_ioc_values_cat = train_test_split(category_ioc_values, test_size=test_size,
                                                                     random_state=random_state)
        train_ioc_values.extend(train_ioc_values_cat)
        test_ioc_values.extend(test_ioc_values_cat)

    return train_ioc_values, test_ioc_values


def custom_split_on_category(filename, category_values):
    df = pd.read_excel(filename)
    train_df = df[~df['category'].isin(category_values)]
    test_df = df[df['category'].isin(category_values)]

    return train_df['ioc_value'], test_df['ioc_value']


train_ioc_values, test_ioc_values = split_dataset_randomly('high_value_TI.xlsx')

with open('train_set.txt', 'w') as train_file:
    for value in train_ioc_values:
        train_file.write(str(value) + '\n')

with open('test_set.txt', 'w') as test_file:
    for value in test_ioc_values:
        test_file.write(str(value) + '\n')
