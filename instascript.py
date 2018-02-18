import InstagramAPI
import logging
import json

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

	i = 0
	for person in to_remove:
		client.unfollow(person['pk'])
		i += 1
	print(i)

	client.logout()
