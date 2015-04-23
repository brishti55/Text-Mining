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
    output_dir1 = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/review_words_new/"
#     output_dir2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/funding_agency/"


    print "Begin..."

    for filename in glob.glob(data_dir1 + '*.txt'):       
        parsed_file = open(filename, 'r')
        out_name = filename.replace("/","_")
        output_file = open(output_dir1 + out_name + '_words.txt', 'w')

#         output_file_name = ['B000GLRREU','B000KUHFGM','B000QSNYGI']
#         for i in range(len(output_file_name)):
#             output_file = open(output_dir1 + output_file_name[i] + '.txt' , 'w')
#         parsed_file.close()

        print output_file

#         Generate list of English stopwords
        english_stops = set(stopwords.words('english'))
 
        # Punctuation set
        punct = ''.join(set(string.punctuation))
 
        # Initialize stemmer2
        porter = PorterStemmer()
         
#         vocabulary = []
 
        
        for line in parsed_file:
                #print line
                if line.isspace():
                    continue
                else:
                    if len(line.split('|')) <= 4:
                        (prodID, reviewID, sentence_id, sentence) = line.split('|')
                     
      
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
#                     words = [porter.stem(word) for word in words]
                      
                    for word in words:
#                         vocabulary.append(word)
#                         if prodIDs[i] == prodID_id:
                            output_file.write(str(prodID)+','+str(reviewID)+','+ str(sentence_id) +','+ str(words.index(word)+1) +','+ word+'\n')
    
        parsed_file.close()
        output_file.close()      

                      
    print "End..."
    

if __name__ == "__main__":
    main()