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

failed = True
while failed:

	failed = False
	client = InstagramAPI.InstagramAPI(USERNAME, PASSWORD)
	if client.login():
		followers = client.getTotalFollowers(client.username_id)
		followings = client.getTotalFollowings(client.username_id)
		followings_pks = [f['pk'] for f in followings]

		to_follow = []
		for follower in followers:
			if follower['pk'] in followings_pks:
				continue
			to_follow.append(follower)

		followed = 0
		
		for person in to_follow:
			if client.follow(person['pk']):
				print("Followed: " + person['username'])
				followed += 1
			else:
				print("==================================")
				print("Failed. " + str(len(to_follow) - followed) + " remaining")
				failed = True
				break	
		print("Followed: " + str(followed))

		client.logout()

		if failed:
			print('RETRYING...')
			time.sleep(5)

print("DONE. Press 'ENTER' to continue...")
input()
