from authentication import Auth


def login_api(request):
    # get information from body
    body = request.body
    username = eval(body)['username']
    password = eval(body)['password']
    auth = Auth(request, username, password)
    result = auth.post()
    # if result['detail'].upper().strip() is 'Signature has expired.'.upper().strip():
    #     pass
    return result
