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
from django.db.models import Q
import time
import os
import re
import pandas as pd
import numpy as np

from .models import *
from .forms import *

# Create your views here.
# def home(request):
#     return render_to_response("qq/qindex.html", RequestContext(request, { }))

@login_required
def tlist(request):
    username = request.user.username
    operater = User.objects.get(username=username)
    if operater.has_perm('accounts.is_teacher',):#只有teacher有查看全部task的权限
        alltasks = QnTask.objects.all().filter(createdtime__lte=timezone.now()).order_by('-createdtime')#连字符“-”在“created_date”前表示降序排列。
        createdtasks = QnTask.objects.all().filter(creater=username)#个人所创建的task
    #学生被指派的task
    #由个人username获取User.pk
    #由User.pk获取Student.pk
    #由Student.pk获取Membership.pk
    #由Membership.pk获取StuGroup.pk
    #由StuGroup.pk获取QnTask.pk
    orderedtask = stutasks.filter(createdtime__lte=timezone.now()).order_by('-createdtime')#连字符“-”在“created_date”前表示降序排列。 
    return render_to_response('qq/tlist.html', RequestContext(request, {'alltsks':alltasks,
        'createdtasks':createdtasks }))

@permission_required('accounts.is_teacher', login_url="/")
def qlist(request):
    user = request.user
    qns = Questionare.objects.all().order_by('-createdtime')
    qn = qns.filter(createdtime__lte=timezone.now()).order_by('-createdtime')#连字符“-”在“created_date”前表示降序排列。

    #检查是否已经存在该人的作答记录

    isrecord = QnRecord.objects.filter(takerid_id=user.id)
  
    return render_to_response('qq/qlist.html', RequestContext(request, {
        'qns':qns,
        'isrecord':isrecord,
         }))

@permission_required('accounts.is_teacher', login_url="/")
def upfiles(request):
    #初次访问
    if request.method == 'GET':
        iform = QForm()
        return render_to_response('qq/upfiles.html', RequestContext(request, {'form': iform,}))
    #已经post提交数据
    else:
        iform = QForm(request.POST,request.FILES)
        if iform.is_valid():
            creater = request.user.username
            title = request.POST.get('title', '')
            desc = request.POST.get('desc', '')
            guidance = request.POST.get('guidance', '')
            itemcount = request.POST.get('itemcount', '')
            subcount = request.POST.get('subcount', '')
            createdtime = timezone.now()
            itemfile = request.FILES.get('itemfile', None)
            filename = itemfile.name
            filepath = 'files/upload/' + time.strftime('%Y/%m/%d/%H/%M/%S/')
            topic = request.POST.get('topic', '')  
            fileformat = request.POST.get('fileformat', '')                      

            #检查用户合法性
            user = User.objects.get(username__exact= creater)
            if user is not None and user.is_active:  
                #将文件写入服务端硬盘
                handle_uploaded_file(itemfile,str(itemfile), filepath) 
                #先写文件再计入数据库,否则文件上传失败也会在数据库里有一条文件记录.
                #检查量表名称是否重复
                qnname = Questionare.objects.filter(title__exact= title)
                if qnname.count() == 0:
                    #写入Questionare数据库
                    infile = Questionare()
                    infile.creater = user
                    infile.title = title
                    infile.desc = desc
                    infile.guidance = guidance
                    infile.itemcount = itemcount 
                    infile.subcount = subcount 
                    infile.createdtime = createdtime 
                    #infile.itemfile = itemfile #会将文件保存在根目录下
                    infile.filepath = filepath    
                    infile.filename = filename
                    infile.topic = topic
                    infile.fileformat = fileformat    
                    infile.save()          
                    return render_to_response('qq/message.html', RequestContext(request, {'words':'上传成功','urlname':'qlist'}))
                else:
                    return render_to_response('qq/message.html', RequestContext(request, {'words':'量表名称已经存在','urlname':'upfiles'}))            
            else:#用户不合法
                return render_to_response('qq/upfiles.html', RequestContext(request, {'form': iform,'some_wrong':True}))
        else:#表单不合法
            return render_to_response('qq/upfiles.html', RequestContext(request, {'form': iform,}))
