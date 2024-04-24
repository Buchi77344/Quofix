from django.utils.crypto import get_random_string
def get(request):
    token =get_random_string(length=45)
    request.session['auth_token'] = token
    print("token:",token)
    return get

