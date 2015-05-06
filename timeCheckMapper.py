#!/usr/bin/python

import re
import sys


def main(argv):
	dateRE = re.compile("^Date: (...), (..) (...) (....) (..):..:.. -.... \(...\)")
		
		
		
	while True:
		s = sys.stdin.readline()
		if not s:
			break
		
		if dateRE.match(s):
			hour = dateRE.search(s).group(5)
			if hour is not None:
				print "LongValueSum:" + hour + "\t" + "1"



if __name__ == "__main__": 
    main(sys.argv) 
