#!/Users/jogg/anaconda/bin/python 
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.datasets import make_moons, make_circles, make_classification
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.lda import LDA
from sklearn.qda import QDA
from sklearn.datasets import load_svmlight_file
from sklearn.metrics import accuracy_score
from scipy.sparse import csr_matrix


names = ["Nearest Neighbors", 
         "Linear SVM", 
         #"Polynomial SVM", 
         "RBF SVM"] 
         #"Sigmoid"

names2=  [
         "Naive Bayes", 
         "LDA", 
         "QDA",
         "AdaBoost", 
         "Decision Tree",
         "Random Forest"] 
         
classifiers = [
    KNeighborsClassifier(3),
    SVC(kernel="linear", C=0.025),
    #SVC(kernel="polynomial"),
    SVC(gamma=2, C=1)]
    #SVC(kernel="sigmoid")

classifiers2 = [
    GaussianNB(),
    LDA(),
    QDA(),	
    AdaBoostClassifier(),
    DecisionTreeClassifier(max_depth=5),
    RandomForestClassifier(max_depth=5, n_estimators=10, max_features=1)]

path = "/Users/jogg/Desktop/Andy/ML-NLP/Data/cvresult1/betterfeature/"
path2 = "/Users/jogg/Desktop/Andy/ML-NLP/Data/cvresult"

out = open(path + "clf_res.txt", "w")
for j in range(3):
  path = path2 + str(j) + "/betterfeature/"
  print "\n"
  out.write("\n")
  for i in range(3):
   if i == 0:
     tf = path + "bow/train_bow_svm.txt" 
     tsf = path + "bow/test_bow_svm.txt" 
   elif i == 1:
     tf = path + "presence/train_pre_svm.txt" 
     tsf = path + "presence/test_pre_svm.txt" 
   else:
     tf = path + "tf-idf/train_tfidf_svm.txt" 
     tsf = path + "tf-idf/test_tfidf_svm.txt" 

   X_train, y_train = load_svmlight_file(tf)
   X_test, y_test = load_svmlight_file(tsf)

   for name, clf in zip(names, classifiers):
     clf.fit(X_train,y_train) 
     score = clf.score(X_test,y_test)
     s = name + ": " + str(score)
     print s
     out.write(s+"\n")


out.close()

#for name, clf in zip(names2, classifiers2):
#   clf.fit(X_train,y_train) 
#   score = clf.score(X_test,y_test)
#   print name + ": " + str(score)
#for name, clf in zip(names2, classifiers2):
#   X =csr_matrix(X_train).todense()
#   y =csr_matrix(y_train).todense()
#   clf.fit(X,y) 
#   X_t =csr_matrix(X).todense()
#   y_t =csr_matrix(y).todense()
#   score = clf.score(X_t,y_t)
#   print name + ": " + str(score)
