from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
import json
import tweepy


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


def trends_by_place_api(request, WOEID):
    api = twitter_auth()
    print("trends_by_place api authenticaion is successful")
    try:
        response = api.trends_place(WOEID)
        print("trends_by_place api call is successful")
    except:
        response = {'Error': 'Invalid WOEID'}
    return JsonResponse(response, safe=False)


def trends_by_place(request, WOEID):
    api = twitter_auth()
    print("trends_by_place api authenticaion is successful")
    try:
        response = api.trends_place(WOEID)
        print("trends_by_place api call is successful")
        context = {'error': False,'trends': response[0]['trends'], 'locations': response[0]['locations'], 'as_of': response[0]['as_of']}
    except:
        context = {'error': True, 'error_text': 'Invalid WOEID'}
    return render(request, 'twitterapiapp/trends_place.html', context)


def find_users(request, search_name):
    context = {}  # dictionary to be sent to template page in order to show it on frontend
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
                    response_dict.update({'Tweet' + str(i): temp})
        except:
            return {}
    return response_dict


def retweet(request, username):
    # dictionary to be sent to template page in order to show it on frontend
    context = process_retweet_api(username)
    # rendered with html file and context dictionary
    return render(request, 'twitterapiapp/retweet.html', context)


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
                'error': 'Twitter rate limit exceeded, please try again 15 minutes later.',
                'followings': friends
            }
            return response
        except StopIteration:
            break

    response = {
        'error': '',
        'followings': friends
    }
    return response


def followings_api(request, screen_name):
    response = process_followings(request, screen_name)
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def followings(request, screen_name):
    response = process_followings(request, screen_name)
    context = {
        'user': screen_name,
        'error': response['error'],
        'followings': response['followings']
    }
    return render(request, 'twitterapiapp/followings_page.html', context)


def recent_favorites(request, screen_name):
    context = proc_recent_favorites(request, screen_name)
    return render(request, 'twitterapiapp/recent_favorites.html', context)


def recent_favorites_api(request, screen_name):
    response = proc_recent_favorites(request, screen_name)
    return JsonResponse(response, safe=False, json_dumps_params={'ensure_ascii': False, 'indent': 4})


def proc_recent_favorites(request, screen_name):
    api = twitter_auth()
    tweet_count, retweet_count = 0, 0

    # print out each favorited tweet
    for page in tweepy.Cursor(api.favorites, id=screen_name, wait_on_rate_limit=True, count=200).pages(200):
        for status in page:
            tweet_count, retweet_count = tweet_count+1, retweet_count + status.retweet_count

    return {'tweet_count': tweet_count, 'retweet_count': retweet_count, 'retweet_average': retweet_count/tweet_count}

def find_followers(request, follower):
    context = {}
    if proc_find_followers_api(follower):
        context['Followers'] = proc_find_followers_api(follower)
    return render(request, 'twitterapiapp/follower.html', context)  # rendered with html file and context dictionary


def find_followers_api(request, follower):
    # get the resulting dict.
    response_data = proc_find_followers_api(follower)
    # dict object will automatically converted to a application/json http response.
    return JsonResponse(request, response_data)


def proc_find_followers_api(follower):
    api = twitter_auth()
    search = tweepy.Cursor(api.followers, id=follower).items()
    response_dict = {}
    follower_limit = 10

    followers = []
    counter = 0
    while True:
        try:
            result = next(search)
            followers.append(result)
            counter += 1
            if counter > follower_limit:
                break
            if followers:
                for i, follower in enumerate(followers):
                    temp = follower.screen_name
                    response_dict.update({'Tweet' + str(i): temp})
        except:
            return {}

    return response_dict
