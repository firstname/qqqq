# coding:utf-8
from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth.models import User,Group,Permission 
from django.contrib import messages
from django.template.context import RequestContext
from django.utils import timezone
import time
import os
import pandas as pd #除了pip安装pandas,还要安装xlrd、xlwt以进行excel读写
import numpy as np
import re

from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

#from bootstrap_toolkit.widgets import BootstrapUneditableInput
from .models import *
from .forms import *

def login(request):
    #初次访问
    if request.method == 'GET':
        loginform = LoginForm()
        return render_to_response('accounts/login.html', RequestContext(request, {'form': loginform,}))
    #已经post提交数据
    else:
        loginform = LoginForm(request.POST)
        if loginform.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if not user.count():
                return render_to_response('accounts/login.html', RequestContext(request, {'form': loginform,'user_not_exist':True}))
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                #登录成功
                auth.login(request, user)
                #return render_to_response('accounts/message.html', RequestContext(request, {'form': loginform,'words':'登录成功',})) 
                return HttpResponseRedirect('/', RequestContext(request, {'form': loginform,}))
                #return render_to_response('login/index.html', RequestContext(request))
            else:
                #登录失败
                return render_to_response('accounts/login.html', RequestContext(request, {'form': loginform,'password_is_wrong':True}))
        else:
            #form无效
            return render_to_response('accounts/login.html', RequestContext(request, {'form': loginform,}))


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")


def register(request):
    #初次访问
    if request.method == 'GET':
        regform = RegisterForm()
        return render_to_response('accounts/register.html', RequestContext(request, {'form': regform,}))
    #已经提交数据
    else:
        regform = RegisterForm(request.POST)
        if regform.is_valid():
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            phone = request.POST.get('phone', '')
            #usergroup = request.POST.get('usergroup', '')
            usergroup='is_student'#默认以学生角色注册
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if user.count():
                return render_to_response('accounts/register.html', RequestContext(request, {'form': regform,}))
            #注册成功
            user = User.objects.create_user( username, email, password1 )
            user.save()
            #用户扩展信息 profile  
            profile=UserProfile()#e*************************  
            profile.user_id=user.id  
            profile.phone=phone
            profile.usergroup=usergroup  
            profile.save()  
            #用户组是否存在
            group = Group.objects.filter(name=usergroup)
            groupperms = Permission.objects.get(codename=usergroup)
                                                #这里usergroup名字来自form要和权限里的对应上
            if not group.count():#如果用户组不存在则创建
                group = Group.objects.create(name=usergroup)
                group.permissions.add(groupperms )#给组赋予权限
                group.save()

            #用户组存在,给用户赋予组和权限
            group = Group.objects.get(name=usergroup)
            user = User.objects.get(username=username)
            user.groups.add(group)#给用户赋予组
            user.user_permissions.add(groupperms)#给用户赋予组权限
            user.save()
            #用户信息写入 student  
            # stu = Student()#e*************************  
            # stu.user_id = user.id  
            # stu.username = username
            # stu.email = email
            # stu.password = password1
            # stu.creater = operator
            # stu.createddate = timezone.now()
            # stu.save()
            #自动登录
            user = auth.authenticate(username=username, password=password1)#登录前需要先验证  
            if user is not None and user.is_active:
                auth.login(request, user) 
                return render_to_response('accounts/message.html', RequestContext(request, {'form': regform,'words':'注册成功', }))          
        else:
            return render_to_response('accounts/register.html', RequestContext(request, {'form': regform,}))

@login_required
def changepassword(request):
    #初次访问
    if request.method == 'GET':
        chgform = PasswordForm()
        return render_to_response('accounts/changepassword.html', RequestContext(request, {'form': chgform,}))
    #已经提交数据
    else:
        chgform = PasswordForm(request.POST)
        if chgform.is_valid():
            username = request.user.username
            oldpassword = request.POST.get('oldpassword', '')
            password1 = request.POST.get('newpassword1', '')
            password2 = request.POST.get('newpassword2', '')
            #检查旧密码
            user = auth.authenticate(username=username, password=oldpassword)
            if user is None or not user.is_active:
                #旧密码错误
                return render_to_response('accounts/changepassword.html', RequestContext(request, {'form': chgform,'password_is_wrong':True})) 
            else:
                user = User.objects.get(username__exact= username)
                user.set_password(password1)
                user.save()
                return render_to_response('accounts/message.html', RequestContext(request, {'form': chgform,'words':'修改成功',}))                                   
        else:
            return render_to_response('accounts/changepassword.html', RequestContext(request, {'form': chgform,}))

