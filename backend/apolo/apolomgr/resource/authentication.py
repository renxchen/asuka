import requests
from django.http import HttpResponse, response
import simplejson as json
from django.contrib import auth
from django.utils.translation import gettext
from rest_framework_jwt.settings import api_settings
from backend.apolo.tools import constants
from rest_framework import permissions
from datetime import datetime, timedelta
from calendar import timegm

payloader = api_settings.JWT_PAYLOAD_HANDLER
encoder = api_settings.JWT_ENCODE_HANDLER
decoder = api_settings.JWT_DECODE_HANDLER


class IsAuthenticated(permissions.BasePermission):
    """
    Allows access only to authenticated users.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated()


class ResponseError(Exception):
    pass


class token_mgr(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def is_success(self, status_code):
        if 200 <= status_code <= 299:
            return True
        return False

    def obtain_token(self):
        req_body = {'username': self.username, 'password': self.password}
        url = "http://%s:%s/api-token-auth/" % ('127.0.0.1', '1111')
        headers = {'content-type': 'application/json'}
        resp = requests.post(url=url, data=json.dumps(req_body), headers=headers)
        if self.is_success(resp.status_code):
            resp_body = json.loads(resp.text)
            token = resp_body.get('token')
        else:
            return HttpResponse(resp)
            # e = resp.status_code
            # raise ResponseError(e)
        return token

    def verify_token(self, token):
        url = "http://%s:%s/api-token-verify/" % ('127.0.0.1', '1111')
        req_body = {'token': token}
        headers = {'content-type': 'application/json'}
        resp = requests.post(url=url, data=json.dumps(req_body), headers=headers)
        if self.is_success(resp.status_code):
            resp_body = json.loads(resp.text)
            token = resp_body.get('token')
        else:
            return HttpResponse(resp)
        return token

    def verify_token_test(self, request):
        url = "http://%s:%s/api-token-verify/" % ('127.0.0.1', '1111')
        req_body = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZW1haWwiOiJraW1saUBjaXNjby5jb20iLCJleHAiOjE1MTE1MjI3NDB9.4QUcFO8XNBLWzWjSJSnQGKW4afiTJseEwma6mGs7Vyw"}
        headers = {'content-type': 'application/json'}
        resp = requests.post(url=url, data=json.dumps(req_body), headers=headers)
        if self.is_success(resp.status_code):
            resp_body = json.loads(resp.text)
            token = resp_body.get('token')
        else:
            return HttpResponse(resp)
            # e = resp.status_code
            # raise ResponseError(e)
        return HttpResponse(resp)

    def refresh_token(self, request):
        url = "http://%s:%s/api-token-refresh/" % ('127.0.0.1', '1111')
        req_body = {
            "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6ImFkbWluIiwidXNlcl9pZCI6MSwiZW1haWwiOiJraW1saUBjaXNjby5jb20iLCJleHAiOjE1MTE3ODc5MzZ9.GMtBdZk0Ui4BXdVUsvkyKgUWZIh3IrTo668cuxvAjHQ"}
        headers = {'content-type': 'application/json'}
        resp = requests.post(url=url, data=json.dumps(req_body), headers=headers)
        if self.is_success(resp.status_code):
            resp_body = json.loads(resp.text)
            token = resp_body.get('token')
        else:
            return HttpResponse(resp)
            # e = resp.status_code
            # raise ResponseError(e)
        return HttpResponse(resp)


class Auth(object):
    def __init__(self, request):
        self.request = request

    def post(self):
        body = self.request.body
        username = eval(body)['username']
        password = eval(body)['password']
        if not username or not password:
            return HttpResponse({'message': constants.NO_USERNAME_OR_PASSWORD})
        user_obj = auth.authenticate(username=username, password=password)
        if not user_obj:
            data = {'message': constants.USER_AND_PASSWD_INCORRECT}
            return HttpResponse(json.dumps(data))
        elif not user_obj.is_active:
            data = {'message': constants.USER_DISABLED}
            return HttpResponse(json.dumps(data))
        else:
            auth.login(self.request, user_obj)
            if user_obj.is_superuser:
                role = 'superuser'
            elif user_obj.is_staff:
                role = 'admin'
            else:
                role = 'staff'
            token = encoder(payloader(user_obj))
            data = {
                "username": username,
                "role": role,
                "token": token
            }
            return HttpResponse(json.dumps(data))


class TokenRefresh(object):
    def __init__(self, token):
        self.token = token
        self.time_diff = timedelta(seconds=120)

    def refresh_token(self):
        payload = decoder(self.token)
        orig_iat = payload.get('orig_iat')
        if orig_iat:
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA
            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 + refresh_limit.seconds)
            refresh_timestamp = orig_iat + float(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())
            if now_timestamp > refresh_timestamp:
                data = {
                    'msg': gettext('Refresh has expired.')
                }
            else:
                new_orig_iat = now_timestamp
                exp_limit = api_settings.JWT_EXPIRATION_DELTA
                if isinstance(exp_limit, timedelta):
                    exp_limit = (exp_limit.days * 24 * 3600 + exp_limit.seconds)
                expiration_timestamp = orig_iat + int(exp_limit)
                if expiration_timestamp - new_orig_iat <= self.time_diff.seconds:
                    new_exp = new_orig_iat + int(exp_limit)
                    payload['orig_iat'] = new_orig_iat
                    payload['exp'] = new_exp
                    new_token = encoder(payload)
                    data = {
                        "token": new_token,
                        "status": 101
                    }
                    print "new token:{}".format(new_token)
                else:
                    data = {
                        "token": self.token,
                        "status": 100
                    }
        else:
            data = {
                'msg': gettext('orig_iat field is required.')
            }
        return eval(json.dumps(data))


def auth_if_refresh_required(view):
    def decorator(request, *args, **kwargs):
        token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        refresh_token = TokenRefresh(token).refresh_token()
        try:
            if refresh_token:
                request.META["NEW_TOKEN"] = refresh_token
                return view(request, *args, **kwargs)
        except ValueError:
            pass

    return decorator
