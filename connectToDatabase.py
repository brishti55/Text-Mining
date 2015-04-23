import mysql.connector
import re
import string
# import p

cnx = mysql.connector.connect(user='root', database='NJKHAN2')
cursor = cnx.cursor()
operation = 'SELECT * from tfidftopranked500 order by tfidf desc'
str=""
tfidf=[]
regex = re.compile(r'[a-z]{4}') 
def num_there(s):
    return any(i.isdigit() for i in s)
for result in cursor.execute(operation, multi=True):
  if result.with_rows:
    res = result.fetchall()
    cnt = 0
    for a,w,tf in res:
        m =regex.match(w)
        if m and str.find(w) == -1 and not num_there(w) and "-" not in w and "/" not in w and "." not in w:
           str += "\'" + w + "\', "
           cnt += 1
           tfidf.append(tf)
           if cnt > 500:
               break;
  else:
    print("Number of affected rows: {}".format(result.rowcount))
print "(" + str + ")" 
print cnt
print tfidf
