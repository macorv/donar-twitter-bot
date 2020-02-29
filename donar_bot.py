import config
import time
from bot_tools import post_processing

tw = config.create_api()

mentions = tw.mentions_timeline()

for mention in mentions:
    if mention._json['in_reply_to_status_id']:
        try:
            new_status = tw.get_status(mention._json['in_reply_to_status_id'])
            if new_status._json['retweeted']:
                print(f"Already RT ID {new_status._json['id']}")
                continue
            else:
                tw.retweet(mention._json['in_reply_to_status_id'])
        except Exception as e:
            print(e)
    elif mention._json['is_quote_status']:
        try:
            quoted_status = tw.get_status(mention._json['quoted_status']['id'])
            if quoted_status._json['retweeted']:
                print(f"Already RT {quoted_status._json['id']}")
                continue
            else:
                tw.retweet(quoted_status._json['id'])
        except Exception as e:
            print(e)
    else:
        if mention._json['retweeted']:
            print(f"Already RT {mention._json['id']}")
            continue
        else:
            tw.retweet(mention._json['id'])

time.sleep(60)

#rt buscando keywords
results = tw.search('dadores de sangre', result_type='mixed', count=40)

for result in results:
    match_status, id_status = post_processing(result)
    if match_status:
        search_status = tw.get_status(id_status)._json
        if search_status['retweeted']:
            print(f'Already RT: {id_status}')
        else:
            tw.retweet(id_status)
            print(f'RT ID {id_status}')
    else:
        print(f"Tweet ID {id_status} didn't match regexp criteria")
    time.sleep(8)

time.sleep(60 * 2)
