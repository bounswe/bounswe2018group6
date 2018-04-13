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


def process_followings(request, screen_name):
    api = twitter_auth()
    # Obtain queries from the request and check if user queried a count parameter.
    queries = request.GET.dict()
    count = int(queries['count']) if 'count' in queries else 20;
    # List that stores all User's found as json objects.
    friends = []

    c = tweepy.Cursor(api.friends,
                      screen_name=screen_name,
                      include_user_entities=False).items(count)
    while True:
        try:
            friend = c.next()
            friends.append(friend._json)
        except tweepy.TweepError:
            response = {
                'error':'Twitter rate limit exceeded, please try again 15 minutes later.',
                'followings':friends
            }
            return response
        except StopIteration:
            break

    response = {
        'error':'',
        'followings':friends
    }
    return response


def followings_api(request, screen_name):
    response = process_followings(request, screen_name)
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii':False, 'indent':4})


def followings(request, screen_name):
    response = process_followings(request, screen_name)
    context = {
        'user':screen_name,
        'error':response['error'],
        'followings':response['followings']
    }
    return render(request, 'twitterapiapp/followings_page.html', context)
