from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import tweepy
import time

def twitter_auth():
    '''Authenticates user and returns api object. It's called from each method.'''
    tokens = open('twitter_key.txt')

    # Assumes you have a file with name twitter_key.txt
    # in this directory which stores tokens in this order
    with open('twitter_key.txt') as f_in:
        consumer_key = f_in.readline().rstrip('\n')
        consumer_secret = f_in.readline().rstrip('\n')
        access_token = f_in.readline().rstrip('\n')
        access_token_secret = f_in.readline().rstrip('\n')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,
                     retry_count=0,
                     retry_delay=10,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit_notify=True)

    return api

def main_page(request):
    return render(request, 'twitterapiapp/main_page.html')
    return

def retweet(request, username):
    # dictionary to be sent to template page in order to show it on frontend
    context = process_retweet_api(username)
    # rendered with html file and context dictionary
    return render(request, 'twitterapiapp/simple_page.html', context)


def retweet_api(request, username):
    # Get the resulting json property of the Status object.
    response_data = process_retweet_api(username)
    return JsonResponse(response_data)



def process_retweet_api(username):
    # Takes username, process the data and returns a dictionary object containing the api response content.
    api = twitter_auth()
    dicts = {}
    # Check if user is found or not.
    try:
        a = api.get_user(username)
    except Exception:
        print("no user!")
        dicts['Retweet'] = "No user is found with this user name."
        return dicts

    list_of_status = []
    # Collect user's status whose name is username and store them into list_of_status. 
    for status in api.user_timeline(screen_name = username, count=100, include_rts=False):
        list_of_status.append(status.id)
    # Handle the empty status situation.
    if len(list_of_status) == 0:
        print("There is no tweet to retweet.")
    # Retweet the user's the last tweet.
    retweet_status = api.get_status(list_of_status[0])._json
    if retweet_status["retweeted"] == False:
        retweet = api.retweet(list_of_status[0])
        retweet_text = retweet._json['text']
    else:
        retweet_text = "You have already retweeted this Tweet."
        
    dicts['Retweet'] = retweet_text
    return dicts