from django.http import HttpResponse, JsonResponse


def timegraph(request, user_id):
    return return HttpResponse("The user_is requested is %s." % user_id)


def timegraph_api(request, user_id):
    # get the resulting dict.
    response_data = proc_twitter_api(user_id)
    # dict object will automatically converted to a application/json http response.
    return JsonResponse(response_data)


def proc_twitter_api(user_id):
    '''Takes user_id, process the data and returns a dictionary object containing the api response content.'''
    return {}