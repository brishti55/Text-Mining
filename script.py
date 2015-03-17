#!/Users/jogg/anaconda/bin/python

import nltk, re, pprint
import glob
import os
import numpy

from nltk import word_tokenize
from nltk import cluster
from nltk.cluster import util
from nltk.cluster import api
from nltk.cluster import euclidean_distance
from nltk.cluster import cosine_distance


def BOW(document,unique_terms):
       word_counts = []
       for word in unique_terms:
          word_counts.append(document.count(word))
       return word_counts

def presence(document,unique_terms):
       word_counts = []
       for word in unique_terms:
          if document.count(word) == 0:
             word_counts.append(0)
          else:
             word_counts.append(1)
       return word_counts
    
def TFIDF(document,collectn):
       word_tfidf = []
       for word in unique_terms:
          word_tfidf.append(collectn.tf_idf(word,document))
       return word_tfidf


DIRLIST=["/Users/zehadyzbdullahkhan/Documents/PurdueUniversity/Courses/ML-NLP/Project/Machine-Learning-Natural-Language-Processing/mix20_rand700_tokens_cleaned/tokens/pos/","/Users/zehadyzbdullahkhan/Documents/PurdueUniversity/Courses/ML-NLP/Project/Machine-Learning-Natural-Language-Processing/mix20_rand700_tokens_cleaned/tokens/neg/"]
cv_cycle=3

