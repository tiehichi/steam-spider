import requests
import re

base_url = 'https://store.steampowered.com/app/'
appids = range(0, 1000)
cookie = {}

cookie['mature_content'] = '1'
cookie['birthtime'] = '-157795199'
cookie['lastagecheckage'] = '1-January-1965'
cookie['Steam_Language'] = 'schinese'
cookie['bShouldUseHTML5'] = '1'

for appid in appids:
	r = requests.get(base_url + str(appid), allow_redirects = False, cookies = cookie)
	if r.status_code == 302:
		if re.search(base_url + str(appid), r.headers['Location']) != None:
			print 'Found Game in ' + str(appid)
	elif r.status_code == 200:
		print 'Found Game in ' + str(appid)
	else:
		print 'Error in ' + str(appid)
		print 'Status Code ' + str(r.status_code)