def handle_uploaded_file(file, filename, filepath):
    file_name = ""
    try:
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        with open(filepath  + filename, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
            destination.close()
    except Exception as error:
        print('error') 
    return file_name
def qstore(request,pp):
    thefile = get_object_or_404(Questionare, pk=pp)
    title = thefile.title

    df = pd.read_excel(str(thefile.filepath)+str(thefile.filename))
    ind = df.index
    rows = len(df.index)
    columns = df.columns
    choicename = re.findall(r'choice+.',str(columns))
    choices = len(choicename)

    if thefile.ifstored == 'not':
        for row in range(rows):
            infile = Question()
            infile.qnid = thefile #outkey of 'Question', must be a 'Question' instance
            infile.qid = df.at[ind[row],'ID']
            infile.question = df.at[ind[row],'question']
            infile.group = df.at[ind[row],'group']
            infile.save()
            for choice in range(choices):
                inf = Option()
                inf.qid = infile
                oid = choice+1
                inf.oid = oid 
                choicen = 'choice'+ str(oid)
                scoren = 'score'+ str(oid)
                inf.option = df.at[ind[row],choicen]
                inf.value = df.at[ind[row],scoren]
                inf.save()
        thefile.ifstored = 'yes'
        thefile.save()
        return render_to_response('qq/message.html', RequestContext(request, {'words':'保存成功','urlname':'qlist'}))
    return render_to_response('qq/message.html', RequestContext(request, {'words':'该问卷已经保存过,如果要修改,请重新上出修改后的文件','urlname':'qlist'}))


               
  
@login_required
def preview(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        thefile = get_object_or_404(Questionare, pk=pp)
        fileread = pd.read_excel(str(thefile.filepath)+str(thefile.filename))
        filecolumn = fileread.columns
        question = fileread.loc[:,['ID','question']]

        
        choicename = re.findall(r'choice+.',str(filecolumn))
        choicename.insert(0,'ID')
        choice = fileread.loc[:,choicename]

        scorename = re.findall(r'score+.',str(filecolumn))
        scorename.insert(0,'ID')
        score = fileread.loc[:,scorename]

        chsc = pd.merge(choice,score,on='ID')

        filet = fileread.T
        questiont = question.T
        choicet = choice.T
        scoret = score.T
        chsct = chsc.T
                
        return render_to_response('qq/preview.html', RequestContext(request, 
            {'thefile': thefile,
            'fileread': fileread,
            'filecolumn': filecolumn,
            'choicename': choicename,
            'scorename': scorename,
            #'idname': idname,
            'choice': choice,
            'question': question,
         
            'filet': filet,
            'choicet': choicet,
            'questiont': questiont,
            'scoret': scoret,

            'chsc': chsc,
            }))

@login_required
def qview(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        qn = get_object_or_404(Questionare, pk=pp)
        qqs = Question.objects.filter(qnid_id=qn.id)
        qqids = []
        for qq in qqs:
            qqid = int(qq.id)
            qqids.append(qqid)
        ops = Option.objects.filter(qid_id__in=qqids)
        #检查是否已经存在该人的作答记录
        alreadytaken = 'no'
        isrecord = QnRecord.objects.filter(Q(takerid=user), Q(qnid=qn))
        if isrecord.count():
                alreadytaken = 'yes'
        # for rec in isrecord:
        #     #检查是否已经存在该人该问卷的作答记录
        #     if rec.qnid == qn:
        #         alreadytaken = 'yes'
        return render_to_response('qq/qview.html', RequestContext(request, 
            {'qn': qn,
            'qqs': qqs,
            'ops': ops,
            'isrecord': isrecord,
            'qqids': qqids,
            'alreadytaken': alreadytaken,
            }))

@login_required
def q_submit(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        qn = get_object_or_404(Questionare, pk=pp)
        qqs = Question.objects.filter(qnid=qn.id)

    #已经post提交数据
    if request.method == 'POST': 
        #检查是否已经存在该人的作答记录
        alreadytaken = 'no'
        isrecord = QnRecord.objects.filter(takerid=user)
        for rec in isrecord:
            #检查是否已经存在该问卷的作答记录
            if rec.qnid == qn:
                alreadytaken = 'yes'
                return render_to_response('qq/message.html', RequestContext(request,
                     {'words':'您已经作答过该问卷','urlname':'javascript:history.go(-1)'}))
        for qq in qqs:
            qqid = qq.id
            op = request.POST.get('q'+ str(qqid), '')#获取input提交的各name(对应模板里的q{{qq.id}})的value,即题目的选项
            if not op : #搜索values里面的空值
                return render_to_response('qq/message.html', RequestContext(request,
                     {'words':'有题目漏选','urlname':'javascript:history.go(-1)'}))
        #计入问卷作答记录数据库
        qnr = QnRecord()
        qnr.takerid = request.user
        qnr.taketime = timezone.now()
        qnr.qnid = qn
        qnr.save()
        for qq in qqs:
            opts = Option.objects.filter(qid_id=qq.id)
            for opt in opts:
                if opt.option == op:
                    #计入题目作答结果数据库
                    qr = QResult()
                    qr.qnrid = qnr
                    qr.qid = qq
                    qr.opt = opt #opt is an instance of Option
                    qr.save()
        qresult = QResult.objects.filter(qnrid_id=qnr.id)
    return render_to_response('qq/result.html', RequestContext(request, 
            {'qn': qn,
            'qqs': qqs,
            'alreadytaken': alreadytaken,
            'op': op,

            'qnr': qnr,
            'qresult': qresult,
            }))


@login_required
def q_submit0(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        thefile = get_object_or_404(Questionare, pk=pp)
        fileread = pd.read_excel(str(thefile.filepath)+str(thefile.filename))
        filecolumn = fileread.columns
        filet = fileread.T

        choicename = re.findall(r'choice+.',str(filecolumn))
        choicedf = fileread.loc[:,choicename]
        choicet = choicedf.T
        #choicecount = len(choicename)
        scorename = re.findall(r'score+.',str(filecolumn))
        scoredf = fileread.loc[:,scorename]
        scoret = scoredf.T      

    answer = {}
    score = {}
    #已经post提交数据
    if request.method == 'POST':        
        for kk,vv in filet.items(): 
            ans = request.POST.get('key'+ str(kk), '')#获取input提交的各name的value,是一个选项                                    
            if not ans : #搜索values里面的空值
                return render_to_response('qq/message.html', RequestContext(request,
                     {'words':'有题目漏选','urlname':'javascript:history.go(-1)'}))
            answer[kk] = ans #更新字典记录所选项

            chline = choicet[kk].tolist() #选择第kk行,转换成list
            chp = chline.index(ans)#提交的选项在这一行的位置

            scline = scoret[kk].tolist() 
            sc = scline[chp] #对应位置的分数就是该选项应得分数
            score[kk] = sc #更新字典记录分数

    return render_to_response('qq/q_result.html', RequestContext(request, 
            {'thefile': thefile,
            'filet': filet,
            'answer': answer,

            'score': score,
            'scoret': scoret,
            'choicet': choicet,
            }))



@login_required
def qdelete(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        thefile = get_object_or_404(Questionare, pk=pp)
        thefile.delete()
        # thefile.save()
        return render_to_response('qq/message.html', RequestContext(request, {'words':'删除成功','urlname':'qlist'}))



@login_required
def q_result(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        qn = get_object_or_404(Questionare, pk=pp)
        qqs = Question.objects.filter(qnid=qn.id)

        #问卷作答记录
        qnr = QnRecord.objects.filter(Q(qnid=qn.id), Q(takerid=user))

        qresult = QResult.objects.filter(qnrid=qnr)
    return render_to_response('qq/result.html', RequestContext(request, 
            {'qn': qn,
            'qqs': qqs,
            
            'qnr': qnr,
            'qresult': qresult,
            }))







