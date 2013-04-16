#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error

class TaskHistoryLogic():

    def __init__(self):   
        return

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance



    _query_sql = '''  SELECT t.id, t.name, t.projectID, t.userName, t.userRealName, 
                            t.startDate, t.endDate, t.users, t.preID, t.parentID, t.sort, t.`status`, 
                            t.remark, t.isDelete, t.creater, t.createTime, t.lastUpdater, 
                            t.lastUpdateTime , ta.name AS preName
                    FROM pm_task AS t 
                    LEFT JOIN pm_task as ta ON ta.id = t.preID 
                    WHERE isDelete = %s   '''
    _query_col = str_helper.format_str_to_list_filter_empty('id, name, projectID, userName, userRealName, startDate, endDate, users, preID, parentID, sort, status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, preName', ',')
    def query_page(self, projectID):
        sql = self._query_sql
        isdelete = state.Boole['false']
        sql = sql + ' AND projectID = %s order by sort asc '
        tasks = mysql.find_all(sql, yz, self._query_col)
        yz = (isdelete, projectID)
        tasks = self._format_project_tasks(tasks)
        return tasks


    def query_one(self, id = 0):
        sql = self._query_sql
        ps = [isdelete]        
        isdelete = state.Boole['false']
        if 0 != id:
            sql = sql + ' and id = %s '
            ps.append(id)
        else:
            return None
        yz = tuple(ps)
        task = mysql.find_one(sql, yz, self._query_col)
        task = self._format_task_status(task)
        return task



    _add_sql = '''   INSERT INTO pm_task(name, projectID, userName, 
                        userRealName, startDate, endDate, users, `preID`, parentID, sort, 
                        status, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
    def add(self, name, projectID, userName, userRealName, 
            startDate, endDate, users, preID, parentID, sort, status, remark, user):
        isdelete = state.Boole['false']
        yz = (name, projectID, userName, userRealName, 
            startDate, endDate, users, preID, parentID, sort, status, remark, isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz, isbackinsertid = True)
        return result


    _update_sql = '''   UPDATE pm_task SET name = %s, userName = %s, 
                            userRealName = %s, users = %s, status = %s, 
                            remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() WHERE id = %s '''
    def update(self, id, name, userName, userRealName, users, status,
                remark, user):
        yz = (name, userName, userRealName, users, status,
                remark, user, id)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        return 0 == result


    _update_taskid_sql = '''   UPDATE pm_task_history SET taskID = %s WHERE taskID = %s '''
    def update_taskid(self, newTaskID, oldTaskID, user):
        yz = (newTaskID, oldTaskID)
        result = mysql.insert_or_update_or_delete(self._update_taskid_sql, yz)
        return 0 == result
    
    _delete_sql = '''   UPDATE pm_task SET isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where projectID = %s AND isDelete = %s  '''
    def delete_by_projectID(self, projectID, user):
        isdelete = state.Boole['true']
        isdeletefalse = state.Boole['false']
        yz = (isdelete, user, projectID, isdeletefalse)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result
