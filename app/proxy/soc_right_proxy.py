#-*- encoding: utf-8 -*-

from tornado.escape import url_escape   

from helper import http_helper, str_helper
import config

def _format_url(url, params):
    if '?' in url:
        url = '%s&' % url
    else:
        url = '%s?' % url
    for k in params.keys():
        url = '%s%s=%s&' % (url, k, url_escape(params[k]))
    return url

def _http_get(url, params):
    url = _format_url(url, params)
    json = http_helper.get(url)
    
    if None == json:
        return None
    obj = str_helper.json_decode(json)
    if obj['code'] != 0:
        return None
    return obj['data']


def get_login_user(token):
    params = {'token': token}
    url = '%sUser/Get' % (config.urls['socRightApi'])
    obj = _http_get(url, params)
    return obj


def get_users_by_usergroup(userGroupID):
    # key = 'soc_right_usergroup_%s' % str(userGroupID)
    # obj = redis_cache.getObj(key = key)
    # if None == obj:
    params = {'userGroupID': str(userGroupID)}
    url = '%sUser/GetByUserGroup' % (config.urls['socRightApi'])
    obj = _http_get(url, params)
    # redis_cache.setObj(key = key, val = obj, time = config.cache['SOCRightInfoTimeOut'])
    if None == obj:
        return []
    return obj


def get_user_by_name(userName):
    # key = 'soc_right_userinfo_%s' % userName
    # obj = redis_cache.getObj(key = key)
    # if None == obj:
    params = {'userName': userName}
    url = '%sUser/GetByUserName' % (config.urls['socRightApi'])
    obj = _http_get(url, params)
    # redis_cache.setObj(key = key, val = obj, time = config.cache['SOCRightInfoTimeOut'])    
    return obj
    
