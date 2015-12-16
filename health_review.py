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
    data_output2 = "/Users/Brishti/Documents/spring2015_classes/text_mining/Final_Project/summary2.txt"
    
    input_file = open(data, 'r')
    output_file = open(data_output1, 'w')
     
    review = []
    prodIDs = []
    review_text = ''
     
    for line in input_file:
      line = line.rstrip()
      line = line.split(':')
      if line[0]=='product/productId' or line[0]=='review/userId' or line[0]=='product/title' or line[0]=='product/price' or line[0]=='review/score' or line[0]=='review/text':
         word = line[1].strip()
#          print str
         if line[0]=='product/productId':
            prodIDs.append(word)
          
         review.append(word)
 
      if line[0]== '':
         review.append('\n')
         output_file.write('<>'.join(review))
         review = []
          
    print "finished"
    if line[0]== '':
         review.append('\n')
          
    input_file.close()
    output_file.close()
    
    
    prodIDs = sorted(set(prodIDs)) 
     
    id_of_product = ''
    ids = [id_of_product]*len(prodIDs)
    for i in range(len(prodIDs)):
        ids[i]= id_of_product
     
    title_of_product = ''
    title_of_products = [title_of_product]*len(prodIDs)
    for i in range(len(prodIDs)):
        title_of_products[i] = title_of_product 
     
    count_product = 0
    count_products = [count_product]*len(prodIDs)
    for i in range(len(prodIDs)):
        count_products[i] = count_product
     
    rev_num_per_product = 0
    rev_num_of_products = [rev_num_per_product]*len(prodIDs)
    for i in range(len(prodIDs)):
        rev_num_of_products[i] = rev_num_per_product 
     
    score_per_product = 0
    score_of_products = [score_per_product]*len(prodIDs)
    for i in range(len(prodIDs)):
        score_of_products[i] = score_per_product
     
    price_per_product = 0
    price_of_products = [price_per_product]*len(prodIDs)
    for i in range(len(prodIDs)):
        price_of_products[i] = price_per_product
     
    input_file = open(data, 'r')
    prodID = ''
    prodIndex = -1
    for line in input_file:
      line = line.rstrip()
      line = line.split(':')
       
      if line[0]=='product/productId' or line[0]=='product/title' or line[0]=='product/price' or line[0]=='review/score' or line[0]=='review/text':
         word = line[1].strip()
#          if line[0]=='review/text':
#              rev = line[1].strip()
#              rev_per_product.append(rev)
              
         if line[0]=='product/productId':
             prodID = line[1].strip()
             
             if prodID in prodIDs:
                 prodIndex = prodIDs.index(prodID)
                 count_products[prodIndex] = count_products[prodIndex] + 1
         if prodID != '' and prodIndex != -1:
             if line[0]=='product/productId':
                 prodID = line[1].strip()
                 ids[prodIndex] = prodID
             if line[0]=='product/title':
                 title = line[1].strip()
                 title_of_products[prodIndex] = title
             if line[0]=='product/price':
                 price = line[1].strip()
                 price_of_products[prodIndex] = price
             if line[0]=='review/score':
                 score = line[1].strip()
                 score_of_products[prodIndex] = score_of_products[prodIndex] + float(score)
                 a = price_of_products[prodIndex]
                 b = score_of_products[prodIndex]
                 c = count_products[prodIndex]
                 d = title_of_products[prodIndex]
#                  print d,b,c,a 
#                  print '\n'
     
    output_file = open(data_output2, 'w')
     
    sorted_count = sorted(count_products)
    sorted_count.reverse()
    sorted_index = [0]*(len(sorted_count))
    for i in range(len(sorted_count)):
        sorted_index[i] = count_products.index(sorted_count[i])
     
    for i in range(len(prodIDs)):
        prodID = ids[sorted_index[i]]
        title = title_of_products[sorted_index[i]]
        count = str(count_products[sorted_index[i]])
        if type(price_of_products[sorted_index[i]]) == float:
            price = '%.2f' % price_of_products[sorted_index[i]]
        else:
            price = price_of_products[sorted_index[i]]
             
        score = '%.2f' % score_of_products[sorted_index[i]]
        average = '%.2f' % (float(score)/float(count))
        output_file.write(prodID+'\t'+title +'\t'+ count +'\t'+ price +'\t'+ average + '\n')
        print title +'\t'+ count +'\t'+ price +'\t'+ average
        print ''
       
    input_file.close()
    output_file.close()
     
if __name__ == "__main__":
    main()