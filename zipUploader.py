import os
import re
import sys
import boto
from boto.s3.key import Key
from boto.s3.connection import S3Connection

#this script accepts an argument consisting of a directory.
#It finds all the files in that directory that match the
#Enron filename format and extracts them to folders that
#match the name of the person who wrote the emails.

def main(argv):
	
	#get credentials
	creds = open("credentials", 'r')
	AWSKeyID = creds.readline().rstrip()
	AWSSecret = creds.readline().rstrip()
	creds.close()
	
	
	#S3 context
	conn = S3Connection(AWSKeyID, AWSSecret)
	bucket = conn.get_bucket("chrisdailey1-enron")
	k = Key(bucket)
	
	
	#this is the array that will hold all the file names
	totalListOfFiles = []
	
	bucket = "chrisdailey1-enron"
	
	keptFiles = []
	#The format for the xml, text-only emails
	keptRE = re.compile("edrm-enron-v2_.*-.*_xml\.zip")
	
	#the base directory given at the cli
	baseDir = argv[1]
	
	
	#find the zip files that match the format
	for filename in os.listdir(baseDir):
		listFile = open("fileList.txt", 'a')
		if (keptRE.match(filename)):
			#for error checking, print the filename
			print "Matched " + filename
			print "Writing "+ filename
			listFile.write(filename + "\n")
			#upload it
			print "Setting key"
			k.key = "zips/" + filename
			if (k.exists()):
				print "Already exists.  Skipping."
			else:
				print "Uploading " + filename
				k.set_contents_from_filename(baseDir + "/" + filename)
			listFile.close()

		
		
		
	
if __name__ == "__main__": 
    main(sys.argv) 
