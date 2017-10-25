import tweepy
import keys

# Create variables for each key, secret, token
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)
api = tweepy.API(auth)

# Write a tweet to push to our Twitter account
# tweet = 'apparently, status can\'t be duplicates'
# api.update_status(status=tweet)

# for status in tweepy.Cursor(api.user_timeline, screen_name='calua').items(20):
#   print(status.text)


for status in tweepy.Cursor(api.search, q='"me sentindo"', lang="pt").items(100):
  print(status._json['user']['screen_name'])