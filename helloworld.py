import tweepy
import json
import keys #meus dados secretos de login!

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

n_usuarios_confessionais = 5

filtros = '-filter:retweets -filter:replies -filter:links -filter:images -filter:videos'

tweets_confessionais = tweepy.Cursor(api.search, q='"me sentindo" ' + filtros, lang="pt").items(n_usuarios_confessionais)

tweets_de_usuarios_confessionais = {}
n_tweets = 5

  # id_tweets.append((tweet._json['user']['screen_name'],tweet.id))

for tweet in tweets_confessionais:
  quem = tweet._json['user']['screen_name']
  tweets = tweepy.Cursor(api.search, q="from:%s %s" % (quem,filtros)).items(n_tweets)
  tweets_de_usuarios_confessionais[quem] = []
  for tweet in tweets:
    dados = {
      'text': tweet.text,
      'geo': str(tweet.geo),
      'id': str(tweet.id),
      'hashtags': tweet.entities['hashtags'],
      # 'coordinates':str(tweet.coordinates),
      'timestamp': str(tweet.created_at)
    }
    tweets_de_usuarios_confessionais[quem].append(dados)

with open('data.json','w') as fp:
   json.dump(dict(tweets_de_usuarios_confessionais), fp)

