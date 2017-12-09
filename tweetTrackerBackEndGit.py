import pyrebase
import time
#from twython import Twython
import tweepy
import json

allHandles=set()


def stream_handler(message):
	#print (message)
	all_users = db.child("Users").get().val()
	#print (all_users)

	global allHandles
	allHandles=set()

	for i in all_users:
		userD = all_users[i]
		userL = userD["list"]
		userL = userL.replace(" ", "")
		userL = userL.split(",")
		for j in userL:
			allHandles.add(j)
	
	#print (allHandles)


config = {
  "apiKey": "",
  "authDomain": "",
  "databaseURL": "",
  "storageBucket": ""
}

consumer_key = ''
consumer_secret = ''
access_token = ''
access_secret = ''


auth = tweepy.OAuthHandler(consumer_key,consumer_secret)
auth.set_access_token(access_token,access_secret)
client = tweepy.API(auth)


firebase = pyrebase.initialize_app(config)
db = firebase.database()
my_stream = db.child("Users").stream(stream_handler)


latestTweets=dict()

# for i in allHandles:
# 	if i not in latestTweets:
# 		latestTweets[i]=0
# 	tweet = client.user_timeline(id = i, count = 1)[0]	
# 	tweetId = tweet.id
# 	if latestTweets[i]!=tweetId:
# 			latestTweets[i]=tweetId

while(1):
	#print(allHandles)

	for i in allHandles:

		if i not in latestTweets:
			latestTweets[i]=0

		tweet = client.user_timeline(id = i, count = 1)[0]
		
		tweetId = tweet.id
		
		tweetText = tweet.text
		tweetPicURL = tweet.user.profile_image_url
		tweetUserName = tweet.user.screen_name

		if latestTweets[i]!=tweetId:

			latestTweets[i]=tweetId

			#ADD TWEET TO DB
			#tweet = json.dumps(tweet._json)
			db.child("allTweets").push(tweet._json)


			#SET FB FOR HANDLE
			all_users = db.child("Users").get().val()

			for singleUser in all_users:

				userD = all_users[singleUser]
				userL = userD["list"]
				userL = userL.replace(" ", "")
				userL = userL.split(",")
				flag=0
				for h in userL:
					if h==i:
						flag=1


				
				tweetMedia = 0
				if "media" in tweet.entities:
					tweetMedia = 1


				textContent = tweetText.split(" ")

				if len(textContent) == 1:
					word = textContent[0]
					if (word[0] == 'h' and word[1] == 't' and word[2] == 't' and word[3] == 'p'):
						tweetlen=0
				else:
					tweetlen=len(textContent)



				userMediaType = userD["type"]

				if (tweetMedia==0 and tweetlen>0 and userMediaType=="text"):
					flag2=1
				elif (tweetMedia==1 and tweetlen>0 and userMediaType=="textAndImage"):
					flag2=1
				elif (tweetMedia==1 and tweetlen==0 and userMediaType=="image"):
					flag2=1
				else:
					flag2=0


				if flag==1 and flag2==1:
					db.child("Users").child(singleUser).child("notif1").set("New tweet from: " + tweetUserName)
					db.child("Users").child(singleUser).child("notif2").set(tweetText)
					db.child("Users").child(singleUser).child("notif3").set(tweetPicURL)
					db.child("Users").child(singleUser).child("notif4").set(tweetUserName)


					db.child("Users").child(singleUser).child("toNotify").set("Yes")

				#print (singleUser,i,flag)



			print (tweetText)



		#print (tweetId)


	time.sleep(10)


















