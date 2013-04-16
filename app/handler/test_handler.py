#-*- encoding: utf-8 -*-


import tornado.web
import tornado.escape

from common import redis_cache
from helper import str_helper
import config

from datetime import datetime
import base_handler


class TestHandler(base_handler.BaseHandler):
    def get(self):
        self.out_ok('','')
    
    def post(self):
        ps = self.get_page_config('登录')
        ps['appcode'] = self.get_arg('appcode', ps['appcode'])
        username = self.get_arg('username', '')
        password = self.get_arg('password', '')        
        if username == '' or password == '':
            self.redirect("/Login?msg=100001")
            return
        user = user_logic.UserLogic.instance().login(username, password, ps['appcode'])
        if None == user:
            self.redirect("/Login?msg=100002")
            return
        uuid = str_helper.get_uuid()
        print uuid
        user = json_encode(user)
        redis_cache.set(uuid, user, config.cache['userTimeOut'])
        self.set_cookie(name = config.SOCPMConfig['cookiename'], value=uuid, expires=config.cache['userTimeOut'])
        self.render("login.html", **ps)
        



