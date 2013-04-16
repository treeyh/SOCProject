#-*- encoding: utf-8 -*-

import tornado.web
import config

from datetime import datetime, timedelta
import admin_base_handler
from common import redis_cache, state, error
from helper import str_helper, http_helper
from proxy import soc_right_proxy
from logic import product_logic

class ProductListHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCPMConfig['appCode'] + '.AppManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config('产品列表')
        product = self.get_args(['userRealName', 'name'], '')
        product['status'] = int(self.get_arg('status', '0'))

        ps['page'] = int(self.get_arg('page', '1'))
        ps['pagedata'] = product_logic.ProductLogic.instance().query_page(name = product['name'], 
                        userRealName = product['userRealName'], status= product['status'], 
                        page = ps['page'], size = ps['size'])
        ps['product'] = product
        ps['pager'] = self.build_page_html(page = ps['page'], size = ps['size'], total = ps['pagedata']['total'], pageTotal = ps['pagedata']['pagetotal'])        
        self.render('admin/product/list.html', **ps)

class ProductAddOrEditHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCPMConfig['appCode'] + '.AppManager'
    _right = 0

    def get(self):
        ps = self.get_page_config('创建产品')
        ps['users'] = soc_right_proxy.get_users_by_usergroup(userGroupID = config.SOCPMConfig['productUserGroupID'])
        if ps['isedit']:
            # self.check_oper_right(right = state.operEdit)
            ps['title'] = self.get_page_title('编辑产品')
            id = int(self.get_arg('id', '0'))
            product = product_logic.ProductLogic.instance().query_one(id)
            if None == product:
                ps['msg'] = state.ResultInfo.get(110001, '')
                ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Product/List'
                product = {'id':'','name':'','userName':'','userRealName':'','remark':'','status':1,'creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        else:
            # self.check_oper_right(right = state.operAdd)
            product = self.get_args(['name', 'userName', 'userRealName', 'remark'], '')
            product['status'] = int(self.get_arg('status', '0'))
            product['id'] = int(self.get_arg('id', '0'))
            # if product['userRealName'] == '' and len(ps['users']) > 0:
            #     product['userRealName'] = ps['users'][0]['userRealName']
        ps['product'] = product
        self.render('admin/product/add_or_edit.html', **ps)


    def post(self):
        ps = self.get_page_config('创建产品')
        if ps['isedit']:
            ps['title'] = self.get_page_title('编辑产品')

        product = self.get_args(['userName', 'name', 'userRealName', 'remark'], '')
        product['status'] = int(self.get_arg('status', '0'))
        product['id'] = int(self.get_arg('id', '0'))
        ps['product'] = product
        ps['users'] = soc_right_proxy.get_users_by_usergroup(userGroupID = config.SOCPMConfig['productUserGroupID'])
        msg = self.check_str_empty_input(product, ['name', 'userName'])
        if str_helper.is_null_or_empty(msg) == False:
            ps['msg'] = msg
            self.render('admin/product/add_or_edit.html', **ps)
            return        
        product['user'] = self.get_oper_user()
        if ps['isedit']:
            # self.check_oper_right(right = state.operEdit)
            try:
                info = product_logic.ProductLogic.instance().update(id = product['id'], name = product['name'], 
                        userName = product['userName'], userRealName = product['userRealName'], status = product['status'],
                        remark = product['remark'], user = product['user'])
                if info:
                    self.redirect(ps['siteDomain'] + 'Admin/Product/List')
                    return
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.ProjectError as e:
                ps['msg'] = e.msg
        else:
            # self.check_oper_right(right = state.operAdd)
            try:
                info = product_logic.ProductLogic.instance().add(name = product['name'], 
                        userName = product['userName'], userRealName = product['userRealName'], status = product['status'],
                        remark = product['remark'], user = product['user'])
                if info > 0:
                    self.redirect(ps['siteDomain'] + 'Admin/Product/List')
                    return
                else:
                    ps['msg'] = state.ResultInfo.get(101, '')
            except error.ProjectError as e:
                ps['msg'] = e.msg
        ps = self.format_none_to_empty(ps)
        self.render('admin/product/add_or_edit.html', **ps)



class ProductDelHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCPMConfig['appCode'] + '.AppManager'
    _right = state.operDel

    def post(self):
        code = self.get_arg('code', '')
        user = self.get_oper_user()
        type = application_logic.ApplicationLogic.instance().delete(code = code, user = user)
        if type:
            self.out_ok()
        else:
            self.out_fail(code = 101)

class ProductDetailHandler(admin_base_handler.AdminRightBaseHandler):
    _rightKey = config.SOCPMConfig['appCode'] + '.AppManager'
    _right = state.operView

    def get(self):
        ps = self.get_page_config('产品详情')
        id = self.get_arg('id', '')
        product = product_logic.ProductLogic.instance().query_one(id)
        if None == product:
            ps['msg'] = state.ResultInfo.get(110001, '')
            ps['gotoUrl'] = ps['siteDomain'] + 'Admin/Product/List'
            product = {'id':'','name':'','userName':'','userRealName':'','remark':'','status':1,'creater':'','createTime':'','lastUpdater':'','lastUpdateTime':''}
        
        ps['product'] = product
        self.render('admin/product/detail.html', **ps)