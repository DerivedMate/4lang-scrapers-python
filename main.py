#!/usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import random
import os
import re
import string
import multiprocessing as mp

def getHTML(url):
	print("----- Starting %s -----" % url)
	req = requests.get(url)
	return req.text

def getUrls(html):
	soup = BeautifulSoup(html, features='html5lib')
	imgs = soup.find_all(name="img")
	print("Found %s images" % len(imgs))
	return [img['src'] for img in imgs]

def getFilename(ext):
	name = './images/'
	alph = string.ascii_lowercase
	max_i = len(alph) - 1
	for _ in range(20):
		name += alph[random.randint(0, max_i)]

	return name + ext

def downloadImages(imgs):
	def validate(url):
		return bool(re.match(r'^https?://', url))

	def download(url):
		print("Downloading %s..." % url[:50])
		return requests.get(url).content

	for src in imgs:
		if not validate(src):
			print("Skipping %s : Invalid URL" % src)
			continue

		matches = re.findall(r'(\.\w{3,4})(?:\?.+)?$', src)
		if len(matches) == 0:
			print("Ext not found %s : supplying .jpg" % src)
			matches.append(".jpg")

		ext = matches[0]
		open(getFilename(ext), 'wb').write(download(src))

def takeCareOfURL(url):
	html = getHTML(url)
	imgs = getUrls(html)
	downloadImages(imgs)
	print("----- Finished %s -----\n\n" % url)
	return len(imgs)

def main():
	base_url = "https://www.deviantart.com/?offset=%s"
	space = 50
	total = 0
	urls = [base_url % (n * space) for n in range(8)]

	pool = mp.Pool(mp.cpu_count())
	results = pool.map(takeCareOfURL, [url for url in urls])
	pool.close()

	for amount in results:
		total += amount

	print("Downloaded %s images" % total)

if __name__ == "__main__":
	main()