@permission_required('accounts.is_teacher', login_url="/")
def userlist(request):
    users = User.objects.all()
    userprof = UserProfile.objects.all()

    return render_to_response('accounts/userlist.html', RequestContext(request, {
        'users': users,
        'userprof':userprof,
        }))

@login_required
def forgetpassword(request):
    auth.logout(request)
    return HttpResponseRedirect("/")

@permission_required('accounts.is_teacher', login_url="/")
def addstu(request):
    operator = request.user.username
    #初次访问
    if request.method == 'GET':
        regform = AddStuForm()
        return render_to_response('accounts/addstu.html', RequestContext(request, {'form': regform,}))
    #已经提交数据
    else:
        regform = AddStuForm(request.POST)
        if regform.is_valid():
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            usergroup = 'is_student'#默认以学生角色注册
            email = ''
            phone = ''
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if user.count():
                return render_to_response('accounts/addstu.html', RequestContext(request, {'form': regform,}))
            #注册成功
            user = User.objects.create_user( username, email, password1 )
            user.save()
            #用户扩展信息 profile  
            profile=UserProfile()#e*************************  
            profile.user_id=user.id  
            profile.phone=phone
            profile.usergroup=usergroup  
            profile.save()  
            #用户组是否存在
            group = Group.objects.filter(name=usergroup)
            groupperms = Permission.objects.get(codename=usergroup)
                                                #这里usergroup名字来自form要和权限里的对应上
            if not group.count():#如果用户组不存在则创建
                usergroup2 = Group.objects.create(name=usergroup)
                usergroup2.permissions.add(groupperms )#给组赋予权限
                usergroup2.save()

            #用户组存在,给用户赋予组和权限
            group = Group.objects.get(name=usergroup)
            user = User.objects.get(username=username)
            user.groups.add(group)#给用户赋予组
            user.user_permissions.add(groupperms)#给用户赋予组权限
            user.save()
            #用户信息写入 student  
            # stu = Student()#e*************************  
            # stu.user_id = user.id  
            # stu.username = username
            # stu.email = email
            # stu.password = password1
            # stu.creater = operator
            # stu.createddate = timezone.now()
            # stu.save()
            #添加成功
            return render_to_response('accounts/message.html', RequestContext(request, {'form': regform,'words':'添加成功',}))          
        else:
            return render_to_response('accounts/addstu.html', RequestContext(request, {'form': regform,}))
@permission_required('accounts.is_teacher', login_url="/")
def stulist(request):
    users = User.objects.all()
    stus = UserProfile.objects.filter(usergroup='is_student')
    userprof = UserProfile.objects.all()

    return render_to_response('accounts/stulist.html', RequestContext(request, {
        'users': users,
        'stus': stus,
        'userprof':userprof,
        }))



@permission_required('accounts.is_teacher', login_url="/")
def impstu(request):
    #初次访问
    if request.method == 'GET':
        iform = ImpStuForm()
        return render_to_response('accounts/upfiles.html', RequestContext(request, {'form': iform,}))
    #已经post提交数据
    else:
        iform = ImpStuForm(request.FILES)
        if iform.is_valid():
            createuser = request.user.username
            #filenickname = request.POST.get('filenickname', '')
            thefile = request.FILES.get('stufile', None)
            filepath = 'userfiles/upload/' + time.strftime('%Y/%m/%d/%H/%M/%S/')
            #filedescr = request.POST.get('filedescr', '')
            createddate = timezone.now()
            #将文件写入服务端硬盘
            handle_uploaded_file(thefile,str(thefile), filepath) 

    
            df = pd.read_excel(str(filepath)+str(thefile))
            #df = pd.read_excel(str(thefile))
            linecount = len(df.index)
            counti = range(linecount)

            imp_username = df['username']#导入的excel文件会自动添加行序号'0 1 2...'作为index
            imp_email = df['email']
            imp_password = df['password'] #是一个series,形式为'index0 value0 index1 value1 ...'


            for i in counti:
                i_name = imp_username[i] #以字典的键名来引用值
                i_email = imp_email[i]
                i_password = imp_password[i]
                #用户名是否被占用
                user = User.objects.filter(username=i_name)
                if user.count():
                    return render_to_response('accounts/message.html', RequestContext(request, {'words':'用户名被占用',})) 
                #用户名未被占用则创建用户
                user = User.objects.create_user( i_name, i_email, i_password )
                user.save()
                #用户扩展信息 profile  
                profile=UserProfile()#e*************************  
                profile.user_id=user.id  
                profile.phone=''
                profile.usergroup='is_student'  
                profile.save() 
                #用户信息写入 student  
                # stu = Student()#e*************************  
                # stu.user_id = user.id  
                # stu.username = i_name
                # stu.email = i_email
                # stu.password = i_password
                # stu.creater = createuser
                # stu.createddate = timezone.now()
                # stu.save()
            #添加成功
            return render_to_response('accounts/message.html', RequestContext(request, {'words':'导入用户成功',}))
        return render_to_response('accounts/message.html', RequestContext(request, {'words':'导入用户失败',}))
