import sys
if sys.version_info[0] < 3:
    import got
else:
    import got3 as got

def main():

	def printTweet(descr, t):
		print(descr)
		print("Username: %s" % t.username)
		print("Retweets: %d" % t.retweets)
		print("Text: %s" % t.text)
		print("Mentions: %s" % t.mentions)
		print("Hashtags: %s\n" % t.hashtags)

	# Example 2 - Get tweets by query search
	tweetCriteria = got.manager.TweetCriteria().setQuerySearch('#FPL #GW9').setSince("2018-10-08").setUntil("2018-10-20").setMaxTweets(10)
	for tweet in got.manager.TweetManager.getTweets(tweetCriteria):
		print(tweet.text)
		print("\n\n")

if __name__ == '__main__':
	main()
