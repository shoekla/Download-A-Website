import urllib
import urllib2
import re
import nltk
import csv
import time
import requests
import string
from bs4 import BeautifulSoup
from BeautifulSoup import BeautifulSoup, SoupStrainer
import urllib2
import os
import shutil



def crawlCSS(url):
	try:
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		arr = []
		check = 0
		for link in soup.findAll('link'):
			href=link.get('href')
			href_test=str(href)
			if href_test.startswith("http") == False:
				arr.append(href_test)
		return arr
	except Exception,e:
		print str(e)

def crawlJS(url):
	try:
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		arr = []
		check = 0
		for link in soup.findAll('script'):
			href=link.get('src')
			href_test=str(href)
			if href_test.startswith("http") == False:
				arr.append(href_test)
		return arr
	except Exception,e:
		print str(e)
def getLinks(arr,name):
	res = []
	if name.endswith("/"):
		for i in arr:
			res.append(name+str(i))
	else:
		for i in arr:
			res.append(name+"/"+str(i))		
	return res
def getReplaceLink(arr):
	res = []
	for link in arr:
		index = link.rfind('/')
		res.append(link[index+1:])
		if link.endswith(".js"):
			res.append("JS/"+link[index+1:])
		else:
			res.append("CSS/"+link[index+1:])
	return res
def getHTML(url):
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)	
	return soup

name = "http://ashobiz.asia/wrapbootstrap/boot-extended161/demo/"
print "CLEARING WORKSPACE"
if os.path.exists("CSS/"):
	shutil.rmtree('CSS/')
if os.path.exists("JS/"):
	shutil.rmtree('JS/')



print "CSS FILES ---------"
originalCSS = crawlCSS(name)
cssLinks = getLinks(originalCSS,name)
updatedCss = getReplaceLink(originalCSS)
print "JS FILES -----------"
originalJS = crawlJS(name)
jsLinks = getLinks(originalJS,name)
updatedJs = getReplaceLink(originalJS)
print "HTML CODE---------"
code = str(getHTML(name))
for i in range(0,len(originalCSS)):
	code = code.replace(originalCSS[i],updatedCss[i])
for i in range(0,len(originalJS)):
	code = code.replace(originalJS[i],updatedJs[i])
print "Aquiring files"
os.makedirs("JS")
os.chdir("JS/")
for i in range(0,len(jsLinks)):
	try:
		testfile = urllib.URLopener()
		testfile.retrieve(jsLinks[i],updatedJs[i][3:])
	except:
		print "Error at "+jsLinks[i]
os.chdir("../")
os.makedirs("CSS")
os.chdir("CSS/")
for i in range(0,len(cssLinks)):
	try:
		testfile = urllib.URLopener()
		testfile.retrieve(cssLinks[i],updatedCss[i][4:])
	except:
		print "Error at "+cssLinks[i]
os.chdir("../")
f = open('webpage.html','w')
f.write(str(code))
f.close()

"""

f = open('test.html','w')
f.write("test")
f.close()
os.chdir("../")
f = open('test2.html','w')
f.write("test2")
f.close()

"""







