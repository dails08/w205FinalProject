import re

fv = open("processed_mr_featurevector.txt", 'r')
fv2 = open("reprocessed_mr_featurevector.txt", 'w')

for line in fv.readlines():
	fv2.write(re.sub("\"", "", line))
