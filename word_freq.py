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

    data_dir1 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/abstract_sentences/"
    data_dir2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/parsed_abstracts/"
    output_dir1 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/abstract_words/"
    output_dir2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/funding_agency/"


    print "Begin..."
    vocabDict={}
    DocCount = 0
    for filename in glob.glob(data_dir1 + '*.txt'):
        print filename
        DocCount += 1
        parsed_file = open(filename, 'r')
        ofn = filename.split("/")
        output_file_name = ofn[len(ofn) - 1]
        output_file = open(output_dir1 + output_file_name , 'w')

        # Generate list of English stopwords
        english_stops = set(stopwords.words('english'))

        # Punctuation set
        punct = ''.join(set(string.punctuation))

        # Initialize stemmer
        porter = PorterStemmer()
        
        vocabulary = []
        for line in parsed_file:
            if line.isspace():
                continue
            else:
                if len(line.split('|')) <= 3:
                    (abstract_id, sentence_id, sentence) = line.split('|')

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
                    vocabulary.append(word)
                    output_file.write(str(abstract_id)+','+str(sentence_id)+','+str(words.index(word))+','+word+'\n')
        vocabulary = set(vocabulary)
        for word in vocabulary:
            if (word in vocabDict):
                vocabDict[word] += 1
            else:
                vocabDict[word] = 1    
                   
    #org name and award number table
    for file_name in glob.glob(data_dir2 + '*.txt'):
                parsed_abstract = open(file_name, 'r')
                output_file1 = open(output_dir2 + 'agency.txt', 'a')
                  
                for line in parsed_abstract:
                    if line.isspace():
                        continue
                    else:
                        if len(line.split('<>')) <= 3:
                            (nsf_agency, award_number, abstract) = line.split('<>')
                              
                output_file1.write(str(award_number)+','+str(nsf_agency) + '\n')
                output_file1.close()
                parsed_abstract.close()              
                      
    
    
    output_file.close()
    parsed_file.close()
    print "End..."
    
#     print vocabulary
#     vocabulary = sorted(vocabulary)
#     #vocabulary = list(set(list(vocabulary)))
#     
#     from nltk import FreqDist
#     vocabDist = FreqDist(vocabulary)
#     for word in set(vocabulary):
#         print word, "=", vocabDist[word]

    print "Total Document = " , DocCount    
    highFreqVocab = {}
    for word in vocabDict:
        print word, "=", vocabDict[word]
        presence = vocabDict[word]
        if (presence > 5 and presence < 95 and 
            not word.isdigit() and word !="'s" 
            and word != "''" and word != "``"):
            highFreqVocab[word] = presence
    
    output_dir3 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/"
    
    sortedHighFreqWords=[]
    for word in highFreqVocab:
        sortedHighFreqWords.append(word)
    
    sortedHighFreqWords = sorted(sortedHighFreqWords)
    
    highFreqVocabFile = open(output_dir3 + "highFreqVocab.txt","w")
    for word in sortedHighFreqWords:
        tmpStr = word+ " " + str(highFreqVocab[word]) + "\n"
        print tmpStr
        highFreqVocabFile.write(tmpStr)
    
        
    

if __name__ == "__main__":
    main()
