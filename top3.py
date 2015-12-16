#!/usr/bin/env python
import os
import glob
import sys, string
import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def main():
#     print "Begin..."

    data_dir1 = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/top3_sent/"
#     data_dir2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/parsed_abstracts/"
    output_dir1 = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/review_words_top3/"
#     output_dir2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/funding_agency/"


    print "Begin..."
#     vocabDict={}
#     DocCount = 0
    for filename in glob.glob(data_dir1 + '*.txt'): 
        print filename
#         DocCount += 1
        parsed_file = open(filename, 'r')
        
        prodIDs = []
        top = ['B000GLRREU','B000KUHFGM','B000QSNYGI']
        
        for line in parsed_file:
            line = line.rstrip()
            line = line.split('|')          
            id = line[0]
            if id in top and id not in prodIDs:
                prodIDs.append(id)
                #print "."
            else:
                continue
        parsed_file.close()

        output_file_name = [''] * len(prodIDs) 
        for i in range(len(prodIDs)):
            output_file_name[i] = prodIDs[i]
            #output_file = open(output_dir1 + output_file_name[i] + '.txt' , 'w')

        # Generate list of English stopwords
        english_stops = set(stopwords.words('english'))

        # Punctuation set
        punct = ''.join(set(string.punctuation))

        # Initialize stemmer2
        porter = PorterStemmer()
        
#         vocabulary = []

        for i in range(len(prodIDs)):
            parsed_file = open(filename, 'r')
             
            output_file = open(output_dir1 + output_file_name[i] + '.txt' , 'w')
            print output_file_name[i]
            for line in parsed_file:
                #print line
                if line.isspace():
                    continue
                else:
                    if len(line.split('|')) <= 3:
                        (prodID_id, sentence_id, sentence) = line.split('|')
                    
     
                if sentence.isspace():
                    continue
                else:
                    words = word_tokenize(sentence.rstrip())
     
                    # Remove words that are just punctuation
                    words = filter(lambda word: word not in punct, words)
     
                    # Normalize the words
                    words = [word.lower() for word in words]
     
                    # Remove stopwords
                    words = [word for word in words if word not in english_stops]
     
                    # Apply the Porter stemmer
                    words = [porter.stem(word) for word in words]
                     
                    for word in words:
#                         vocabulary.append(word)
                        if prodIDs[i] == prodID_id:
                            output_file.write(str(prodID_id)+','+str(sentence_id)+','+str(words.index(word))+','+word+'\n')
            parsed_file.close()
            output_file.close()      
                      
    print "End..."
    

if __name__ == "__main__":
    main()
