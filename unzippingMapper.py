#!/usr/bin/python
import re
import sys
import boto
import zipfile
from boto.s3.key import Key
from boto.s3.connection import S3Connection
from boto.utils import get_instance_metadata
from boto.sts import STSConnection


#read from stdin
#expects a line with exactly one filename
#reaches out to a specific S3 bucket and pulls that file
#unzips it
#And analyzes the text emails in it
#then deletes the unzipped files

def main(argv):
	
	#print "started"
	
	#establish instance credentials
	
	#instanceMD = boto.utils.get_instance_metadata()
	
	#accesKey = instanceMD['iam']['security-credentials']['get-enron-zips']['AccessKeyId']
	#secretKey = instanceMD['iam']['security-credentials']['get-enron-zips']['SecretAccessKey']
	
	#stsconn = boto.sts.STSConnection(accesKey, secretKey)
	
	
	#sts_connection = STSConnection()
	#assumedRoleObject = sts_connection.assume_role(role_arn="arn:aws:iam::321504313022:role/get-enron-zips", role_session_name="AssumeRoleSession1")

	# Use the temporary credentials returned by AssumeRole to call Amazon S3  
	# and list all buckets in the account that owns the role (the trusting account)
	#print "Connecting"
	#s3conn = S3Connection(aws_access_key_id=assumedRoleObject.credentials.access_key, aws_secret_access_key=assumedRoleObject.credentials.secret_key, security_token=assumedRoleObject.credentials.session_token)
	s3conn = S3Connection()
	#print "Connected"
	
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

		zipbucket = s3conn.get_bucket("chrisdailey1-enron")
		#print "Got bucket"
		
		k = Key(zipbucket)
		k.key = "zips/" + s
		#print "Saving"
		k.get_contents_to_filename(s)
		#print "Saved"
		try:
			z = zipfile.ZipFile(s, 'r')
		except zipfile.BadZipfile as e:
			print e
			continue
		shortname = re.match("edrm-enron-v2_(.*-.*)_xml\.zip", s).group(1)
		#print "making directory"
		if not os.path.exists(shortname):
			os.makedirs(shortname)
		#print "Made"
		#print "Extracting"
		z.extractall(shortname + "/")
		#print "Extracted"
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
					#print "Opening textfile"
					emailText = open(textDirectory + "/" + textFile, 'r')
					#print "Opened"
					#emit keys
					if (fromRE.match(s)):
						if (emailAddressRE.search(s)):
							addy = emailAddressRE.search(s).group(1)
							if (len(addy) < 50):
								#print "Emitting"
								print "LongValueSum:" + addy.lower() + "\t" + "1"
								#print "Emitted"
					#close it
					emailText.close()

		
		#delete their special folder since it's not needed anymore
		#if we leave it we'll take up a ton of space (presumably)
		#with everyone's unzipped emails
		#print "Deleting"
		shutil.rmtree(shortname+"/")
		#print "Deleted"
		
		
		
		
		
		
		
		



if __name__ == "__main__": 
    main(sys.argv) 
