# -*- coding: utf-8 -*-
"""Regression-Final-Assessment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1_iXMP-U2zjhuAng_64b529uE70GwxhHV
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

## Loading Data

df = pd.read_csv("https://raw.githubusercontent.com/Deepsphere-AI/LVA-Batch5-Assessment/main/Fare%20prediction.csv")
df.head()

## Data Preprocessing

df.shape

df.info()

df.describe(include="all").T

df.info()

df.isnull().sum()

df.duplicated().sum()

df.drop_duplicates(inplace=True)
df.head()

## Exploratory Data Analysis

for col in df.select_dtypes(include=['float','int']).columns:
  sns.histplot(df[col], kde=True)
  plt.title(f" Histogram of {col} ")
  plt.xlabel(col)
  plt.ylabel("Frequency")
  plt.show()

for col in df.select_dtypes(include=['object']).columns:
  sns.barplot(df[col])
  plt.title(f" Bar Chart of {col} ")
  plt.xlabel(col)
  plt.ylabel("Frequency")
  plt.show()

## Bivariate Analysis

num = df.select_dtypes(include=['float','int']).columns

for i in range(len(num)):
  for j in range(i+1, len(num)):
    sns.scatterplot(data=df, x=num[i], y=num[j])
    plt.xlabel(col)
    plt.ylabel("Frequency")
    plt.show()

from sklearn.preprocessing import LabelEncoder, MinMaxScaler

le = LabelEncoder()

for col in df.select_dtypes(include=["object"]).columns:
  df[col] = le.fit_transform(df[col])

df.head()

correlation_matrix = df.corr()

correlation_matrix

plt.figure(figsize=(12, 12))
sns.heatmap(correlation_matrix, annot=True, cmap='viridis')
plt.show()

## Feature Selection

df.drop('pickup_datetime', axis=1)
df.head()

# x = df.drop('fare_amount', axis=1)

x = df[['key', 'pickup_datetime','passenger_count']]
y = df['fare_amount']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

mn = MinMaxScaler()
x_train = mn.fit_transform(x_train)
x_test = mn.transform(x_test)

from sklearn.linear_model import LinearRegression

model = LinearRegression()

model.fit(x_train, y_train)

y_pred = model.predict(x_test)

from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error

r2 = r2_score(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)


print("R-squared:", r2)
print("mse:", mse)
print("mae:", mae)

plt.scatter(y_test, y_pred, c='red', label='Actual')
plt.scatter(y_test, y_test, c='blue', label='Predicted')
plt.xlabel("Actual values")
plt.ylabel("Predicted values")
plt.plot([min(y_test), max(y_test)], [min(y_test), max(y_test)], color='black', linestyle='-', label='bestfitline')
plt.legend()
