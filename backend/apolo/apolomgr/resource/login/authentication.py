import requests
import simplejson as json
from django.contrib import auth
from django.http import HttpResponse
from django.utils.translation import gettext
from rest_framework_jwt.settings import api_settings
from backend.apolo.tools import constants
from datetime import datetime, timedelta
from calendar import timegm
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools.exception import exception_handler

import logging
from logging import Formatter
from logging.handlers import TimedRotatingFileHandler
from backend.apolo.tools import views_helper

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
formatter = Formatter(
    fmt='%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(filename)s - %(threadName)s - %(funcName)s - %(message)s',
    datefmt='%Y/%m/%d %p %I:%M:%S')
file_handler = TimedRotatingFileHandler(constants.LOG_PATH, when="D", interval=1, backupCount=5)
file_handler.level = logging.INFO
file_handler.formatter = formatter
logger.addHandler(file_handler)

payloader = api_settings.JWT_PAYLOAD_HANDLER
encoder = api_settings.JWT_ENCODE_HANDLER
decoder = api_settings.JWT_DECODE_HANDLER


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
        try:
            body = self.request.body
            username = eval(body)[constants.USERNAME]
            password = eval(body)[constants.PASSWORD]
            if not username or not password:
                logger.info(constants.NO_USERNAME_OR_PASSWORD_FONUD_ERROR % (username, password))  ###Logger###
                return api_return(
                    data={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.NO_USERNAME_OR_PASSWORD})
            user_obj = auth.authenticate(username=username, password=password)
            if not user_obj:
                logger.info(constants.LOGIN_FAILED_ERROR % (username, password))  ###Logger###
                return api_return(
                    data={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.USER_AND_PASSWD_INCORRECT})
            elif not user_obj.is_active:
                logger.info(constants.USERNAME_INACTIVE_ERROR % username)  ###Logger###
                return api_return(
                    data={constants.STATUS: constants.FALSE, constants.MESSAGE: constants.USER_DISABLED})
            else:
                logger.info(constants.LOGIN_SUCCESSFUL % (username, password))  ###Logger###
                auth.login(self.request, user_obj)
                if user_obj.is_superuser:
                    role = constants.SUPERUSER
                elif user_obj.is_staff:
                    role = constants.ADMIN
                else:
                    role = constants.STAFF
                token = encoder(payloader(user_obj))
                data = {
                    constants.USERNAME: username,
                    constants.ROLE: role,
                    constants.TOKEN: token,
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.SUCCESS
                }
                self.request.session['TOKEN_IN_SESSION'] = token
                # return api_return(data=eval(json.dumps(data)))
                return api_return(data=data)
        except Exception, e:
            return exception_handler(e)

    def delete(self):
        self.request.session.clear()
        # print self.request.session.keys()
        # print self.request.session.get('TOKEN_IN_SESSION')


class TokenRefresh(object):
    def __init__(self, token):
        self.token = token
        self.time_diff = timedelta(seconds=constants.TIMEDELTA)

    def refresh_token(self):
        try:
            payload = decoder(self.token)
        except Exception, e:
            print e.message
            return False
        orig_iat = payload.get('orig_iat')
        if orig_iat:
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA
            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 + refresh_limit.seconds)
            refresh_timestamp = orig_iat + float(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())
            if now_timestamp > refresh_timestamp:
                data = {
                    constants.MESSAGE: constants.REFRESH_EXPIRED
                }
                logger.info(constants.REFRESH_EXPIRED)
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
                        constants.TOKEN: new_token,
                        constants.STATUS: constants.REFRESH_CODE
                    }
                    print "new token:{}".format(new_token)
                else:
                    data = {
                        constants.TOKEN: self.token,
                        constants.STATUS: constants.NO_REFRESH_CODE
                    }
        else:
            data = {
                constants.MESSAGE: gettext(constants.ORIG_IAT_REQUIRED)
            }
            logger.info(constants.ORIG_IAT_REQUIRED)
        return eval(json.dumps(data))


def auth_if_refresh_required(view):
    def decorator(request, *args, **kwargs):
        # this token is from header
        new_token = views_helper.get_request_value(request, "HTTP_AUTHORIZATION", 'META')
        # this token is from session, for jqgrid
        token = request.session.get('TOKEN_IN_SESSION')
        if new_token is not '':
            token = request.META.get("HTTP_AUTHORIZATION").split()[1]
        refresh_token = TokenRefresh(token).refresh_token()
        if refresh_token is False:
            return HttpResponse(
                json.dumps({'detail': 'Signature has expired.', 'code': constants.TOKEN_ALREADY_EXPIRED_CODE}))
        if refresh_token[constants.STATUS] == constants.REFRESH_CODE:
            request.session['TOKEN_IN_SESSION'] = refresh_token[constants.TOKEN]
        try:
            if refresh_token:
                request.META[constants.NEW_TOKEN] = refresh_token
                return view(request, *args, **kwargs)
        except ValueError:
            pass

    return decorator
