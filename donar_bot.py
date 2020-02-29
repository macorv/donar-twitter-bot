import config
import time
from bot_tools import post_processing

time.sleep(60 * 3)

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

time.sleep(60)

# rt buscando keywords
results = tw.search('dadores de sangre', result_type='mixed', count=40)

for result in results:
    match_status, id_status = post_processing(result)
    if match_status:
        search_status = tw.get_status(id_status)._json
        if search_status['retweeted']:
            pass
        else:
            tw.retweet(id_status)
    else:
        pass
    time.sleep(8)
