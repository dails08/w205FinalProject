#!/usr/bin/python
import re
import sys
import boto
import zipfile
from boto.s3.key import Key
from boto.s3.connection import S3Connection


#read from stdin
#expects a line with exactly one filename
#reaches out to a specific S3 bucket and pulls that file
#unzips it
#And analyzes the text emails in it
#then deletes the unzipped files

def main(argv):
	
	
	
	dateRE = re.compile("^Date: .*")
	subjectRE = re.compile("^Subject: .*")
	fromRE = re.compile("^From: .*")
	toRE = re.compile("^To: .*")
	origMessageRE = re.compile("-----Original Message-----")
	emailAddressRE = re.compile("<([^@]+@[^@]+\.[^@]+)>") 
	while True:
		s = sys.stdin.readline()
		if not s:
			break
		#download
		conn = boto.connect_s3()
		zipbucket = conn.get_bucket("chrisdailey1-enron")
		
		k = Key(zipbucket)
		k.key = "zips/" + s
		k.get_contents_to_filename(s)
		try:
			z = zipfile.ZipFile(s, 'r')
		except zipfile.BadZipfile as e:
			print e
			continue
		shortname = re.match("edrm-enron-v2_(.*-.*)_xml\.zip", s).group(1)
		if not os.path.exists(shortname):
			os.makedirs(shortname)
		z.extractall(shortname + "/")
		#the email unzip into a couple of different folder, one of which stores
		#only the text of the email.  I think I've seen folders with more than one text
		#folder, so go through them one by one and if they match the name format
		#of the text-only folders, use that folder
		for lineEntry in os.listdir(shortname+"/"):
			#Check for that format I mentioned
			if (re.match("text_.*", lineEntry)):
				#store the directory to make more readable code
				textDirectory = shortname + "/" + lineEntry
				#go through each text file
				for textFile in os.listdir(textDirectory):
					#read it
					emailText = open(textDirectory + "/" + textFile, 'r')
					#emit keys
					if (fromRE.match(s)):
						if (emailAddressRE.search(s)):
							addy = emailAddressRE.search(s).group(1)
							if (len(addy) < 50):
								print "LongValueSum:" + addy.lower() + "\t" + "1"
					#close it
					emailText.close()

		
		#delete their special folder since it's not needed anymore
		#if we leave it we'll take up a ton of space (presumably)
		#with everyone's unzipped emails
		shutil.rmtree(shortname+"/")
		
		
		
		
		
		
		
		



if __name__ == "__main__": 
    main(sys.argv) 
