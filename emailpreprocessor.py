from os import listdir
import re

keptFiles = []
keptRE = re.compile("edrm-enron-v2_.*-._xml\.zip")

for filename in os.lisdir():
	if (keptRE.match(filename):
		print filename
	
