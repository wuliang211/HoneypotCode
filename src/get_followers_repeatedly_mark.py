import json
import time
import calendar
from datetime import datetime
from twython import Twython
import random
import os
import codecs

def get_bots():
	bots = []
	#### GET BOT APP INFO ####
	for file in os.listdir("./"):
		if file.endswith(".tsv") and file.startswith("accounts"):
			with codecs.open(file,'r',encoding='utf-8') as i:
				next(i)
				for line in i:
					line = line.strip()
					bots.append(bot(line))
	return bots

class bot:
	def __init__(self,line):
		tokens = line.split('\t')
		self.name = tokens[0]
		self.ckey = tokens[4]
		self.csecret = tokens[5]
		self.atoken = tokens[6]
		self.asecret = tokens[7]
		self.twython = Twython(self.ckey,self.csecret,self.atoken,self.asecret)

bots = get_bots()

while True:
	for bot in bots:
		cur_time = calendar.timegm(datetime.utcnow().utctimetuple())
		next_cursor = -1
		page = 1
		success = False

		try:
			while next_cursor != 0:
				followers = bot.twython.get_followers_list(screen_name=bot.name, count=200, cursor=next_cursor)
				if not os.path.exists("follow_data/" + bot.name):
					os.makedirs("follow_data/" + bot.name)
				json.dump(followers, open("follow_data/%s/followers_%d_page%d.json" % (bot.name,cur_time, page), "w"))

				page += 1

				next_cursor = followers['next_cursor']
				print(next_cursor)
				success = True
		except Exception,e:
			print str(e)
			print("Failed... %d" % cur_time)

	print("%d %s" % (cur_time, success))
	if success:
		#wait 15 minutes
		print("Sleeping 15 minutes... %d" % cur_time)
		time.sleep(15 * 60)
	else:
		print("Sleeping 30 minutes... %d" % cur_time)
		time.sleep(30 * 60)