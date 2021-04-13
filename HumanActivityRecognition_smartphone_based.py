# -*- coding: utf-8 -*-
"""HumanActivityRecognition_smartphone based.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18J9eE-yLLNPGd0DV_YjwPrCLdFG9q32g
"""

import pandas as pd
import numpy as np

# Commented out IPython magic to ensure Python compatibility.
#Visualization Libraries:
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline
import plotly.graph_objects as go
import plotly.express as px
import plotly.io as pio
pio.templates.default = "plotly_dark"
sns.set(style="darkgrid")

#Scikit-model requisites:
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import confusion_matrix
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score

import warnings
warnings.filterwarnings("ignore")

# Get Features from the Dataset:
with open("/content/HAPT Dataset/features.txt", "r") as _: 
  features = [x.strip().replace('()', '').replace(',', '').split(' ')[-1] for x in _.readlines()]
print("Number of Features:", len(features))
print("Features:\n",features[:5])

"""**Training Data**"""

#Participant IDs:
with open('/content/HAPT Dataset/Train/subject_id_train.txt', 'r') as _: 
  train_id = pd.Series([int(x.strip()) for x in _.readlines()])

#Activity Labels:
with open('/content/HAPT Dataset/Train/y_train.txt', 'r') as _: 
  y_train = pd.Series([int(x.strip()) for x in _.readlines()])
y_train.value_counts().sort_index()

#Creating the Train Dataframe: 
X_train = pd.read_csv('/content/HAPT Dataset/Train/X_train.txt', sep=" ", header=None)
X_train.columns = features
X_train

#Finding Shape of the Tarin Dataframe:
X_train.shape

#Finding the Datatype of the Train Dataframe:
X_train.dtypes

"""**Test Data**"""

#Participant IDs:
with open('/content/HAPT Dataset/Test/subject_id_test.txt', 'r') as _: 
  test_id = pd.Series([int(x.strip()) for x in _.readlines()])

#Activity Labels:
with open('/content/HAPT Dataset/Test/y_test.txt', 'r') as _: 
  y_test = pd.Series([int(x.strip()) for x in _.readlines()])

y_test.value_counts().sort_index()

#Creating the Test Dataframe:
X_test = pd.read_csv('/content/HAPT Dataset/Test/X_test.txt', sep=" ", header=None)
X_test.columns = features
X_test

#Finding Shape of the Test Dataframe:
X_test.shape

#Finding Datatypes of the Test Dataframe:
X_test.dtypes

"""We implement the following 3 ML Algorithms on the Dataset:

1. **LOGISTIC REGRESSION**
2. **K-NEAREST NEIGHBOURS**
3. **SVM**

And compare the output accuracies of these algorithms.

***Algorithm 1:***

**LOGISTIC REGRESSION**
"""

LR = LogisticRegression()

#K-fold CV 
"K-value is substiuited by 10, 20 and 30 after a complete run of the code"
accuraccies = cross_val_score(estimator = LR, X= X_train, y=y_train, cv=30)   
print("Average Accuracies: ",100*np.mean(accuraccies))
print("Standard Deviation Accuracies: ",100*np.std(accuraccies))

LR.fit(X_train,y_train) #Learning Stage
#Prediction Stage:
print("LR Score: {}".format(100*LR.score(X_test,y_test))) 
LRscore = LR.score(X_test,y_test)

#Confusion Matrix:
y_pred_lr= LR.predict(X_test)
CM = confusion_matrix(y_test,y_pred_lr)

f, ax = plt.subplots(figsize=(6,6))
sns.heatmap(CM,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred_lr")
plt.ylabel("y_test")
plt.show()

"""***Algorithm 2:***

**K-NEAREST NEIGHBOURS**
"""

KNN = KNeighborsClassifier(n_neighbors = 30) #"K-value is substiuited by 10, 20 and 30 after a complete run of the code"

#K-fold CV
"K-value is substiuited by 10, 20 and 30 after a complete run of the code"
accuraccies = cross_val_score(estimator = KNN, X= X_train, y=y_train, cv=30)
print("Average Accuracies: ",100*np.mean(accuraccies))
print("Standard Deviation Accuracies: ",100*np.std(accuraccies))

#Learning Stage:
KNN.fit(X_train,y_train)

#Prediction Stage:
prediction = KNN.predict(X_test)
print("{}-NN Score: {}".format(30,100*KNN.score(X_test,y_test)))
KNNscore = KNN.score(X_test,y_test)

#Confusion Matrix:
y_pred_knn= KNN.predict(X_test)
CM = confusion_matrix(y_test,y_pred_knn)

f, ax = plt.subplots(figsize=(6,6))
sns.heatmap(CM,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred_knn")
plt.ylabel("y_test")
plt.show()

"""***Algorithm 3:***

**SUPPORT VECTOR MACHINES**
"""

SVM = SVC(random_state=42)

#K-fold CV
"K-value is substiuited by 10, 20 and 30 after a complete run of the code"
accuraccies = cross_val_score(estimator = SVM, X= X_train, y=y_train, cv=30)
print("Average Accuracies: ",100*np.mean(accuraccies))
print("Standart Deviation Accuracies: ",100*np.std(accuraccies))

#Learning Stage:
SVM.fit(X_train,y_train)  

#Prediction Stage:
print("SVM Score:", 100*SVM.score(X_test,y_test))
SVMscore = SVM.score(X_test,y_test)

#Confusion Matrix:
y_pred_svm= SVM.predict(X_test)
CM = confusion_matrix(y_test,y_pred_svm)

f, ax = plt.subplots(figsize=(6,6))
sns.heatmap(CM,annot = True, linewidths=0.5,linecolor="red",fmt=".0f",ax=ax)
plt.xlabel("y_pred_svm")
plt.ylabel("y_test")
plt.show()

"""***Model Comparisions:***

Models are compared on the basis of their **f1-score**.
"""

#Model Comaparision:
data = [['Logistic Regression',f1_score(y_test, y_pred_lr, average='weighted')],
        ['K-Nearest Neighbors Algorithm (K-NN)',f1_score(y_test, y_pred_knn, average='weighted')],
        ['Support Vector Machines (SVM)',f1_score(y_test, y_pred_svm, average='weighted')]]

F1_Score = pd.DataFrame(data, columns = ['Ml Algorithms', 'f1_score'])
F1_Score.sort_values(by = 'f1_score', ascending=0)

#Comparative Plot of f1-scores:
F1_Score.set_index('Ml Algorithms')['f1_score'].plot(figsize=(10, 5), linewidth=2.5)

#Author: Shirshakk Purkayastha
#18247