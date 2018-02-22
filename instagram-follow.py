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

client = InstagramAPI.InstagramAPI(USERNAME, PASSWORD)
if client.login():
	followers = client.getTotalFollowers(client.username_id)
	followings = client.getTotalFollowings(client.username_id)
	followings_pks = [f['pk'] for f in followings]

	to_follow = []
	for follower in followers:
		if follower['pk'] in followings_pks:
			continue
		to_follow.append(following)

	followed = 0
	for person in to_follow:
		if client.follow(person['pk']):
			print("Followed: " + person['username'])
			followed += 1
		else:
			print("==================================")
			print("Failed. " + str(len(to_follow) - followed) + "remaining")
			break	
	print("Followed: " + str(unfollowed))

	client.logout()

print("DONE. Press 'ENTER' to continue...")
input()
