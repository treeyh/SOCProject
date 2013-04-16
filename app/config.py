#-*- encoding: utf-8 -*-

import os


SOCPMConfig = {
    'version':'1',
    'siteName' : '云海项目管理平台',
    'jsDomain' : '/static/',
    'cssDomain' : '/static/',
    'siteDomain' : 'http://pm.kanchene.com/',
    'rightSiteDomain' : 'http://sso.kanchene.com/',

    'size' : 10,
    'appCode' : 'SOCProject',
    'productUserGroupID' : 2,
    'devUserGroupID' : 1,
    'adminCookieName' : 'soc_project_manager_user',
}

urls = {
    'socRightApi' : SOCPMConfig['rightSiteDomain']+'Api/',
    'adminBackUrl' : SOCPMConfig['siteDomain']+'Admin/Main',
    'loginUrl' : SOCPMConfig['rightSiteDomain']+'Login',
}

#db = {
#    'host' : '192.168.99.83',
#    'user' : 'root',
#    'passwd' : 'root123',
#    'db' : 'ProjectManager',
#    'charset':'utf8',
#}

db = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'passwd' : 'dswybs',
    'db' : 'SOCProject',
    'charset':'utf8',
}


cache = {
    'host' : '127.0.0.1',
    'port' : 6379,
    'db' : 0,
    'userTimeOut' : 86400,
    'SOCRightInfoTimeOut' : 600,
}


settings = dict(
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    debug=True,
)


