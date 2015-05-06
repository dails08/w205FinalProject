#!/usr/bin/python

import re
import sys


def main(argv):
	fromRE = re.compile("^From: ([^<\[]*)")# ([a-zA-Z0-9_,])* <")
	emailAddressRE = re.compile("([^@\s<]+@[^@]+\.[^@\s>]+)")
	nameRE = re.compile("  ")
	

	
	while True:
		s = sys.stdin.readline()
		if not s:
			break
		
		if fromRE.match(s):
			
			match = fromRE.search(s).group(1).strip()
			if match is not None:
				print "LongValueSum:" + match + "\t" + "1"
				
if __name__ == "__main__": 
    main(sys.argv) 
