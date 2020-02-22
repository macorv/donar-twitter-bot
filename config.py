from dotenv import load_dotenv
import os
import tweepy

load_dotenv()

def create_api():
    API_KEY = os.getenv('API_KEY')
    API_SECRET_KEY = os.getenv('API_SECRET_KEY')
    ACCESS_TOKEN =  os.getenv('ACCESS_TOKEN')
    ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

    AUTH = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    AUTH.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    api = tweepy.API(AUTH, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    try:
        api.verify_credentials()
    except Exception as e:
        raise e

    return api
