from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import tweepy

def twitter_auth():
    '''Authenticates user and returns api object. It's called from each method.'''

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


def find_friends(request, user_id):
    context = {}
    if proc_find_friends_api(user_id):
        context['Friend'] = proc_find_friends_api(user_id)
    return render(request, 'twitterapiapp/friends.html', context)


def find_friends_api(request, user_id):

    response_data = proc_find_friends_api(user_id)

    return JsonResponse(response_data)


def proc_find_friends_api(user_id):
    api = twitter_auth()
    search = tweepy.Cursor(api.friends, q=user_id).items()
    response_dict = {}
    friend_limit = 20
    friends = []
    counter = 0
    while True:
        try:
            result = next(search)
            friends.append(result)
            counter += 1
            if counter > friend_limit:
                break
            if friends:
                for i, friend in enumerate(friends):
                        temp = friend.json['status']['text']
                        response_dict.update({'Friend'+str(i):temp})
        except:
            return {}
    return response_dict

# TODO
# Add two methods that were specified in urls.py for your paths.
# Firstly, call twitter_auth() in both of your methods and then
# For the first method, do your work and return JSON for the API,
# For the second method, do your work and return HTML response for the frontend.
