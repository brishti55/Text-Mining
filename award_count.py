#!/usr/bin/env python
import os
import sys, string
import nltk
import nltk.data
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

#read file 
filename = 'abstract_list.txt'
f = open(filename, 'rU')
output_file = open('parsed_abstracts.txt', 'w')
#content = f.read()
#print filename, len(content)

abstract_record = []
abstract_text = ''

for line in f:
    #line = line.rstrip
    line = line.split(":")
    
    if line[0] == 'NSF Org     ' or line[0] == 'Award Number':
        abstract_record.append(line[1].strip())
        if line[0] == 'Abstract    ':
            for line in f:
                abstract_text = abstract_text + line.rstrip()
                abstract_text = ' '.join(abstract_text.split())
                abstract_record.append(abstract_text)
                break
        
                
                output_file.write('^'.join(abstract_record)+'\n')
    
                output_file.close()