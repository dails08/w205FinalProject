import os
import re
import sys
from subprocess import call
import zipfile

#this script accepts an argument consisting of a directory.
#It finds all the files in that directory that match the
#Enron filename format and extracts them to folders that
#match the name of the person who wrote the emails.

def main(argv):
	keptFiles = []
	keptRE = re.compile("edrm-enron-v2_.*-.*_xml\.zip")
	
	baseDir = argv[1]
	
	for filename in os.listdir(baseDir):
		if (keptRE.match(filename)):
			keptFiles.append(filename)
			print filename
			
	for filename in keptFiles:
		print filename
		z = zipfile.ZipFile(filename, 'r')
		shortname = re.match("edrm-enron-v2_(.*-.*)_xml\.zip", filename).group(1)
		if not os.path.exists(baseDir + "/" + shortname):
			os.makedirs(baseDir + "/" + shortname)
		z.extractall(baseDir + "/" + shortname)
		
		
		
	
if __name__ == "__main__": 
    main(sys.argv) 
