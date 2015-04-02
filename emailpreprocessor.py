from os import listdir
import re

def main(argv):
	keptFiles = []
	keptRE = re.compile("edrm-enron-v2_.*-._xml\.zip")

	for filename in os.lisdir(argv[0]):
		if (keptRE.match(filename):
			print filename
	
if __name__ == "__main__": 
    main(sys.argv) 
