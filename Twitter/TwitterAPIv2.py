import sys
import json
import External.OldTweets.got3 as got

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)

	with open('gameweekDates.json', 'r') as file:
		data = json.load(file)

	for gw in data:
		since = data[gw]['since']
		until = data[gw]['until']
		currentGW = 'GW'+gw

		tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#FPL #'+currentGW).setSince(since).setUntil(until).setMaxTweets(1000)

		gwTweets = []
		for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
			text = str(tweet.text.encode("utf-8"))
			gwTweets.append(text)

		with open('GW_Tweets2/' + gw + '.json', 'w') as f:
			i = 1
			for text in gwTweets:
				f.write(str(i)+": %s\n" %text)
				i+=1
		print("GW"+gw+" :"+str(i))


if __name__ == '__main__':
	main()
