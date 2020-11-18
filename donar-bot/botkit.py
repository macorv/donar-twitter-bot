from dotenv import load_dotenv
import os
import tweepy
import re
import time

load_dotenv()


def authAPI():
    '''
    Authenticates in the Twitter API.

    :params: no params
    '''
    API_KEY = os.getenv('API_KEY')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    ACCESS_TOKEN =  os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
        return api
    except tweepy.error.TweepError as e:
        raise e


def post_processing(raw_tweet):
    '''
    Receives a tweet and search for a pattern match. Returns the id of the tweet with a match.

    :params: raw_tweet: tweet.
    '''
    tweet = raw_tweet._json
    match = re.search('([Nn]ecesit(amos|a|an|o) (\d*)|[Nn]ecesit(amos|a|an|o)|[Bb]uscando) (dadores) (de) (sangre)', tweet['text'])
    if match:
        try:
            tweet_id = tweet['retweeted_status']['id']
        except KeyError:
            tweet_id = tweet['id']
        
        return tweet_id


def wasBotRetweeted(tweet):
    '''
    Checks if a tweet was RT'd before by the Bot

    :params: tweet: JSON representation of the tweet.
    '''
    return tweet['retweeted']


def wasBotFavorited(tweet):
    '''
    Checks if a tweet was favorited before by the Bot.

    :params: tweet: JSON representation of the tweet.
    '''
    return tweet['favorited']


def isRetweet(tweet):
    '''
    Checks if a tweet is a retweet.

    :params: tweet: JSON representation of the tweet.
    '''
    if tweet.get('retweeted_status') == None:
        return False
    else:
        return True


def ongRT(tw_engine, ong_list):
    '''
    RT tweets for listed ONGs & OGs. Receives a list of Orgs. and checks for the 20 most recent tweets.

    :params: tw_engine: Authenticated Twitter API
    :params: ong_list: list of ongs screen name.
    '''

    for ong in ong_list:
        ong_timeline = tw_engine.user_timeline(ong)

        for tweet in ong_timeline:
            tweet = tweet._json
            
            if not (tweet['in_reply_to_status_id'] != None or tweet['is_quote_status']):
                if not isRetweet(tweet):
                    try:
                        if not wasBotRetweeted(tweet):
                            tw_engine.retweet(tweet['id'])
                            print(f"RT Tweet ID ONG-OG: {tweet['id']}")
                            if not wasBotFavorited(tweet):
                                tw_engine.create_favorite(tweet['id'])
                                print(f"Fav Tweet ID ONG-OG: {tweet['id']}")
                    except Exception as e:
                        print(f"An exception occurred while trying to RT replied Tweet ID {tweet['id']}: {e}")
            
            time.sleep(1)


def mentionsRT(tw_engine, mention):
    '''
    Search for mentions in @DonarSangreBOT timeline (last 20 as per Tweepy doc) to RT. 
    Search for mentions in replies, tweets and quotes.

    :params: tw_engine: Twitter API authenticated.
    :params: mention: A tweet where @DonarSangreBOT was mentioned. Could be a reply, a tweet or a quote.
    '''

    mention = mention._json

    if mention['in_reply_to_status_id'] != None: # @DonarSangreBOT es mencionado en una respuesta a un tweet
        original_tweet_id = mention['in_reply_to_status_id']
        try:
            original_tweet = tw_engine.get_status(original_tweet_id)._json
            if not wasBotRetweeted(original_tweet):
                tw_engine.retweet(original_tweet_id)
                print(f"RT Tweet ID Reply: {original_tweet_id}")
                if not wasBotFavorited(original_tweet):
                    tw_engine.create_favorite(original_tweet_id)
                    print(f"Fav Tweet ID Reply: {original_tweet_id}")
        except Exception as e:
            print(f"An exception occurred while trying to RT replied Tweet ID {mention['in_reply_to_status_id']}: {e}")
    
    elif mention['is_quote_status']: # @DonarSangreBOT es mencionado citando un tweet
        quoted_tweet_id = mention['is_quote_status']

        try:
            quoted_tweet = tw_engine.get_status(quoted_tweet_id)._json
            if not wasBotRetweeted(quoted_tweet):
                tw_engine.retweet(quoted_tweet_id)
                print(f"RT Tweet ID Quote: {quoted_tweet_id}")
                if not wasBotFavorited(quoted_tweet_id):
                    tw_engine.create_favorite(quoted_tweet_id)
                    print(f"Fav Tweet ID Quote: {quoted_tweet_id}")
        except Exception as e:
            print(f"An exception occurred while trying to RT quoted Tweet ID {mention['is_quote_status']}: {e}")

    else: # @DonarSangreBOT es mencionado en un tweet.
        try:
            if not wasBotRetweeted(mention):
                tw_engine.retweet(mention['id'])
                print(f"RT Tweet ID Mention: {mention['id']}")
                if not wasBotFavorited(mention):
                    tw_engine.create_favorite(mention['id'])
                    print(f"Fav Tweet ID Mention: {mention['id']}")
        except Exception as e:
            print(f"An exception occurred while trying to RT mention Tweet ID {mention['id']}: {e}")

    time.sleep(1)


def searchRT(tw_engine, phrase):
    '''
    Search for related tweets on the matter.

    :params: tw_engine: Twitter API authenticated.
    :params: phrase: 
    '''
    #rt buscando keywords
    results = tw_engine.search(phrase, result_type='mixed', count=40)

    for result in results:
        id_status = post_processing(result)
        
        if id_status:
            search_status = tw_engine.get_status(id_status)._json
            if not wasBotRetweeted(search_status):
                tw_engine.retweet(id_status)
                print(search_status)
                print(f"RT Tweet ID Search: {id_status}")
                if not wasBotFavorited(search_status):
                    tw_engine.create_favorite(id_status)
                    print(f"Fav Tweet ID Search: {id_status}")

        time.sleep(1)
