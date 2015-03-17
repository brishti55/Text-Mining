#!usr/bin/env/python
import os
import sys, string 
import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

def main():
    
    print "Load data"
    
    data = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/Health.txt"
    data_output1 = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/health_output.txt"
    
    input_file = open(data, 'r')
    output_file = open(data_output1, 'w')
    
    review = []
    review_text = ''
    
    for line in input_file:
      line = line.rstrip()
      line = line.split(':')
      if line[0]=='product/productId' or line[0]=='product/title' or line[0]=='product/price' or line[0]=='review/score' or line[0]=='review/text':
         str= line[1].strip()
         review.append(str)
      if line[0]== '':
         review.append('\n')
         output_file.write('<>'.join(review))
         review = []
         
    print "finished"
      
    input_file.close()
    output_file.close()
    
if __name__ == "__main__":
    main()