#!/usr/bin/python

#import string
import string
#import regex
import re
#import nltk
import nltk
from nltk.tokenize import RegexpTokenizer


#start process_email
def processEmail(email):
    # process the emails
    #Convert [InternetShortcut] URL=www.* or http://* to PERSONALURL
    email = re.sub('((URL=www\.[^\s]+)|(URL=http://[^\s]+))','PERSONALURL',email)
    #Convert [InternetShortcut] URL=mailto to BUSINESSURL
    email = re.sub('URL=mailto:[^\s]+','BUSINESSURL',email)
    #Remove email addresses 
    email = re.sub('[^\s]+@[^\s]+','',email)
    #Remove strings that start with </
    email = re.sub('</[^\s]+','',email)
    #Remove additional white spaces
    email = re.sub('[\s]+', ' ', email)
    #Replace #word with word
    email = re.sub(r'#([^\s]+)', r'\1', email)
    #Convert to lower case
    email = email.lower()
    #trim
    email = email.strip('\'"')
    
    return email
#end

#Read the emails one by one and process it
fr = open('emails.txt', 'rU')
fw = open('processedemails.txt', 'w')
line = fr.readline()

while line:
    processedEmail = processEmail(line)
    fw.write(processedEmail + '\r\n')
    line = fr.readline()
#end loop
fr.close()