def handle_uploaded_file(file, filename, filepath):
    file_name = ""
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(filepath  + filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
    except :
        print('error') 
    return file_name






@permission_required('accounts.is_teacher', login_url="/")
def addtea(request):
    operator = request.user.username
    #初次访问
    if request.method == 'GET':
        regform = AddStuForm()
        return render_to_response('accounts/addstu.html', RequestContext(request, {'form': regform,}))
    #已经提交数据
    else:
        regform = AddStuForm(request.POST)
        if regform.is_valid():
            username = request.POST.get('username', '')
            password1 = request.POST.get('password1', '')
            password2 = request.POST.get('password2', '')
            usergroup = 'is_teacher'#默认以teacher角色
            email = ''
            phone = ''
            #用户名是否被占用
            user = User.objects.filter(username=username)
            if user.count():
                return render_to_response('accounts/addstu.html', RequestContext(request, {'form': regform,}))
            #注册成功
            user = User.objects.create_user( username, email, password1 )
            user.save()
            #用户扩展信息 profile  
            profile=UserProfile()#e*************************  
            profile.user_id=user.id  
            profile.phone=phone
            profile.usergroup=usergroup  
            profile.save()  
            #用户组是否存在
            group = Group.objects.filter(name=usergroup)
            groupperms = Permission.objects.get(codename=usergroup)
                                                #这里usergroup名字来自form要和权限里的对应上
            if not group.count():#如果用户组不存在则创建
                usergroup2 = Group.objects.create(name=usergroup)
                usergroup2.permissions.add(groupperms )#给组赋予权限
                usergroup2.save()

            #用户组存在,给用户赋予组和权限
            group = Group.objects.get(name=usergroup)
            user = User.objects.get(username=username)
            user.groups.add(group)#给用户赋予组
            user.user_permissions.add(groupperms)#给用户赋予组权限
            user.save()
            
            #添加成功
            return render_to_response('accounts/message.html', RequestContext(request, {'form': regform,'words':'添加成功',}))          
        else:
            return render_to_response('accounts/addstu.html', RequestContext(request, {'form': regform,}))


@permission_required('accounts.is_teacher', login_url="/")
def tealist(request):
    users = User.objects.all()
    stus = UserProfile.objects.filter(usergroup='is_teacher')
    userprof = UserProfile.objects.all()

    return render_to_response('accounts/stulist.html', RequestContext(request, {
        'users': users,
        'stus': stus,
        'userprof':userprof,
        }))



@login_required
def downtemplate(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    filename =  pp #超链接传递过来的文件名字
    if user is not None and user.is_active:        
        fpath = './examples/'+str( filename )+'.xls' #文件在根目录下的examples目录下，且名字就是超链接传递过来
        fname = str( filename)+'.xls'
        def readFile(fn, buf_size=262144):
            f = open(fn, "rb")
            while True:
                c = f.read(buf_size)
                if c:
                    yield c
                else:
                    break
            f.close()
        data = readFile(fpath)
        response = HttpResponse(data,content_type='application/octet-stream') 
        response['Content-Disposition'] = 'attachment; filename=%s' % fname
        return response