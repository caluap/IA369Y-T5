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


# passo 1: identificar usuários que tuitaram “me sentindo”. registrar o momento do tweet em questão junto com o screen_name
# passo 2: buscar 100 tweets anteriores a esse momento, 100 tweets seguintes. limitar a 100 usuários.
#   sub-passo 2: deve-se ignorar tweets que sejam em:
#     - resposta a alguém
#     - retweets
# passo 3: salvar os tweets em um arquivo json (manter formato do twitter). 

n_tweets = 10

filtro = '-filter:retweets -filter:replies -filter:links -filter:images -filter:videos'

# pega tweets de um ano atrás, pois quero que o passado e o futuro sejam suficientemente grandes
tweets_emotivos = tweepy.Cursor(api.search, q='me sentindo until:2017-01-01 ' + filtro, lang="pt").items(n_tweets)

for t in tweets_emotivos:
  print(t.text)

id_tweets = []

for tweet in tweets_emotivos:
  id_tweets.append((tweet._json['user']['screen_name'],tweet.id))

n_anteriores = 5
n_proximos = 5

for (quem, id_tweet) in id_tweets:
  anteriores = []
  proximos = []
  
  tweets_anteriores = tweepy.Cursor(api.user_timeline,screen_name=quem,result_type='recent',max_id=id_tweet).items(n_anteriores)
  tweets_proximos =  tweepy.Cursor(api.user_timeline,screen_name=quem,result_type='recent',since_id=id_tweet).items(n_proximos)
  for s in tweets_anteriores:
    print("%s > %s" % (quem,s.text))
  for s in tweets_proximos:
    print("%s > %s" % (quem,s.text))