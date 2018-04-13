from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import tweepy

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

def main_page(request):
    '''Main page handler'''
    return render(request, 'twitterapiapp/main_page.html')

def find_users(request, search_name):
    context = {} # dictionary to be sent to template page in order to show it on frontend
    if proc_find_user_api(search_name):
        context['Tweets'] = proc_find_user_api(search_name)    
    return render(request, 'twitterapiapp/find_users.html', context) # rendered with html file and context dictionary
    #return HttpResponse("The user_is requested is %s." % user_id) # pure HTTP response


def find_users_api(request, search_name):
    # get the resulting dict.
    response_data = proc_find_user_api(search_name)
    # dict object will automatically converted to a application/json http response.
    return JsonResponse(response_data)


def proc_find_user_api(search_name):
    '''Takes search query, finds best 5 accounts for that search and returns
    last tweet of that 5 accounts.'''
    api = twitter_auth()
    search = tweepy.Cursor(api.search_users, q=search_name).items() 
    response_dict = {}
    tweet_limit = 5
    # Name of output JSON file
    users = []
    counter = 0
    while True:
        try:
            result = next(search)
            users.append(result)
            counter += 1
            if counter > tweet_limit:
                break
            if users:
                for i, user in enumerate(users):
                        temp = user._json['status']['text']
                        response_dict.update({'Tweet'+str(i):temp})
        except:
            return {}
    return response_dict