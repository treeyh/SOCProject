#-*- encoding: utf-8 -*-

from helper import str_helper
from common import mysql, state, error

from logic import task_history_logic

class TaskLogic():

    def __init__(self):   
        return

    _instance = None
    @classmethod
    def instance(cls):
        if cls._instance == None:
            cls._instance = cls()
        return cls._instance



    _query_sql = '''  SELECT t.id, t.name, t.projectID, t.userName, t.userRealName, t.date,
                            t.startDate, t.endDate, t.users, t.preID, t.parentID, t.sort, t.`status`, t.degree,
                            t.remark, t.isDelete, t.creater, t.createTime, t.lastUpdater, 
                            t.lastUpdateTime , ta.name AS preName, p.name as projectName
                    FROM pm_task AS t 
                    LEFT JOIN pm_task as ta ON ta.id = t.preID 
                    LEFT JOIN pm_project as p ON p.id = t.projectID 
                    WHERE t.isDelete = %s   '''
    _query_col = str_helper.format_str_to_list_filter_empty('id, name, projectID, userName, userRealName, date, startDate, endDate, users, preID, parentID, sort, status, degree, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime, preName, projectName', ',')
    def query_by_projectID(self, projectID):
        sql = self._query_sql
        isdelete = state.Boole['false']
        sql = sql + ' AND t.projectID = %s order by sort asc '
        yz = (isdelete, projectID)
        tasks = mysql.find_all(sql, yz, self._query_col)        

        if tasks != None or len(tasks) > 0:
            for task in tasks:
                task = self._format_task_status(task)
        return tasks


    def query_one(self, id = 0):
        sql = self._query_sql
        isdelete = state.Boole['false']
        ps = [isdelete]
        if 0 != id:
            sql = sql + ' and t.id = %s '
            ps.append(id)
        else:
            return None
        yz = tuple(ps)
        task = mysql.find_one(sql, yz, self._query_col)
        task = self._format_task_status(task)
        return task


    def save_tasks(self, projectID, tasks, user):
        '''  保存任务信息(还没有事务)
            1、isdelete原有的任务信息
            2、插入新的任务信息，并获取ID
            3、如果有老的ID，原来的关系替换成新的ID
            4、设置preid、parentID
        '''
        code = self._check_tasks_info(tasks)
        if code != 0:
            raise error.ProjectError(code = code)
        #删除老任务
        result = self.delete_by_projectID(projectID = projectID, user = user)
        if not result:
            raise error.ProjectError(code = 112005)

        #插入新任务
        sortMap = {0:0}
        for task in tasks:
            taskid = self.add(name = task['name'], projectID = projectID, userName = task['userName'],
                        userRealName = task['userRealName'],date = task['date'], startDate = task['startDate'], 
                        endDate = task['endDate'], users = task['users'], preID = 0, parentID = 0,
                        sort = task['sort'], status = 0, degree = task['degree'], remark = '', user = user)
            task['id'] = taskid
            sortMap[task['sort']] = taskid
            if task.get('taskID', 0) > 0:
                #如果有老ID，替换成新ID
                task_history_logic.TaskHistoryLogic.instance().update_taskid(newTaskID = taskid, 
                    oldTaskID = task['taskID'], user = user)

        #检索，如果有preid和parentid的进行设置
        for task in tasks:
            if task['parentID'] > 0 or task['preID'] > 0:
                parentID = sortMap.get(task['parentID'], 0)
                preID = sortMap.get(task['preID'], 0)
                self.update_parentID_preID(id = task['id'], parentID = parentID, preID = preID, user = user)

        return True



    _add_sql = '''   INSERT INTO pm_task(name, projectID, userName, 
                        userRealName, date, startDate, endDate, users, `preID`, parentID, sort, 
                        status, degree, remark, isDelete, creater, createTime, lastUpdater, lastUpdateTime)  
                        VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), %s, now())  '''
    def add(self, name, projectID, userName, userRealName, date,  
            startDate, endDate, users, preID, parentID, sort, status, degree, remark, user):
        isdelete = state.Boole['false']
        yz = (name, projectID, userName, userRealName, date ,
            startDate, endDate, users, preID, parentID, sort, status, degree, remark, isdelete, user, user)
        result = mysql.insert_or_update_or_delete(self._add_sql, yz, isbackinsertid = True)
        return result


    _update_parentID_preID_sql = '''   UPDATE pm_task SET parentID = %s, preID = %s, 
                            lastUpdater = %s, lastUpdateTime = now() WHERE id = %s '''
    def update_parentID_preID(self, id, parentID, preID, user):
        yz = (parentID, preID, user, id)
        result = mysql.insert_or_update_or_delete(self._update_parentID_preID_sql, yz)
        return 0 == result


    _update_sql = '''   UPDATE pm_task SET name = %s, userName = %s, 
                            userRealName = %s, users = %s, status = %s, degree = %s,
                            remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() WHERE id = %s '''
    def update(self, id, name, userName, userRealName, users, status, degree,
                remark, user):
        yz = (name, userName, userRealName, users, status, degree, 
                remark, user, id)
        result = mysql.insert_or_update_or_delete(self._update_sql, yz)
        return 0 == result



    update_degree_remark_sql = '''   UPDATE pm_task SET degree = %s, users = %s, 
                            remark = %s, lastUpdater = %s, 
                            lastUpdateTime = now() WHERE id = %s '''
    def update_degree_remark(self, id, degree, users, remark, user):
        yz = (degree, users, remark, user, id)
        result = mysql.insert_or_update_or_delete(self.update_degree_remark_sql, yz)
        return 0 == result



    
    _delete_sql = '''   UPDATE pm_task SET isDelete = %s, lastUpdater = %s, 
                            lastUpdateTime = now() where projectID = %s AND isDelete = %s  '''
    def delete_by_projectID(self, projectID, user):
        isdelete = state.Boole['true']
        isdeletefalse = state.Boole['false']
        yz = (isdelete, user, projectID, isdeletefalse)
        result = mysql.insert_or_update_or_delete(self._delete_sql, yz)
        return 0 == result





    def _format_task_status(self, task):
        if None == task:
            return None
        if task['status'] == 0:
            task['statusname'] = '未开始'
        elif task['status'] >= 100:
            task['statusname'] = '已完成'
        else:
            task['statusname'] = '%d%' % (task['status'])   
        return task


    def _check_tasks_info(self, tasks):
        if None == tasks or type(tasks) != list:
            return 112001

        for task in tasks:
            if str_helper.is_null_or_empty(task.get('userName', '')) or str_helper.is_null_or_empty(task.get('userRealName', '')):
                return 112002
            if str_helper.is_null_or_empty(task.get('startDate', '')) or str_helper.is_null_or_empty(task.get('endDate', '')):
                return 112003
            if str_helper.is_null_or_empty(task.get('name', '')):
                return 112004
            if task.get('degree', 0) < 0 or task.get('degree', 0) > 100:
                return 112008

        return 0