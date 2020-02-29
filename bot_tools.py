import re

def post_processing(raw_tweet):
    tweet = raw_tweet._json
    match = re.search('(necesit(amos|a|an|o) (\d*)|necesit(amos|a|an|o)|buscando) (dadores) (de) (sangre)', tweet['text'])
    if match:
        try:
            id = tweet['retweeted_status']['id']
            return True, id
        except KeyError:
            id = tweet['id']
            return True, id
    return False, tweet['id']