for i in range(cv_cycle):
   #For positive movie reviews
    DIR=DIRLIST[0]
    os.chdir(DIR)
    filenum=0
    files=[]
    for file in glob.glob("*.txt"):
        filenum+=1
        files.append(file)
    d= int(filenum / cv_cycle)
    #print d

    train_files=[]
    test_files=[]
    #print i
    if i == 0:
       for j in range(2*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)

       for j in range(2*d,3*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  test_files.append(fn)
    elif i==1:
       for j in range(d,3*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)
       #print "\n"
       for j in range(d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  test_files.append(fn)
    elif i==2:
       for j in range(0,d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)
       for j in range(2*d,3*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)
       #print "\n"
       for j in range(d,2*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  test_files.append(fn)

    #print "\n\n"
    
    all_terms=[]
    texts=[]
    texts_train=[]
    texts_test=[]
    raw=""
    #print train_files
    #print test_files
    trainandtestfiles=train_files + test_files
    #print trainandtestfiles

    for file in trainandtestfiles:
        #print file
        f=open(file,"r")
        raw=f.read().decode("latin-1")+"\n"
        f.close()
        tokens=word_tokenize(raw)
        all_terms=all_terms+tokens
        text=nltk.Text(tokens)
        texts.append(text)
        if file in train_files:
           texts_train.append(text)
        elif file in test_files:
           texts_test.append(text)

  # For negative movie reviews
    DIR=DIRLIST[1]
    os.chdir(DIR)
    filenum=0
    files=[]
    for file in glob.glob("*.txt"):
        filenum+=1
        files.append(file)
    d= int(filenum / cv_cycle)
    #print d

    train_files=[]
    test_files=[]
    #print i
    if i == 0:
       for j in range(2*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)

       for j in range(2*d,3*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  test_files.append(fn)
    elif i==1:
       for j in range(d,3*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)
       #print "\n"
       for j in range(d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  test_files.append(fn)
    elif i==2:
       for j in range(0,d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)
       for j in range(2*d,3*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  train_files.append(fn)
       #print "\n"
       for j in range(d,2*d):
          m=re.match(r"cv[0-9]+_tok-([0-9]+).txt",files[j])
          num=m.group(1)
          #print j
          fn = "cv"+'{0:03d}'.format(int(j))+"_tok-"+str(num)+".txt"
          #print fn
	  test_files.append(fn)

    #print "\n\n"


    
    trainandtestfiles=train_files + test_files
    #print trainandtestfiles

    for file in trainandtestfiles:
        #print file
        f=open(file,"r")
        raw=f.read().decode("latin-1")+"\n"
        f.close()
        tokens=word_tokenize(raw)
        all_terms=all_terms+tokens
        text=nltk.Text(tokens)
        texts.append(text)
        if file in train_files:
           texts_train.append(text)
        elif file in test_files:
           texts_test.append(text)
 
    #print texts
    #print texts_train
    #print texts_test
    #print "\n"
    
    unique_terms=sorted(list(set(all_terms)))
    #print unique_terms
    
    path="/Users/zehadyzbdullahkhan/Documents/PurdueUniversity/Courses/ML-NLP/Project/Machine-Learning-Natural-Language-Processing/cvresult" + str(i)+"/"
    if not os.path.exists(path):
       #print "hello"
       os.makedirs(path)

    outf=open(path+"words.txt","w")
    for word in unique_terms:
       #print word
       outf.write(word.encode("latin-1")+"\n")
    
    outf.close
    
    
    #print "Prepared ", len(texts), " documents..."
    #print "They can be accessed using texts[0] - texts[" + str(len(texts)-1) + "]"
    
    #Load the list of texts into a TextCollection object.
    collection = nltk.TextCollection(texts)
    collection_train = nltk.TextCollection(texts_train)
    collection_test = nltk.TextCollection(texts_test)
    #print "Created a collection of", len(collection), "terms."
    
    
#################BOW##################
    path=path+"bow/"
    if not os.path.exists(path):
       #print "hello"
       os.makedirs(path)

    trainf=open(path+"train_bow.txt","w")
    testf=open(path+"test_bow.txt","w")

    freq_vectors_bow=[]
    freq_vectors_bow_train=[]
    freq_vectors_bow_test=[]

    freq_vectors = [numpy.array(BOW(f,unique_terms)).astype(numpy.int64) for f in texts]
    #print "Vectors for train files created."
    
    #print freq_vectors_bow

    #print texts_train
    freq_vectors_bow_train = [numpy.array(BOW(f,unique_terms)).astype(numpy.int64) for f in texts_train]
    #print "Vectors for train files created."
    
    #print freq_vectors_bow_train
    numpy.savetxt(trainf,freq_vectors_bow_train,fmt="%d")
 
    #svm-light train file for bow
    trainf_svm=open(path+"train_bow_svm.txt","w")

    freq_vectors_bow_train_a= numpy.array(freq_vectors_bow_train)
    (row,col)=freq_vectors_bow_train_a.shape 
    for i in range(row):
        if i in range(2*d):
 	    trainf_svm.write("+1 ")
        else:
 	    trainf_svm.write("-1 ")
        for j in range(col):
            val=freq_vectors_bow_train_a[i,j] 
            if val != 0: 
 	        trainf_svm.write(str(j) + ":" + str(val) + " ")
        trainf_svm.write("\n")
        

    #print texts_test
    freq_vectors_bow_test = [numpy.array(BOW(f,unique_terms)).astype(numpy.int64) for f in texts_test]
    #print "Vectors for test files created."
    
    #print freq_vectors_bow_test
    numpy.savetxt(testf,freq_vectors_bow_test,fmt="%d")

    #svm-light test file for bow
    testf_svm=open(path+"test_bow_svm.txt","w")

    freq_vectors_bow_test_a= numpy.array(freq_vectors_bow_test)
    (row,col)=freq_vectors_bow_test_a.shape 
    for i in range(row):
        if i in range(d):
 	    testf_svm.write("+1 ")
        else:
 	    testf_svm.write("-1 ")
        for j in range(col):
            val=freq_vectors_bow_test_a[i,j] 
            if val != 0: 
 	        testf_svm.write(str(j) + ":" + str(val) + " ")
        testf_svm.write("\n")

    trainf.close()
    testf.close()
    trainf_svm.close()
    testf_svm.close()
    
    
################PRESENCE##################

    path=path+"../presence/"
    if not os.path.exists(path):
       #print "hello"
       os.makedirs(path)

    trainf=open(path+"train_presence.txt","w")
    testf=open(path+"test_presence.txt","w")

    freq_vectors_pre=[]
    freq_vectors_pre_train=[]
    freq_vectors_pre_test=[]

    freq_vectors_pre = [numpy.array(presence(f,unique_terms)).astype(numpy.int64) for f in texts]
    #print "Vectors for train files created."
    
    #print freq_vectors_pre

    #print texts_train
    freq_vectors_pre_train = [numpy.array(presence(f,unique_terms)).astype(numpy.int64) for f in texts_train]
    #print "Vectors for train files created."
    
    #print freq_vectors_pre_train
    numpy.savetxt(trainf,freq_vectors_pre_train,fmt="%d")

    #svm-light train file for presence 
    trainf_svm=open(path+"train_pre_svm.txt","w")

    freq_vectors_pre_train_a= numpy.array(freq_vectors_pre_train)
    (row,col)=freq_vectors_pre_train_a.shape 
    for i in range(row):
        if i in range(2*d):
 	    trainf_svm.write("+1 ")
        else:
 	    trainf_svm.write("-1 ")
        for j in range(col):
            val=freq_vectors_pre_train_a[i,j] 
            if val != 0: 
 	        trainf_svm.write(str(j) + ":" + str(val) + " ")
        trainf_svm.write("\n")

    #print texts_test
    freq_vectors_pre_test = [numpy.array(presence(f,unique_terms)).astype(numpy.int64) for f in texts_test]
    #print "Vectors for test files created."
    
    #print freq_vectors_pre_test
    numpy.savetxt(testf,freq_vectors_pre_test,fmt="%d")

    #svm-light test file for bow
    testf_svm=open(path+"test_pre_svm.txt","w")

    freq_vectors_pre_test_a= numpy.array(freq_vectors_pre_test)
    (row,col)=freq_vectors_pre_test_a.shape 
    for i in range(row):
        if i in range(d):
 	    testf_svm.write("+1 ")
        else:
 	    testf_svm.write("-1 ")
        for j in range(col):
            val=freq_vectors_pre_test_a[i,j] 
            if val != 0: 
 	        testf_svm.write(str(j) + ":" + str(val) + " ")
        testf_svm.write("\n")

    trainf.close()
    testf.close()
    trainf_svm.close()
    testf_svm.close()
    

################TF-IDF##################

    path=path+"../tf-idf/"
    if not os.path.exists(path):
       #print "hello"
       os.makedirs(path)

    trainf=open(path+"train_tf-idf.txt","w")
    testf=open(path+"test_tf-idf.txt","w")

    freq_vectors_tfidf=[]
    freq_vectors_tfidf_train=[]
    freq_vectors_tfidf_test=[]

    freq_vectors_tfidf = [numpy.array(TFIDF(f,collection)) for f in texts]
    #print "Vectors for train files created."
    
    #print freq_vectors_tfidf

    #print texts_train
    freq_vectors_tfidf_train = [numpy.array(TFIDF(f,collection_train)) for f in texts_train]
    #print "Vectors for train files created."
    
    #print freq_vectors_tfidf_train
    numpy.savetxt(trainf,freq_vectors_tfidf_train,fmt="%.6f")

    #svm-light train file for tf-idf 
    trainf_svm=open(path+"train_tfidf_svm.txt","w")

    freq_vectors_tfidf_train_a= numpy.array(freq_vectors_tfidf_train)
    (row,col)=freq_vectors_tfidf_train_a.shape 
    for i in range(row):
        if i in range(2*d):
 	    trainf_svm.write("+1 ")
        else:
 	    trainf_svm.write("-1 ")
        for j in range(col):
            val=freq_vectors_tfidf_train_a[i,j] 
            if val != 0: 
 	        trainf_svm.write(str(j) + ":" + str(val) + " ")
        trainf_svm.write("\n")

    #print texts_test
    freq_vectors_tfidf_test = [numpy.array(TFIDF(f,collection_train)) for f in texts_test]
    #print "Vectors for test files created."
    
    #print freq_vectors_tfidf_test
    numpy.savetxt(testf,freq_vectors_tfidf_test,fmt="%.6f")

    #svm-light test file for tfidf 
    testf_svm=open(path+"test_tfidf_svm.txt","w")

    freq_vectors_tfidf_test_a= numpy.array(freq_vectors_tfidf_test)
    (row,col)=freq_vectors_tfidf_test_a.shape 
    for i in range(row):
        if i in range(d):
 	    testf_svm.write("+1 ")
        else:
 	    testf_svm.write("-1 ")
        for j in range(col):
            val=freq_vectors_tfidf_test_a[i,j] 
            if val != 0: 
 	        testf_svm.write(str(j) + ":" + str(val) + " ")
        testf_svm.write("\n")

    trainf.close()
    testf.close()
    trainf_svm.close()
    testf_svm.close()


    #classification
    

