import config
import time

time.sleep(60 * 5)

tw = config.create_api()

mentions = tw.mentions_timeline()

for mention in mentions:
    if mention._json['in_reply_to_status_id']:
        new_status = tw.get_status(mention._json['in_reply_to_status_id'])
        if new_status._json['retweeted']:
            print('Already RT')
            continue
        tw.retweet(mention._json['in_reply_to_status_id'])
    elif mention._json['is_quote_status']:
        quoted_status = tw.get_status(mention._json['quoted_status']['id'])
        if quoted_status._json['retweeted']:
            print('Already RT')
            continue
        tw.retweet(quoted_status._json['id'])
    else:
        if mention._json['retweeted']:
            print('Already RT')
            continue
        tw.retweet(mention._json['id'])
