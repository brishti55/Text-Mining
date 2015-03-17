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

    data_dir = "/Users/zehadyzbdullahkhan/Downloads/Brishti/Part1/"
    output_dir1 = "/Users/zehadyzbdullahkhan/Downloads/Brishti/Parsed_Abstracts/"
    output_dir2 = "/Users/zehadyzbdullahkhan/Downloads/Brishti/Abstract_Sentences/"


    year = ["1990", "1991", "1992", "1993", "1994"]
    #year = ["1990"]

    #cnt = 0
    line_distribution = [0 for i in range(100)]
    print line_distribution
    for y in year:
      award_dir = "awards_" + y
      award_folder_prefix = "awd_" + y + "_"

      for id in range (0, 97):
      #for id in range (0, 1):
        #cnt = cnt + 1 
        #if cnt == 10:
        #   break
        award_folder_index = "%02d" %id
        file_format = ".txt"

        #print award_folder_index

        filepath = data_dir + award_dir + "/" + award_folder_prefix + award_folder_index + "/"

        #print folder_name

       # filepath = 'abstract_list.txt'
        for filename in glob.glob(filepath + '*.txt'):
          abstract = open(filename, 'r')
          out_name = filename.replace("/","_")
          #print out_name
          #print abstract
          output_file = open(output_dir1 + out_name + '_parsed_abstracts.txt', 'w')
      #
      #     for abstract_filename in abstract_file_list:
      #         print abstract_filename.rstrip()
      #         abstract = open(abstract_filename.rstrip(), 'r')
  
          abstract_record = []
          abstract_text = ''
          
          for line in abstract:
            line = line.rstrip()
            line = line.split(':')
            if line[0] == 'NSF Org     ' or line[0] == 'Award Number':
                abstract_record.append(line[1].strip())
    
            if line[0] == 'Abstract    ':
                for line in abstract:
                    abstract_text = abstract_text + line.rstrip()
                abstract_text = ' '.join(abstract_text.split())
                abstract_record.append(abstract_text)
                #print abstract_text
                break
  
          output_file.write('<>'.join(abstract_record)+'\n')
  
  
          abstract.close()
  
          output_file.close()
     
          #parsed_file = open('parsed_abstracts.txt', 'r')
          parsed_file = open(output_dir1 + out_name + '_parsed_abstracts.txt', 'r')
          fi = output_dir1 + out_name + '_parsed_abstracts.txt'
          print "Begin Tokenization... on " + fi  
          output_file = open(output_dir2 + out_name + '_abstract_sentences.txt', 'w')
          fo = output_dir2 + out_name + '_abstract_sentences.txt'
     
          tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
     
          for line in parsed_file:
              if line.isspace():
                  continue
              else:
                  if len(line.split('<>')) <= 3:
                      (nsf_agency, award_number, abstract) = line.split('<>')
     
              if abstract.isspace():
                  continue
              else:
                  # Remove non-ASCII characters
                  abstract = ''.join([i if ord(i) < 128 else '' for i in abstract])
     
                  # Tokenize sentences
                  sentences = tokenizer.tokenize(abstract.rstrip())
     
                  if '***' in sentences[-1]:   # Error check
                      sentences.pop()
                  
                  sent_cnt = 0
                  for sentence in sentences:
                      sent_cnt += 1
                      print "saving abstract sentences to " + fo 
                      output_file.write(str(award_number)+'|'+str(sentences.index(sentence))+'|'+sentence+'\n')
                  line_distribution[sent_cnt] += 1

          output_file.close()
          parsed_file.close()
          print "End Tokenization of the file."

    print line_distribution 
    line_dist_file = open(data_dir + "../line_distribution.txt", "w")
    for i in range(0,len(line_distribution)):
        line_dist_file.write(str(i) + " " + str(line_distribution[i]) + "\n")
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
