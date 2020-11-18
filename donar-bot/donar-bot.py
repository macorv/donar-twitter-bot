import configparser
import time
import botkit

config = configparser.ConfigParser()
config.read('config.ini')

print('---AUTHENTICATION---') # future logger
try:
    tw = botkit.authAPI()
    print('Authenticated') # future logger
except Exception as e:
    print(f"An error occurred while Authenticating in Twitter API: {e}") # future logger

print('---MENTIONS---') # future logger
bot_mentions = tw.mentions_timeline()

for mention in bot_mentions:
    botkit.mentionsRT(tw, mention)

time.sleep(30)

print('---SEARCH---') # future logger
botkit.searchRT(tw, 'dadores de sangre')

time.sleep(30)

print('---ONG/OG---') # future logger
ong_list = config['ONG']['names'].split('|')
botkit.ongRT(tw, ong_list)

time.sleep(30)

print('---FINISH---') # future logger

