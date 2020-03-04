

import datetime

import pymysql
from django.shortcuts import render, redirect
import datetime
import re
import pymysql
from django.contrib import admin
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse


def login(request):
    if request.method=="GET":
        #指定要访问的页面，render的功能：讲请求的页面结果提交给客户端
        return render(request, 'login.html')
    else:
        #登录页面提交
        return query(request)

def query(request):

    a = request.POST
    print("request类型：",type(request))
    userName = a.get('username')
    passWord = a.get('password')
    print(userName,passWord)
    user_tup = (userName,passWord)
    db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
    cursor = db.cursor()

    #查询用户名是否存在
    sql = 'select username,password from userdata'
    cursor.execute(sql)
    all_users = cursor.fetchall()
    has_user = 0
    i = 0
    print(all_users)
    while i < len(all_users):
        print(all_users[i])
        if user_tup == all_users[i]:
            sql2='select username,center,project from userdata where username='+"'"+all_users[i][0]+"'"
            print(sql2)
            cursor.execute(sql2)
            userinf = cursor.fetchall()
            print(userinf)
            print("ok")
            name=userinf[0][0]
            center=userinf[0][1]
            project=userinf[0][2]
            has_user = 1
        i += 1

    cursor.close()
    db.close()


    #若用户名存在
    if has_user == 1:
        tablename = "table"+datetime.date.today().strftime('%y%m%d')
        db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
        cursor = db.cursor()

        #查询当日数据表是否存在
        sql = "show tables;"
        cursor.execute(sql)  # 执行sql语句
        tables = [cursor.fetchall()]  # 返回所有结果
        table_list = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_list]
        print(table_list)

        # 若当日表存在
        if tablename in table_list:
            print(tablename)
            print("*************进入1************")
            sql = "SELECT todaywork,todayproblems,tomorrowwork FROM {table} WHERE username='{username}'".format(table=tablename,username=name)
            cursor.execute(sql)
            data = cursor.fetchall()
            print(data)
            if len(data)>0:
                print("!=")
                data1=data[0][0]
                data2=data[0][1]
                data3=data[0][2]
            else:
                print("=")
                data1=""
                data2=""
                data3=""
            return render(request,'inputdata.html',{"name":name,"center":center,"project":project,"data1":data1,"data2":data2,"data3":data3})

        #若当日表不存在
        else:
            print("**************进入2*****************")
            return render(request, 'inputdata.html',{"name":name,"center":center,"project":project})
            # return render(request, 'inputdata.html',
            #               {"name": name, "center": center, "project": project})

    #若用户名不存在
    else:
        print("***********进入3************")
        return render(request,'login.html',{"message":"用户名或密码错误！请重新输入。"})

def group(request):
    if request.method=="GET":
        today="table"+datetime.date.today().strftime('%y%m%d')
        db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
        db.autocommit(True) #自动提交
        cursor = db.cursor()
        # cursor = db.cursor(sursor=pymysql.cursors.DictCursor)
        sql = 'select * from {table}'.format(table=today)
        cursor.execute(sql)
        userdata = cursor.fetchall()
        cursor.close()
        db.close()
        print(userdata)
        return render(request,"showAllData.html",{"data":userdata,"time":datetime.date.today().strftime('%y%m%d')})
    # method==POST
    else:
        pass

def addelem(request):
    if request.method == "GET":
        return render(request, "addelem.html")
    else:
        data1=request.POST.get("name")
        data2=request.POST.get("center")
        data3=request.POST.get("project")
        data4=request.POST.get("todaywork")
        data5=request.POST.get("todayproblem")
        data5=request.POST.get("tomorrowwork")
        #下一步写入数据库并返回成功页面
        return redirect("/showdata/")

def addelem2(request):
    title=request.POST.get("title")
    print("title",title)
    #执行SQL语句
    if title:
        return HttpResponse("ok")
    else:
        return HttpResponse("不能为空！")

def delelem(request):
    name=request.POST.get("name")
    #删除name记录


    return redirect("/showdata/")
#

def editelem(request):
    if request.method=="GET":
        name=request.POST.get("name")
        #数据库查询信息并返回页面，这里可使用字典方式返回数据库结果
        return redirect("editelem.html")
    else:

        #数据库修改操作
        return redirect("/showdata/")
#

#注册页面
def register(request):
    if request.method == "GET":
        return render(request,'register.html')
    else:
        return save(request)
        # save(request)


