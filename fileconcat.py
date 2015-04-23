import os,sys,glob

data_dir = "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/abstract_words/"
output_dir =  "/Users/Brishti/Documents/spring2015_classes/text_mining/python-codes/python-output/abstract_words_total/"

outf = open(output_dir + "abstract_words_total.txt","a")

for filename in glob.glob(data_dir + '*.txt'):
    parsed_file = open(filename, 'r')
    print filename
    for line in parsed_file:
        #print ""
        outf.write(line)