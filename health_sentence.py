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
          print "Begin..."

          data = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/health_output.txt"
          output_token = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/top3_sent/B000KUHFGM.txt"
#           output_dir2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/abstract_sentences/"
   
          line_distribution = [0 for i in range(110)]
          #parsed_file = open('parsed_abstracts.txt', 'r')
          parsed_file = open(data, 'r')
          print "Begin Tokenization... on " + data  
          output_file = open(output_token, 'w')
          
     
          tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
     
          for line in parsed_file:
              if line.isspace():
                  continue
              else:
#                   print line.split('<>')[:-1]
                  if len(line.split('<>')[:-1]) <= 6:
                      (prodID, prodTitle, price, reviewID, rating, review) = line.split('<>')[:-1]
                      
                      if  review.isspace():
                          continue
                      else:
                  # Remove non-ASCII characters
                          review = ''.join([i if ord(i) < 128 else '' for i in review])
     
                  # Tokenize sentences
                          sentences = tokenizer.tokenize(review.rstrip())
#                           if len(sentences)>=1 and '***' in sentences[-1]:   # Error check
#                               sentences.pop()
     
#                           sent_cnt = 0
                          if prodID=='B000KUHFGM':
                              for sentence in sentences:
#                                   sent_cnt += 1
                                  print "." 
                                  output_file.write(str(prodID)+'|'+str(reviewID)+'|'+str(sentences.index(sentence)+1)+'|'+sentence+'\n')
#                           line_distribution[sent_cnt] += 1
     
          output_file.close()
          parsed_file.close()
          print "End Tokenization of the file."

#           line_dist_file = open("/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/line_distribution.txt", "w")
#           for i in range(0,len(line_distribution)):
#              line_dist_file.write(str(i) + " " + str(line_distribution[i]) + "\n")
    #abstract_file_list.close()
     
    #abstract_file_list.close()
          print "End Abstract parsing and tokenization."
      
            
#     print "Begin..."
#
#     parsed_file = open('abstract_sentences.txt', 'r')
#     output_file = open('abstract_words.csv', 'w')
#
#     # Generate list of English stopwords
#     english_stops = set(stopwords.words('english'))
#
#     # Punctuation set
#     punct = ''.join(set(string.punctuation))
#
#     # Initialize stemmer
#     porter = PorterStemmer()
#
#     for line in parsed_file:
#         if line.isspace():
#             continue
#         else:
#             if len(line.split('^')) <= 3:
#                 (abstract_id, sentence_id, sentence) = line.split('^')
#
#         if sentence.isspace():
#             continue
#         else:
#             words = word_tokenize(sentence.rstrip())
#
#             # Remove words that are just punctuation
#             words = filter(lambda word: word not in punct, words)
#
#             # Normalize the words
#             words = [word.lower() for word in words]
#
#             # Remove stopwords
#             words = [word for word in words if word not in english_stops]
#
#             # Apply the Porter stemmer
#             words = [porter.stem(word) for word in words]
#
#             for word in words:
#                 output_file.write(str(abstract_id)+'|'+str(sentence_id)+'|'+str(words.index(word))+'|'+word+'\n')
#
#     output_file.close()
#     parsed_file.close()
#     print "End..."
#
if __name__ == "__main__":
    main()
