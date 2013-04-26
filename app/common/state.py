#-*- encoding: utf-8 -*-

ResultInfo = {
    0 : 'OK',

    101 : '数据库操作失败',
    
    1001 : '参数缺少或错误',

    1002 : '该对象不存在',
    1003 : '该对象已存在',
    1004 : '无权限执行该操作',


    110001 : '该产品不存在',
    110002 : '该产品名称已存在',


    111001 : '该项目不存在',
    111002 : '该项目名称已存在',
    111003 : '目前还没有添加项目',

    
    112001 : '任务列表为不能空',
    112002 : '任务负责人不能空',
    112003 : '任务开始日期和结束日期不能为空',
    112004 : '任务名称不能为空',
    112005 : '删除旧的任务数据失败',
    112006 : '添加任务需要选择项目',
    112007 : '该任务不存在',
    112008 : '该任务完成度只能是0~100之间的整数',

    999999 : '未知错误',
}

Boole = {
    'true' : 1,
    'false' : 2,
}

User = {
    'normal' : 1,
    'leave' : 10,
}


Status = {
    1 : '可用',
    2 : '不可用',
}

TaskStatus = {
    1 : '未开始',
    2 : '进行中',
    3 : '已完成',
}
TaskNoRunStatus = 1 
TaskRunningStatus = 2
TaskRunedStatus = 3


ProjectStatus = {
    1 : '需求分析',
    2 : '概要设计',
    3 : '详细设计',
    4 : '迭代开发',
    5 : '系统测试',
    6 : '项目上线',
    7 : '后期维护',
    8 : '项目结束',
}
projectStatusActive = 8

statusActive = 1

operView = 1
operAdd = 2
operEdit = 4
operDel = 8

ProjectRoles = [
    {'id' : 10 , 'name' : u'产品经理', 'isOne' : True},
    {'id' : 11 , 'name' : u'产品团队', 'isOne' : False},
    {'id' : 20 , 'name' : u'技术经理', 'isOne' : True},
    {'id' : 21 , 'name' : u'开发团队', 'isOne' : False},
    {'id' : 30 , 'name' : u'测试经理', 'isOne' : True},
    {'id' : 31 , 'name' : u'测试团队', 'isOne' : False},
]

productManagerRoleID=10
devManagerRoleID=20


TaskTypes = [
    {'id' : 1 , 'name' : u'项目工作'},
    {'id' : 2 , 'name' : u'会议'},
    {'id' : 3 , 'name' : u'例行工作'},
    {'id' : 4 , 'name' : u'例行工作111'},
]