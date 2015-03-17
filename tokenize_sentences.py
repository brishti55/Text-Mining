#!/usr/bin/env python
import sys
import nltk
import nltk.data

def main():
    #my_id=sys.argv[1]
    parsed_abstract_file='parsed_abstracts.txt'
    abstract_sentence_file='abstract_sentence.txt'


    parsed_file = open( parsed_abstract_file, 'r')
    output_file = open(abstract_sentence_file, 'w')

    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

    for line in parsed_file:
        if line.isspace():
            continue
        else:
            if len(line.split('^')) <= 3:
                (nsf_agency, award_number, abstract) = line.split('^')
                
                print line

        if abstract.isspace():
            continue
        else:
        # Remove non-ASCII characters
            abstract = ''.join([i if ord(i) < 128 else '' for i in abstract])

            # Tokenize sentences
            sentences = tokenizer.tokenize(abstract.rstrip())

            if '***' in sentences[-1]:   # Error check
                sentences.pop()

            for sentence in sentences:
                output_file.write(str(award_number)+'|'+str(sentences.index(sentence))+'|'+sentence+'\n')

    output_file.close()
    parsed_file.close()
    print "End..."

if __name__ == "__main__":
    main()
