""" Bot do publikowania informacji z kalendarium XVI wieku na Twitterze """
import requests
import tweepy
import os
import sys
from datetime import date


CONSUMER_KEY = os.environ.get("CONSUMER_KEY")
CONSUMER_SECRET = os.environ.get("CONSUMER_SECRET")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")
XVI_API = "http://localhost:8080/api/short"


def get_fact():
    """ funkcja pobiera wydarzenie przez API serwisu XVI wiek """
    fact = requests.get(XVI_API).json()
    return fact["content"]


# ------------------------------------------------------------------------------   
if __name__ == '__main__':
    
    home_path = os.path.expanduser('~')
    log_file_path = home_path + "/.xvi-wiek-bot/xvi-wiek-bot.log"
    err_file_path = home_path + "/.xvi-wiek-bot/bot_errrors.log"
    
    with open(log_file_path, 'r', encoding='utf-8') as f:
        log_date = f.read().strip()
        
    today = str(date.today())
    
    if log_date == today:
        print('Dziś już opublikowano tweeta.')
        sys.exit(1)
            
    try:    
        client = tweepy.Client(
            consumer_key=CONSUMER_KEY,
            consumer_secret=CONSUMER_SECRET,
            access_token=ACCESS_TOKEN,
            access_token_secret=ACCESS_TOKEN_SECRET
        )
    except tweepy.TweepError as e:
       with open(err_file_path, 'a', encoding='utf-8') as f:
           f.write(e.message + '\n')
    
    # wydarzenie z serwisu xvi-wiek
    text = get_fact()
    
    try:    
        response = client.create_tweet(text=text)
    except tweepy.TweepError as e:
       with open(err_file_path, 'a', encoding='utf-8') as f:
           f.write(e.message + '\n')
    
    with open(log_file_path, 'w', encoding='utf-8') as f:
        f.write(today)

