import requests
import simplejson as json
from django.contrib import auth
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings
from backend.apolo.tools import constants
from datetime import datetime, timedelta
from calendar import timegm
from backend.apolo.tools.views_helper import api_return
from backend.apolo.tools.exception import exception_handler

import logging
from backend.apolo.tools import views_helper
import traceback

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger(__name__)
# formatter = Formatter(
#     fmt='%(asctime)s - %(name)s - %(levelname)s - %(thread)d - %(filename)s - %(threadName)s - %(funcName)s - %(message)s',
#     datefmt='%Y/%m/%d %p %I:%M:%S')
# script_dir = os.path.split(os.path.realpath(__file__))[0]
# log_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))),
#                         constants.LOG_PATH)
# file_handler = TimedRotatingFileHandler(log_path, when="D", interval=1, backupCount=5)
# file_handler.level = logging.INFO
# file_handler.formatter = formatter
# logger.addHandler(file_handler)

payloader = api_settings.JWT_PAYLOAD_HANDLER
encoder = api_settings.JWT_ENCODE_HANDLER
decoder = api_settings.JWT_DECODE_HANDLER


class TokenMgrAPI(object):
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
        self.username = views_helper.get_request_value(self.request, constants.USERNAME, 'BODY')
        self.password = views_helper.get_request_value(self.request, constants.PASSWORD, 'BODY')
        self.logger = logging.getLogger("apolo.log")

    def post(self):
        try:
            if not self.username or not self.password:
                self.logger.info(constants.NO_USERNAME_OR_PASSWORD_FONUD_ERROR)  ###Logger###
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.NO_USERNAME_OR_PASSWORD
                    }
                }
                return api_return(data=data)
            user_obj = auth.authenticate(username=self.username, password=self.password)
            if not user_obj:
                self.logger.info(constants.LOGIN_FAILED_ERROR)  ###Logger###
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.USER_AND_PASSWD_INCORRECT
                    }
                }
                return api_return(data=data)
            elif not user_obj.is_active:
                self.logger.info(constants.USERNAME_INACTIVE_ERROR)  ###Logger###
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.USER_DISABLED
                    }
                }
                return api_return(data=data)
            else:
                self.logger.info(constants.LOGIN_SUCCESSFUL)  ###Logger###
                auth.login(self.request, user_obj)
                if user_obj.is_superuser:
                    role = constants.SUPERUSER
                elif user_obj.is_staff:
                    role = constants.ADMIN
                else:
                    role = constants.STAFF
                token = encoder(payloader(user_obj))
                data = {
                    'data': {
                        constants.USERNAME: self.username,
                        constants.ROLE: role,
                    },
                    'new_token': token,
                    constants.STATUS: {
                        constants.STATUS: constants.TRUE,
                        constants.MESSAGE: constants.SUCCESS
                    }
                }
                # self.request.session['TOKEN_IN_SESSION'] = token
                self.request.session['_username'] = self.username
                self.request.session[self.username + '_token'] = token
                # return api_return(data=eval(json.dumps(data)))
                return api_return(data=data)
        except Exception, e:
            return exception_handler(e)

    def delete(self):
        # self.request.session[self.username] = None
        # if self.request.session[self.username] is None:
        #     data = {
        #         constants.STATUS: {
        #             'status': 'True',
        #             'message': 'Logout Success.',
        #             'username': self.username
        #         }
        #     }
        #     return api_return(data=data)
        # else:
        #     data = {
        #         constants.STATUS: {
        #             'status': 'False',
        #             'message': 'Logout Success.',
        #             'username': self.username
        #         }
        #     }
        #     return api_return(data=data)
        try:
            self.request.session.clear()
            data = {
                constants.USERNAME: self.username,
                constants.STATUS: {
                    constants.STATUS: constants.TRUE,
                    constants.MESSAGE: constants.USER_LOGOUT_SUCCESSFUL
                }
            }
            return api_return(data=data)
            # print self.request.session.keys()
            # print self.request.session.get('TOKEN_IN_SESSION')
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)


class TokenRefresh(object):
    def __init__(self, token):
        self.token = token
        self.time_diff = timedelta(seconds=constants.TOKEN_TIMEDELTA)
        self.logger = logging.getLogger("apolo.log")

    def refresh_token(self):
        try:
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
                        constants.STATUS: {
                            constants.STATUS: constants.FALSE,
                            constants.MESSAGE: constants.REFRESH_EXPIRED
                        }
                    }
                    self.logger.info(constants.REFRESH_EXPIRED)
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
                            'new_token': new_token,
                            constants.CODE: constants.REFRESH_CODE
                        }
                        print "new token:{}".format(new_token)
                    else:
                        data = {
                            'new_token': self.token,
                            constants.CODE: constants.NO_REFRESH_CODE
                        }
            else:
                data = {
                    constants.STATUS: {
                        constants.STATUS: constants.FALSE,
                        constants.MESSAGE: constants.SYSTEM_ERROR
                    }
                }
                self.logger.info(constants.ORIG_IAT_REQUIRED)
            return eval(json.dumps(data))
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)


def auth_if_refresh_required(view):
    def decorator(request, *args, **kwargs):
        try:
            # username = views_helper.get_request_value(request, 'username', 'GET')
            username = request.session.get('_username')
            if username is None:
                data = {
                    constants.STATUS: {
                        constants.CODE: constants.TOKEN_NOT_EXIST_FOR_CURRENT_USER_CODE,
                        constants.MESSAGE: constants.NO_USERNAME_OR_PASSWORD_FONUD_ERROR,
                        constants.STATUS: constants.FALSE
                    }
                }
                return HttpResponse(json.dumps(data))
            # token = request.session[username + '_token']
            # this token is from header
            new_token = views_helper.get_request_value(request, "HTTP_AUTHORIZATION", 'META')
            # this token is from session, for jqgrid
            token = request.session.get(username + '_token')
            if token is None:
                data = {
                    constants.STATUS: {
                        constants.CODE: constants.TOKEN_NOT_EXIST_FOR_CURRENT_USER_CODE,
                        constants.MESSAGE: constants.TOKEN_NOT_EXIST_FOR_CURRENT_USER_MSG
                    }
                }
                return HttpResponse(json.dumps(data))
            if new_token is not '':
                token = request.META.get("HTTP_AUTHORIZATION").split()[1]
            refresh_token = TokenRefresh(token).refresh_token()
            if refresh_token is False:
                data = {
                    constants.STATUS: {
                        constants.MESSAGE: constants.TOKEN_EXPIRED_MSG,
                        constants.CODE: constants.TOKEN_ALREADY_EXPIRED_CODE,
                        constants.STATUS: constants.FALSE
                    }
                }
                return HttpResponse(json.dumps(data))
            if refresh_token[constants.CODE] == constants.REFRESH_CODE:
                request.session[username] = refresh_token[constants.TOKEN]
            if refresh_token:
                request.META[constants.NEW_TOKEN] = refresh_token
                return view(request, *args, **kwargs)
        except Exception, e:
            if constants.DEBUG_FLAG:
                print traceback.format_exc(e)
            return exception_handler(e)

    return decorator
