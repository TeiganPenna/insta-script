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

three_days_ago = int(time.time()) - 259200 #60*60*24*3

client = InstagramAPI.InstagramAPI(USERNAME, PASSWORD)
try:
	if client.login():
		followers = client.getTotalSelfFollowers()

		followers_with_no_posts = []
		for follower in followers:
			if follower['is_private']:
				continue

			posts = client.getTotalUserFeed(follower['pk'], three_days_ago)
			
			if len(posts) == 0:
				followers_with_no_posts.append(follower)
				continue

			print("Liking posts from " + follower['username'])
			
			liked = 0
			for post in posts:
				if client.like(post['id']):
					liked += 1
				else:
					print("==================================")
					print("Failed. Successfully liked " + str(liked) + "posts from " + follower['username'])
					break
			print("   Liked " + str(liked) + " posts")
		
		print()
		for follower_with_no_posts in followers_with_no_posts:
			print(follower_with_no_posts['username'] + " had no posts in the last 3 days")

		client.logout()
finally:
	client.logout()

print("DONE. Presse 'Enter' to continue...")
input()