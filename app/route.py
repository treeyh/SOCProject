#-*- encoding: utf-8 -*-

import os
from handler import test_handler
from handler.admin import main_handler, product_handler, project_handler, task_handler




'''        路由规则         '''

route = []

route.append((r'^/Test', test_handler.TestHandler))

#route.append((r'^/', main_handler.MainHandler))        #后台程序需开启这个
route.append((r'^/Admin', main_handler.MainHandler))
route.append((r'^/Admin/Main', main_handler.MainHandler))
route.append((r'^/Admin/NotRight', main_handler.NotRightHandler))
route.append((r'^/Admin/Logout', main_handler.LogoutHandler))


route.append((r'^/Admin/Product/List', product_handler.ProductListHandler))
route.append((r'^/Admin/Product/Add', product_handler.ProductAddOrEditHandler))
route.append((r'^/Admin/Product/Edit', product_handler.ProductAddOrEditHandler))
route.append((r'^/Admin/Product/Detail', product_handler.ProductDetailHandler))
#route.append((r'^/Admin/Product/Del', product_handler.ProductDelHandler))

route.append((r'^/Admin/Project/List', project_handler.ProjectListHandler))
route.append((r'^/Admin/Project/Add', project_handler.ProjectAddOrEditHandler))
route.append((r'^/Admin/Project/Edit', project_handler.ProjectAddOrEditHandler))
route.append((r'^/Admin/Project/Detail', project_handler.ProjectDetailHandler))
route.append((r'^/Admin/Project/Del', project_handler.ProjectDelHandler))



route.append((r'^/Admin/Task/ProjectList', task_handler.TaskProjectListHandler))
route.append((r'^/Admin/Task/ProjectEdit', task_handler.TaskProjectAddOrEditHandler))
route.append((r'^/Admin/Task/Edit', task_handler.TaskAddOrEditHandler))