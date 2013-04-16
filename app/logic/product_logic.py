#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error

class ProductLogic():

    def __init__(self):   
        return

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance



    _query_sql = '''  select id, name, userName, userRealName, `status`, remark, isDelete, 
                    creater, createTime, lastUpdater, lastUpdateTime  from  pm_product   where  isDelete = %s   '''
    _query_col = str_helper.format_str_to_list_filter_empty('id, name, userName, userRealName, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime', ',')
    ''' 分页查询产品信息 '''
    def query_page(self, name = '', userRealName = '', status = 0, page = 1 , size = 12):
        sql = self._query_sql
        isdelete = state.Boole['false']
        ps = [isdelete]
        if 0 != status:
            sql = sql + ' and status = %s '
            ps.append(status)
        if '' != name:
            sql = sql + ' and name like %s '
            ps.append('%'+name+'%')
        if '' != userRealName:
            sql = sql + ' and userRealName like %s '
            ps.append('%'+userRealName+'%')
        sql = sql + ' order by createTime asc '
        yz = tuple(ps)
        products = mysql.find_page(sql, yz, self._query_col, page, size)
        if None != products['data']:
            for r in products['data']:
                r['statusname'] = state.Status.get(r['status'])
        return products
 
    ''' 根据id查询产品信息 '''
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
        product = mysql.find_one(sql, yz, self._query_col)
        if None != product:
            product['statusname'] = state.Status.get(product['status'])
        return product

    ''' 根据名称查询产品信息 '''
    def query_one_by_name(self, name = ''):
        sql = self._query_sql
        isdelete = state.Boole['false']
        sql = sql + ' and name = %s '
        yz = (isdelete, name)
        product = mysql.find_one(sql, yz, self._query_col)
        if None != product:
            product['statusname'] = state.Status.get(product['status'])
        return product


    _query_all_by_active_sql = '''  select id, name from pm_product  where isDelete = %s   '''
    _query_all_by_active_col = str_helper.format_str_to_list_filter_empty('id, name', ',')
    ''' 查询所有可用的产品信息 '''
    def query_all_by_active(self):
        sql = self._query_all_by_active_sql
        isdelete = state.Boole['false']
        sql = sql + ' and status = %s order by createTime asc '        
        yz = (isdelete, state.statusActive)
        products = mysql.find_all(sql, yz, self._query_all_by_active_col)
        return products

    _query_all_by_project_sql = ''' select p.id, p.name from pm_product_project as pp 
                                        LEFT JOIN pm_product as p ON p.id = pp.productID
                                        WHERE pp.projectID = %s and pp.isDelete = %s order by pp.createTime asc'''
    _query_all_by_project_col = str_helper.format_str_to_list_filter_empty('id, name', ',')
    ''' 根据项目ID查询产品信息 '''
    def query_all_by_project(self, projectID):
        sql = self._query_all_by_project_sql
        isdelete = state.Boole['false']
        yz = (projectID, isdelete)
        products = mysql.find_all(sql, yz, self._query_all_by_project_col)
        return products

    ''' 根据IDs查询产品信息 '''
    def query_by_ids(self, ids = []):
        sql = self._query_all_by_active_sql
        isdelete = state.Boole['false']
        idss = ''
        for i in ids:
            if idss == '':
                idss = i
            else:
                idss = idss + ',' + i 
        if idss == '':
            return []
        sql = sql + ' and id in ('+idss+') order by createTime asc '        
        yz = (isdelete)
        products = mysql.find_all(sql, yz, self._query_all_by_active_col)
        return products


    _add_sql = '''   INSERT INTO pm_product(name, userName, userRealName, `status`, remark, isDelete, 
                    creater, createTime, lastUpdater, lastUpdateTime)  
                        VALUES(%s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
    ''' 添加产品 '''
    def add(self, name, userName, userRealName, status, remark, user):
        obj = self.query_one_by_name(name = name)
        if None != obj:
            raise error.ProjectError(code = 110002)

        isdelete = state.Boole['false']
        yz = (name, userName, userRealName, status, remark, isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz, True)
        return result


    _update_sql = '''   update pm_product set name = %s, userName = %s, 
                            userRealName = %s, status = %s, remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s '''
    ''' 更新产品信息 '''
    def update(self, id, name, userName, userRealName, status, remark, user):
        obj = self.query_one_by_name(name = name)
        if None != obj and str(obj['id']) != str(id):
            raise error.ProjectError(code = 110002)

        yz = (name, userName, userRealName, status, remark, user, id)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        return 0 == result

    
    _delete_sql = '''   update pm_product set isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where id = %s  '''
    ''' 删除产品信息 '''
    def delete(self, id, user):
        isdelete = state.Boole['true']
        yz = (isdelete, user, id)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result


