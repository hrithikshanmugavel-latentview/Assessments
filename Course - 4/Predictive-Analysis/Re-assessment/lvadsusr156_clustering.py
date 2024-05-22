# -*- coding: utf-8 -*-
"""LVADSUSR156-Clustering

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1CAlZXPG-PD8ynsISsE3UVLFGy44M5Ije

**CLUSTERING MODEL - K-MEANS CLUSTERING - CREDIT CARD CUSTOMERS**

**DATA LOADING**
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("/content/Credit Card Customer Data.csv")

df.head()

df.shape

df.info()

df.columns

df.nunique()

df.describe(include="all")

"""**BASIC ANALYSIS - EDA**"""

# Univariate Analysis between the numerical features by plotting Histogram

for num_col in df.select_dtypes(include=['float','int']):
  sns.histplot(df[num_col], kde=True)
  plt.show()
  plt.xlabel(num_col)
  plt.ylabel("Amount")
  plt.title(f"The Histogram of {num_col}")

## Bi-variate Analysis between the numerical columns using scatter plots

numerical_columns = df.select_dtypes(include=['float64', 'int64']).columns
for i in range(len(numerical_columns)):
    for j in range(i + 1, len(numerical_columns)):
        plt.figure(figsize=(10, 6))
        sns.scatterplot(data=df, x=numerical_columns[i], y=numerical_columns[j])
        plt.title(f'Scatter Plot between {numerical_columns[i]} and {numerical_columns[j]}')
        plt.show()

## Bi-variate Analysis between numerical features using correlation matrix and heat map

correlation_matrix = df.corr(numeric_only=True)

correlation_matrix

plt.figure(figsize=(8, 8))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm')
plt.show()

"""**HANDLING NULL VALUES AND DUPLICATES**"""

df.isnull().sum()

df.shape

df.columns

## For the total_visits_online feature we fill the null and missing values help of Simple Imputation with Median
## because the data is right skewed distribution

df['Total_visits_online'].fillna(df['Total_visits_online'].mean(), inplace=True)

df.isnull().sum()

df.duplicated().sum()

## No duplicates or repeated rows presents in the given dataset

"""**MANAGING OUTLIERS**"""

## Finding the outliers using Box-plot for the numerical features

for col in df.select_dtypes(include=['float','int']):
  sns.boxplot(df[col])
  plt.show()

# Function to calculate the IQR bounds
def calculate_bounds(column):
    Q1 = column.quantile(0.25)
    Q3 = column.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return lower_bound, upper_bound

# Function to treat outliers by capping
def treat_outliers(column):
    lower_bound, upper_bound = calculate_bounds(column)
    return column.apply(lambda x: lower_bound if x < lower_bound else upper_bound if x > upper_bound else x)

df.columns

## Outliers lies in the given numerical features like Avg_Credit_Limit and Total_visits_online
## So these are treated to maintain the effifiency of the model
## These are treated by IQR function to reduce the outliers

df['Avg_Credit_Limit'] = treat_outliers(df['Avg_Credit_Limit'])
df['Total_visits_online'] = treat_outliers(df['Total_visits_online'])

"""**FEATURE ENGINEERING AND ENCODING**"""

df.columns

df.drop(['Sl_No','Customer Key'], axis=1, inplace=True)

## Dropping the above features because of their ID or Serial number which are used to record the transactions

df.info()

df.head()

"""**2.2 ENCODING**"""

## No Encoding is done because there is no categorical feature

df.head()

cor = df.corr(numeric_only=True)

plt.figure(figsize=(8, 8))
sns.heatmap(cor, annot=True, cmap='coolwarm')
plt.show()

"""**3. FINDING THE OPTIMAL K VALUE USING ELBOW METHOD AND SILHOUTTE SCORE**"""

from sklearn.cluster import KMeans

sse = [] # The sum of Squared Errors =SSE
k_rng = range(1,10)
for k in k_rng:
   km = KMeans(n_clusters=k)
   km.fit(df)
   sse.append(km.inertia_)

plt.xlabel('K')
plt.ylabel('Sum of squared error')
plt.plot(k_rng,sse)

from sklearn.metrics import silhouette_score

silhouette_score(df, km.fit_predict(df))

df.columns

km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df[['Avg_Credit_Limit','Total_Credit_Cards']])
print(y_predicted)

df['cluster']=y_predicted
df.head(5)

original_df = df.copy()

original_df.head()

print(km.cluster_centers_)

from sklearn.metrics import silhouette_score

df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]

plt.scatter(df1.Avg_Credit_Limit,df1['Total_Credit_Cards'],color='green')
plt.scatter(df2.Avg_Credit_Limit,df2['Total_Credit_Cards'],color='red')
plt.scatter(df3.Avg_Credit_Limit,df3['Total_Credit_Cards'],color='black')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')

plt.xlabel('Avg_Credit_Limit')
plt.ylabel('Total_Credit_Cards')
plt.legend()

from sklearn.preprocessing import LabelEncoder, MinMaxScaler

scaler = MinMaxScaler()
for column in df.select_dtypes(include=['float64','int64']):
  df[column] = scaler.fit_transform(df[[column]])

print(df.head())

km = KMeans(n_clusters=3)
y_predicted = km.fit_predict(df[['Avg_Credit_Limit','Total_Credit_Cards']])
y_predicted

df['cluster']=y_predicted
df.head(5)

print(km.cluster_centers_)

from sklearn.metrics import silhouette_score

df1 = df[df.cluster==0]
df2 = df[df.cluster==1]
df3 = df[df.cluster==2]

original_df1 = original_df[original_df.cluster==0]
original_df2 = original_df[original_df.cluster==1]
original_df3 = original_df[original_df.cluster==2]

plt.scatter(df1.Avg_Credit_Limit,df1['Total_Credit_Cards'],color='green')
plt.scatter(df2.Avg_Credit_Limit,df2['Total_Credit_Cards'],color='red')
plt.scatter(df3.Avg_Credit_Limit,df3['Total_Credit_Cards'],color='black')
plt.scatter(km.cluster_centers_[:,0],km.cluster_centers_[:,1],color='purple',marker='*',label='centroid')

plt.xlabel('Avg_Credit_Limit')
plt.ylabel('Total_Credit_Cards')
plt.legend()

print("The Silhouette Score: ")
print(silhouette_score(df, y_predicted))

print(original_df1['Avg_Credit_Limit'].mean())
print(original_df1['Total_Credit_Cards'].mean())

print(original_df2['Avg_Credit_Limit'].mean())
print(original_df2['Total_Credit_Cards'].mean())

print(original_df3['Avg_Credit_Limit'].mean())
print(original_df3['Total_Credit_Cards'].mean())

silhouette_score(df[['Avg_Credit_Limit','Total_Credit_Cards']], km.fit_predict(df[['Avg_Credit_Limit','Total_Credit_Cards']]))

"""**CLUSTER PROFILING**"""

# From the above Clustering, the optimal cluster number for the given features
# Average Credit Card Limit and Total Credit Cards Using.

# Cluster 1 has average credit limit with about 102607 as an Average with average total of 8 cards,
# which we can Profile them as High Credit Card Users.

# Cluster 2 has average credit limit with about 13463 as an Average with average total of 3 cards,
# which we can Profile them as Low Credit Card Users.

# Cluster 1 has average credit limit with about 53612 as an Average with average total of 5 cards,
# which we can Profile them as Medium Credit Card Users.

"""**BUSINESS RECOMMENDATIONS**"""

# From the above Inference, we recommend that

# For High Users, We can include various schemes and we can mobilize our credit card usage across various platform which
#  improves the longevity and customer satisfaction.

# For Medium Users, we can offer various offers, discounts for the products or services they purchases
# which helps to improve the usage from medium to high.

# For Low Users, we can gain their trust by improving their satisfactions and allows them to
# purchase more with their credit by not deducting any charges, and providing offers which '
# intrudes them to use the credit cards.