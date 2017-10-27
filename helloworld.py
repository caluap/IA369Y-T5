import tweepy
import json
import keys #meus dados secretos de login!

# Create variables for each key, secret, token
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

n_usuarios_confessionais = 1000

filtros = '-filter:retweets -filter:replies -filter:links -filter:images -filter:videos'


print(">>> quem fala “me sentindo”? <<<")
tweets_confessionais = tweepy.Cursor(api.search, q='"me sentindo" ' + filtros, lang="pt", wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items(n_usuarios_confessionais)

cidade1 = 'Rio de Janeiro, Brasil'
cidade2 = 'São Paulo, Brasil'

twitteiros = [[] for _ in range(2)]

for t in tweets_confessionais:
  if t._json['user']['location'] == cidade1: twitteiros[0].append(t._json['user']['screen_name'])
  if t._json['user']['location'] == cidade2: twitteiros[1].append(t._json['user']['screen_name'])

print(f">>> {len(twitteiros[0])} cariocas, {len(twitteiros[1])} paulistanos <<<")

tweets_de_usuarios_confessionais = {}
n_tweets = 200

twitteiros = twitteiros[0] + twitteiros[1]

for quem in twitteiros:
  print(f">>> buscando {n_tweets} de {quem} <<<")
  tweets = tweepy.Cursor(api.search, q="from:%s %s" % (quem,filtros), wait_on_rate_limit = True, wait_on_rate_limit_notify = True).items(n_tweets)
  tweets_de_usuarios_confessionais[quem] = []
  for tweet in tweets:
    dados = {
      'text': tweet.text,
      'location': tweet._json['user']['location'],
      'id': str(tweet.id),
      'hashtags': tweet.entities['hashtags'],
      # 'coordinates':str(tweet.coordinates),
      'timestamp': str(tweet.created_at)
    }
    tweets_de_usuarios_confessionais[quem].append(dados)

with open('data.json','w') as fp:
   json.dump(dict(tweets_de_usuarios_confessionais), fp)

