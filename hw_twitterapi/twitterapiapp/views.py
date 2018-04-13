from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import tweepy
import time

def twitter_auth():
    '''Authenticates user and returns api object. It's called from each method.'''
    tokens_file = 'twitter_key.txt'

    # Assumes you have a file with name twitter_key.txt
    # in this directory which stores tokens in this order
    with open(tokens_file) as f_in:
        consumer_key = f_in.readline().rstrip('\n')
        consumer_secret = f_in.readline().rstrip('\n')
        access_token = f_in.readline().rstrip('\n')
        access_token_secret = f_in.readline().rstrip('\n')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,
                     retry_count=5,
                     retry_delay=10,
                     retry_errors=set([401, 404, 500, 503]),
                     wait_on_rate_limit_notify=True)

    return api


def timegraph(request, user_id):
    context = {} # dictionary to be sent to template page in order to show it on frontend
    return render(request, 'twitterapiapp/simple_page.html', context) # rendered with html file and context dictionary
    #return HttpResponse("The user_is requested is %s." % user_id) # pure HTTP response


def timegraph_api(request, user_id):
    # get the resulting dict.
    response_data = proc_twitter_api(user_id)
    # dict object will automatically converted to a application/json http response.
    return JsonResponse(response_data)


def proc_twitter_api(user_id):
    '''Takes user_id, process the data and returns a dictionary object containing the api response content.'''
    return {}

# TODO
# Add two methods that were specified in urls.py for your paths.
# Firstly, call twitter_auth() in both of your methods and then
# For the first method, do your work and return JSON for the API,
# For the second method, do your work and return HTML response for the frontend.