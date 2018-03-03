import InstagramAPI
import logging
import json
import time

logging.basicConfig(filename='instascript.log', level=logging.DEBUG)

USERNAME = ''
PASSWORD = ''
with open("settings.json") as f:
	settings = json.load(f)
	USERNAME = settings['username']
	PASSWORD = settings['password']

logging.info("the username is [{0}]. the password is [{1}].".format(USERNAME, PASSWORD))

BLACKLIST = []
with open('blacklist.txt') as f:
	for line in f:
		BLACKLIST.append(line.strip())
logging.info("number of blacklisted friends: [{0}]".format(str(len(BLACKLIST))))

failed = True
while failed:

		failed = False
		client = InstagramAPI.InstagramAPI(USERNAME, PASSWORD)
		if client.login():
		followers = client.getTotalFollowers(client.username_id)
		followings = client.getTotalFollowings(client.username_id)
		followers_usernames = [f['username'] for f in followers]

		to_remove = []
		for following in followings:
			if following['username'] in BLACKLIST:
				continue
			if following['username'] in followers_usernames:
				continue
			to_remove.append(following)

		unfollowed = 0
		for person in to_remove:
			if client.unfollow(person['pk']):
				print("Unfollowed: " + person['username'])
				unfollowed += 1
			else:
				print("==================================")
				print("Failed. " + str(len(to_remove) - unfollowed) + "remaining")
				failed = True
				break	
		print("Unfollowed: " + str(unfollowed))

		client.logout()

		if failed:
			print('RETRYING...')
			time.sleep(5)

print("DONE. Press 'ENTER' to continue...")
input()
