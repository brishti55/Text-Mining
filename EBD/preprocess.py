#!/usr/bin/env python
from __future__ import division, unicode_literals
import os
import re
import glob
import sys, string
import math
import csv
import operator
from operator import itemgetter
from textblob import TextBlob as tb
import nltk
import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import Counter

def main():
    
    data_dir = "/Users/Brishti/Documents/fall2015_classes/SODA_EVD/Assignment6/LIS590AG_Assignment6/NSF_Part1/"
    out_filepath = "/Users/Brishti/Documents/fall2015_classes/SODA_EVD/Assignment6/output/"
    
    year = ["1990", "1991", "1992", "1993", "1994"]
    
    for y in year:
        award_dir = "awards_" + y
        award_folder_prefix = "awd_" + y + "_"
        
        for id in range (0, 97):
            award_folder_index = "%02d" %id
            
            filepath = data_dir + award_dir + "/" + award_folder_prefix + award_folder_index + "/"
    
    
            for filename in glob.glob(filepath + '*.txt'):
                print filename
        
                content = open(filename, 'r')
                filename_extract = re.search(r'(a[0-9].*)', filename)
                out_name = filename_extract.group(0)
                output_file = open(out_filepath + out_name, 'w')

                all_text = []
                abstract = ''
                for line in content:
                    line = filter(lambda x: x in string.printable, line)
                    line = line.rstrip()
                    line = line.split(':')

                    if line[0] == 'NSF Org     ' or line[0] == 'Title       ':
                        all_text.append(line[1].strip())


                    if line[0]== 'Abstract    ':
                        for line in content:
                            # print line
                            line = filter(lambda x: x in string.printable, line)
                            # line = line.encode('ascii',errors='ignore')
                            abstract = abstract + line.rstrip()
                        # abstract = ' '.join([i if ord(i) < 128 else '' for i in abstract])
                        abstract = ' '.join(abstract.split())
                        all_text.append(abstract)
                
                output_file.write(' '.join(all_text))
        
        
                content.close()
                output_file.close()

    
if __name__ == "__main__":
    main()
        

