#!/usr/bin/python
import re
import sys

dateRE = re.compile("^Date: .*")
subjectRE = re.compile("^Subject: .*")
fromRE = re.compile("^From: .*")
toRE = re.compile("^To: .*")
origMessageRE = re.compile("-----Original Message-----")

emailAddressRE = re.compile("<[^@]+@[^@]+\.[^@]+>")


lines = [
"From: Miller  Don (Asset Mktg) <Don.Miller@ENRON.com>",
"From: Deffner  Joseph <Joseph.Deffner@ENRON.com>",
"From: Richardson, James <James.Richardson@ENRON.com>",
"From: Ghosh, Soma",
"From: Martin.Woodhams@barclayscapital.com",
"From: Schoppe  Tammie <Tammie.Schoppe@ENRON.com>",
"From: Lavorato  John <John.Lavorato@ENRON.com>",
"From: Gillespie  John <John.Gillespie@ENRON.com>",
"From: Billing Dept <paymentz_935@hanmail.net>",
]
	
for line in lines:
	if (fromRE.match(line)):
		if (emailAddressRE.search(line)):
			print "LongValueSum: " + emailAddressRE.search(line).group(0) + "\t1"
		
		
