#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error

class ProjectLogic():

    def __init__(self):   
        return

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance



    _query_sql = '''  SELECT id, name, teamPath, productUserName, productUserRealName, devUserName, 
                        devUserRealName, startDate, endDate, `status`, remark, isDelete, creater, createTime, 
                        lastUpdater, lastUpdateTime  FROM  pm_project WHERE isDelete = %s   '''
    _query_col = str_helper.format_str_to_list_filter_empty('id, name, teamPath, productUserName, productUserRealName, devUserName, devUserRealName, startDate, endDate, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
    ''' 分页查询项目信息 '''
    def query_page(self, name = '', productUserRealName = '', devUserRealName = '', 
                        status = 0, page = 1 , size = 12):
        sql = self._query_sql
        isdelete = state.Boole['false']
        ps = [isdelete]
        if 0 != status:
            sql = sql + ' and status = %s '
            ps.append(status)
        if '' != name:
            sql = sql + ' and name like %s '
            ps.append('%'+name+'%')
        if '' != productUserRealName:
            sql = sql + ' and productUserRealName like %s '
            ps.append('%'+productUserRealName+'%')
        if '' != devUserRealName:
            sql = sql + ' and devUserRealName like %s '
            ps.append('%'+devUserRealName+'%')
        sql = sql + ' order by createTime desc '
        yz = tuple(ps)
        projects = mysql.find_page(sql, yz, self._query_col, page, size)

        if None != projects['data']:
            for r in projects['data']:
                r['statusname'] = state.ProjectStatus.get(r['status'])
        return projects
 
    ''' 根据id查询项目信息 '''
    def query_one(self, id = 0):
        sql = self._query_sql
        isdelete = state.Boole['false']
        ps = [isdelete]        
        if 0 != id:
            sql = sql + ' and id = %s '
            ps.append(id)
        else:
            return None
        yz = tuple(ps)
        project = mysql.find_one(sql, yz, self._query_col)
        if None != project:
            project['statusname'] = state.ProjectStatus.get(project['status'])
        return project

 
    ''' 根据名称查询项目信息 '''
    def query_one_by_name(self, name = ''):
        sql = self._query_sql
        isdelete = state.Boole['false']
        sql = sql + ' and name = %s '
        yz = (isdelete, name)
        project = mysql.find_one(sql, yz, self._query_col)
        if None != project:
            project['statusname'] = state.ProjectStatus.get(project['status'])
        return project


    _query_all_by_active_sql = '''  SELECT id, name FROM pm_project WHERE isDelete = %s  '''
    _query_all_by_active_col = str_helper.format_str_to_list_filter_empty('id, name', ',')
    ''' 查询所有可用项目 '''
    def query_all_by_active(self):
        sql = self._query_all_by_active_sql
        isdelete = state.Boole['false']
        sql = sql + ' and status != %s order by createTime desc '        
        yz = (isdelete, state.projectStatusActive)
        products = mysql.find_all(sql, yz, self._query_all_by_active_col)
        return products


    _add_sql = '''   INSERT INTO pm_project(name, teamPath, productUserName, productUserRealName, 
                        devUserName, devUserRealName, startDate, endDate, `status`, remark, isDelete, 
                        creater, createTime, lastUpdater, lastUpdateTime)  
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
    ''' 添加项目 '''
    def add(self, name, teamPath, productUserName, productUserRealName, devUserName, 
            devUserRealName, startDate, endDate, status, remark, user, productIDs = [], users = []):
        obj = self.query_one_by_name(name = name)
        if None != obj:
            raise error.ProjectError(code = 111002)

        isdelete = state.Boole['false']
        yz = (name, teamPath, productUserName, productUserRealName, 
                devUserName, devUserRealName, startDate, endDate, status, remark, isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz, isbackinsertid = True)
        if result > 0:
            self._bind_project_product(result, productIDs, user)
            self._bind_project_user(projectID = result, users = users, user = user)
        return result


    _update_sql = '''   UPDATE pm_project SET name = %s, teamPath = %s, 
                            productUserName = %s, productUserRealName = %s, 
                            devUserName = %s, devUserRealName = %s, startDate = %s, endDate = %s,
                            status = %s, remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s '''
    ''' 更新项目 '''
    def update(self, id, name, teamPath, productUserName, productUserRealName, 
                devUserName, devUserRealName, startDate, endDate, status, remark, user, productIDs = [], users = []):
        obj = self.query_one_by_name(name = name)
        if None != obj and str(obj['id']) != str(id):
            raise error.ProjectError(code = 111002)

        yz = (name, teamPath, productUserName, productUserRealName, devUserName, 
                    devUserRealName, startDate, endDate, status, remark, user, id)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        self._bind_project_product(id, productIDs, user)
        self._bind_project_user(projectID = id, users = users, user = user)
        return 0 == result

    
    _delete_sql = '''   UPDATE pm_project SET isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s  '''
    ''' 删除项目 '''
    def delete(self, id, user):
        isdelete = state.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result


    _add_bind_project_product_sql = '''  INSERT INTO pm_product_project(productID, projectID, 
                            remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                            VALUES(%s, %s, %s, %s, %s, now(), %s , now()) '''
    _del_bind_project_product_sql = '''  UPDATE pm_product_project SET isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() WHERE projectID = %s AND isDelete = %s  '''
    ''' 绑定项目与产品 '''
    def _bind_project_product(self, projectID, productIDs, user):
        isdeletefalse = state.Boole['false']
        isdeletetrue = state.Boole['true']
        yz = (isdeletetrue, user, projectID, isdeletefalse)
        result = mysql.insert_or_update_or_delete(self._del_bind_project_product_sql, yz)
        for productID in productIDs:
            yz = (productID, projectID, '', isdeletefalse, user, user)
            result = mysql.insert_or_update_or_delete(self._add_bind_project_product_sql, yz)
        return 0 == result


    _add_bind_project_user_sql = '''  INSERT INTO pm_project_user(projectID, userName, 
                            userRealName, type, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                            VALUES(%s, %s, %s, %s, %s, %s, %s, now(), %s , now()) '''
    _del_bind_project_user_sql = '''  UPDATE pm_project_user SET isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() WHERE projectID = %s AND isDelete = %s  '''
    ''' 绑定项目与人员 '''
    def _bind_project_user(self, projectID, users, user):
        isdeletefalse = state.Boole['false']
        isdeletetrue = state.Boole['true']
        yz = (isdeletetrue, user, projectID, isdeletefalse)
        result = mysql.insert_or_update_or_delete(self._del_bind_project_user_sql, yz)
        for user in users:
            yz = (projectID, user['userName'], user['userRealName'], user['type'], '', isdeletefalse, user, user)
            result =  mysql.insert_or_update_or_delete(self._add_bind_project_user_sql, yz)
        return 0 == result


    _query_user_by_projectID_sql = ''' select id, projectID, userName, userRealName, type, remark from pm_project_dev 
                            where projectID = %s and isDelete = %s order by type asc '''
    _query_user_by_projectID_col = str_helper.format_str_to_list_filter_empty('id, projectID, userName, userRealName, type, remark', ',')
    ''' 查询项目开发者 '''
    def query_user_by_project(self, projectID):
        isdelete = state.Boole['false']
        
        yz = (projectID, isdelete)
        users = mysql.find_all(self._query_user_by_projectID_sql, yz, self._query_user_by_projectID_col)
        return users

    