#定义一个函数，用来保存注册的数据
def save(request):
    has_register = 0#用来记录当前账号是否已存在，0：不存在 1：已存在
    a = request.POST#获取get()请求
    #print(a)
    #通过get()请求获取前段提交的数据
    userName = a.get('username')
    passWord = a.get('password')
    center = a.get('center')
    project = a.get('project')
    if(userName=="" or passWord=="" or center=="" or project==""):
        return render(request,'register.html',{"message":"请补全注册信息！"})

    #print(userName,passWord)
    # #连接MongoDB数据库
    # conn = MongoClient('47.105.38.117', 27017)
    # db = conn.long_distance_data  # 选定数据库，设定数据库名称为file
    # #创建游标
    # mycol = db['userdata']  # 用户文件表
    # # print(mycol.find({age: {$exists: true}}))
    # mycol.insert({'userName': userName,'passWord':passWord})
    # return HttpResponse('注册成功')
    # cursor = db.cursor()

    db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
    sql1 = 'select username from userdata'
    #执行SQL语句
    cursor = db.cursor()
    cursor.execute(sql1)
    #查询到所有的数据存储到all_users中
    all_users = cursor.fetchall()
    print(all_users)
    i = 0
    while i < len(all_users):
        if userName in all_users[i]:
            ##表示该账号已经存在
            has_register = 1

        i += 1
    if has_register == 0:
        # 将用户名与密码插入到数据库中
        sql2 = 'insert into userdata(username,password,center,project) values(%s,%s,%s,%s)'
        cursor.execute(sql2,(userName,passWord,center,project))
        db.commit()
        cursor.close()
        db.close()
        # return HttpResponse('注册成功')
        return render(request, 'login.html',{"message":"用户注册成功，请登录！"})
    else:

        cursor.close()
        db.close()
        return render(request, 'register.html',{"message":"用户已存在！"})



def savedata(request):
    has_register = 0#用来记录当前账号是否已存在，0：不存在 1：已存在
    today = datetime.date.today().strftime('%y%m%d')
    a = request.POST#获取get()请求
    #print(a)
    #通过get()请求获取前段提交的数据
    username = a.get('username')
    center = a.get('center')
    project = a.get('project')
    todaywork = a.get('todaywork').strip()
    todayproblems = a.get('todayproblems').strip()
    tomorrowwork = a.get('tomorrowwork').strip()
    print(username,center,project,todaywork,todayproblems,tomorrowwork)
    db = pymysql.connect("47.105.38.117", "root", "1234", "long_distance_data", port=3306, charset='utf8')
    cursor = db.cursor()
    sql = "show tables;"
    cursor.execute(sql)  # 执行sql语句
    tables = [cursor.fetchall()]  # 返回所有结果
    table_list = re.findall('(\'.*?\')', str(tables))
    table_list = [re.sub("'", '', each) for each in table_list]
    print(table_list)
    values="\'"+username+"\',\'"+center+"\',\'"+project+"\',\'"+todaywork+"\',\'"+todayproblems+"\',\'"+tomorrowwork+"\'"
    print(values)
    if 'table'+today in table_list:  # 存在
        sql1="select count(*) from {table} where username ='{name}';".format(table='table' + today,name=username)
        cursor.execute(sql1)
        res = cursor.fetchall()[0][0]
        print(res)
        #字段不存在 插入
        if( res == 0):
            sql2 = 'INSERT INTO {table} VALUES ({values});'.format(table='table' + today, values=values)
            print(sql2)
            cursor.execute(sql2)

        #字段存在 更新
        else:
            sql2 = "UPDATE {table} SET todaywork='{par1}',todayproblems='{par2}',tomorrowwork='{par3}' WHERE username='{par4}';".format(table='table' + today, par1=todaywork,par2=todayproblems,par3=tomorrowwork,par4=username)
            print(sql2)
            cursor.execute(sql2)


    else:  # 不存在
        sql="CREATE TABLE {table} (username VARCHAR(255), center VARCHAR(255), project VARCHAR(255),todaywork text, todayproblems text, tomorrowwork text)default charset=utf8;".format(table="table"+today)
        print(sql)
        cursor.execute(sql)
        sql2 = 'INSERT INTO {table} VALUES ({values});'.format(table='table'+today, values=values)
        print(sql2)
        cursor.execute(sql2)
    db.commit()
    cursor.close()
    db.close()
    return render(request,'Succeed.html',{"username":username,"center":center,"project":project,"todaywork":todaywork,"todayproblems":todayproblems,"tomorrowwork":tomorrowwork})

    # if today  not in table_list:  # 存在
    #
    # #执行SQL语句
    # cursor = db.cursor()
    # cursor.execute(sql1)
    # #查询到所有的数据存储到all_users中
    # all_users = cursor.fetchall()
    # print(all_users)
    # i = 0
    # while i < len(all_users):
    #     if userName in all_users[i]:
    #         ##表示该账号已经存在
    #         has_register = 1
    #
    #     i += 1
    # if has_register == 0:
    #     # 将用户名与密码插入到数据库中
    #     sql2 = 'insert into userdata(username,password) values(%s,%s)'
    #     cursor.execute(sql2,(userName,passWord))
    #     db.commit()
    #     cursor.close()
    #     db.close()
    #     # return HttpResponse('注册成功')
    #     return HttpResponse('该账号已存在')
    # else:
    #
    #     cursor.close()
    #     db.close()
    #     return HttpResponse('该账号已存在')
