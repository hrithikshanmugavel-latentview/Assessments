# -*- coding: utf-8 -*-
"""Classification-Final-Assessment

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CzbD-f4e3l460ZvtrK-lchZF2aNQ0Wat
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import warnings
warnings.filterwarnings("ignore")

## Loading Data

df = pd.read_csv("/content/penguins_classification.csv")
df.head()

## Data Preprocessing

df.shape

df.info()

df.describe(include="all").T

df.info()

df.isnull().sum()

df['bill_depth_mm'].fillna(df['bill_depth_mm'].mean(), inplace=True)

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

## Handling Outliers

for column in df.select_dtypes(include=['float64','int64']):
  sns.boxplot(df[column])
  plt.show()


for column in df.select_dtypes(include = "number"):
  q1 = df[column].quantile(0.25)
  q3 = df[column].quantile(0.75)
  iqr = q3-q1
  lower = q1 - 1.5*iqr
  upper = q3 + 1.5* iqr
  df[column] = df[column].clip(lower = lower, upper= upper)

from sklearn.preprocessing import LabelEncoder, MinMaxScaler

le = LabelEncoder()

for col in df.select_dtypes(include=["object"]).columns:
  df[col] = le.fit_transform(df[col])

df.head()

correlation_matrix = df.corr()

correlation_matrix

plt.figure(figsize=(8, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

# x = df.drop('fare_amount', axis=1)

x = df.drop('species', axis=1)
y = df['species']

from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)

mn = MinMaxScaler()
x_train = mn.fit_transform(x_train)
x_test = mn.transform(x_test)

from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()

model.fit(x_train, y_train)

y_pred = model.predict(x_test)

from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

acc = accuracy_score(y_test, y_pred)
cr = classification_report(y_test, y_pred)

print(acc)
print(cr)

conf_mat = confusion_matrix(y_test, y_pred)
print(conf_mat)