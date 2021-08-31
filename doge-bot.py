from binance.spot import Spot
import client_env
import sys,tweepy, os, re, threading
from os.path import join, dirname
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

prev_tweet_id = ""

# Market order to buy doge
def buy_doge(api_key, api_seccret_key):
    client = Spot()
    client = Spot(key=api_key, secret=api_seccret_key)
    params = {
        'symbol': 'DOGEUSDT',
        'side': 'BUY',
        'type': 'MARKET',
        'quantity': 50
    }
    response = client.new_order(**params)
    return response

#authentication function
def twitter_auth():
    try:
        consumer_key = os.environ.get("CONSUMER_KEY") 
        consumer_secret = os.environ.get("CONSUMER_SECRET_KEY") 
        access_token = os.environ.get("ACCESS_TOKEN") 
        access_secret = os.environ.get("ACCESS_TOKEN_SECRET")
    except KeyError:
        sys.stderr.write("TWITTER_* environment variable not set\n")
        sys.exit(1)
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    return auth

#authenticate twitter client
def get_twitter_client():
    auth = twitter_auth()
    client = tweepy.API(auth, wait_on_rate_limit=True)
    return client

# function to check tweet for doge
def get_tweet():
    user = "elonmusk"
    client = get_twitter_client()
    tweet_data = ''
    
    for status in tweepy.Cursor(client.user_timeline, screen_name=user).items(1):
        tweet_data = status
    
    # check if it is equal to old tweet or invoke a listener for a new tweet
    return tweet_data

# function to check if tweet contains doge
def check_tweet(tweet):
    match_doge = "(d|D)(o|O)(g|G)(e|E)"
    check = re.search(match_doge, tweet)
    
    if check:
        print("Tweet contains doge. Triggering buy via kraken API")
        buy_doge(client_env.api_key, client_env.secret_key)
    else:
        print("Going to sleep for 7 seconds")


# listener function
def trigger():
    global prev_tweet_id
    print("Checking for any new tweets...")
    threading.Timer(7.0, trigger).start()
    tweet = get_tweet()
    if(tweet.id != prev_tweet_id):
        check_tweet(tweet.text)
        prev_tweet_id = tweet.id
    else:
        print('Going to sleep for 7 seconds')
        pass

if __name__ == '__main__':
    trigger()
    # TODO: Add Kraken API to trigger BUY

        
def get_last_tweet(self):
    tweet = self.client.user_timeline(id=self.client_id, count = 1)[0]
    print(tweet.text)