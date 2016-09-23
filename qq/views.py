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




@permission_required('accounts.is_teacher', login_url="/")
def upfiles(request):
    #初次访问
    if request.method == 'GET':
        iform = QForm()
        return render_to_response('qq/upfiles.html', RequestContext(request, {'form': iform,}))
    #已经post提交数据
    else:
        iform = QForm(request.POST,request.FILES)#从表单获取数据
        if iform.is_valid():
            creater = request.user.username
            # title = request.POST.get('title', '')
            # shortname = request.POST.get('short_name', '')
            # labels = request.POST.get('labels', '')
            # desc = request.POST.get('desc', '')
            # guidance = request.POST.get('guidance', '')
            # tips = request.POST.get('tips', '')
            often = request.POST.get('if_often', '')
            homepage = request.POST.get('if_homepage', '')
            createdtime = timezone.now()
            itemfile = request.FILES.get('item_file', None)
            filename = itemfile.name
            filepath = 'files/upload/' + time.strftime('%Y/%m/%d/%H/%M/%S/')

            df = pd.read_excel(itemfile,sheetname = 'basic')#读取问卷信息信息文件
            ind = df.index
            title = df.at[ind[0],'title']
            shortname = df.at[ind[0],'short_name']
            labels = df.at[ind[0],'keyword']
            desc = df.at[ind[0],'introduce']
            guidance = df.at[ind[0],'guidance']
            tips = df.at[ind[0],'tips']
                    

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
                    infile.short_name = shortname
                    infile.labels = labels 
                    infile.desc = desc
                    infile.guidance = guidance
                    infile.tips = tips 
                    infile.if_often = often
                    infile.if_homepage = homepage  
                    infile.created_time = createdtime 
                    #infile.item_file = itemfile #会将文件保存在根目录下
                    infile.file_path = filepath    
                    infile.file_name = filename   
                    infile.save()          
                    return render_to_response('qq/message.html', RequestContext(request, {'words':'上传成功!','urlname':'qlist'}))
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

    if thefile.if_stored == 'not':
        df1 = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'rule1')#读取维度包含题目信息文件
        ind1 = df1.index
        rows1 = len(df1.index)
        if rows1 > 0:
           for row1 in range(rows1):
            infile1 = Group()#保存每一个维度 
            infile1.g_order = df1.at[ind[row1],'id']
            infile1.g_name = df1.at[ind[row1],'sub_name']
            infile1.items = df1.at[ind[row1],'formula']
            infile1.qn_id = thefile
            infile1.qn_name = thefile.title
            infile1.save()

        df2 = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'trans1')#读取维度分数转换规则文件
        ind2 = df2.index
        rows2 = len(df2.index)
        if rows2 > 0:
           for row2 in range(rows2):
            infile2 = GpTrans()#保存每一个维度规则
            infile2.g_t_order = df2.at[ind[row2],'id']
            infile2.g_name = df2.at[ind[row2],'sub_name']
            infile2.up_limit = df2.at[ind[row2],'up_limit']
            infile2.low_limit = df2.at[ind[row2],'low_limit']
            infile2.score_transed = df2.at[ind[row2],'transed_score']
            infile2.gender = df2.at[ind[row2],'gender']
            infile2.up_age = df2.at[ind[row2],'up_age']
            infile2.low_age = df2.at[ind[row2],'low_age']
            infile2.qn_id = thefile
            infile2.qn_name = thefile.title
            infile2.save()

        df3 = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'interp1')#读取维度分数转换规则文件
        ind3 = df3.index
        rows3 = len(df3.index)
        if rows3 > 0:
           for row3 in range(rows3):
            infile3 = GpInterpret()#保存每一个维度规则
            infile3.g_i_order = df3.at[ind[rows3],'id']
            infile3.g_name = df3.at[ind[rows3],'sub_name']
            infile3.up_limit = df3.at[ind[rows3],'up_limit']
            infile3.low_limit = df3.at[ind[rows3],'low_limit']
            infile3.g_inter = df3.at[ind[rows3],'interpret']
            infile3.if_warn = df3.at[ind[rows3],'if_warn']
            infile3.qn_id = thefile
            infile3.qn_name = thefile.title
            infile3.save()

    
        df4 = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'rule2')#读取维度包含题目信息文件
        ind4 = df4.index
        rows4 = len(df4.index)
        if rows4 > 0:
           for row4 in range(rows4):
            infile4 = Group2()#保存每一个维度 
            infile4.g_order = df4.at[ind[row4],'id']
            infile4.g_name = df4.at[ind[row4],'sub_name']
            infile4.methods = df4.at[ind[row4],'methods']
            infile4.items = df4.at[ind[row4],'formula']
            infile4.qn_id = thefile
            infile4.qn_name = thefile.title
            infile4.save()

        df5 = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'trans2')#读取维度分数转换规则文件
        ind5 = df5.index
        rows5 = len(df5.index)
        if rows5 > 0:
           for row5 in range(rows5):
            infile5 = QnTrans()#保存每一个维度规则
            infile5.qn_t_order = df5.at[ind[row5],'id']
            infile5.up_limit = df5.at[ind[row5],'up_limit']
            infile5.low_limit = df5.at[ind[row5],'low_limit']
            infile5.score_transed = df5.at[ind[row5],'transed_score']
            infile5.gender = df5.at[ind[row5],'gender']
            infile5.up_age = df5.at[ind[row5],'up_age']
            infile5.low_age = df5.at[ind[row5],'low_age']
            infile5.qn_id = thefile
            infile5.qn_name = thefile.title
            infile5.save()

        df6 = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'interp2')#读取维度分数转换规则文件
        ind6 = df6.index
        rows6 = len(df6.index)
        if rows3 > 0:
           for row6 in range(rows6):
            infile6 = QnInterpret()#保存每一个维度规则
            infile6.qn_i_order = df6.at[ind[row6],'id']
            infile6.g_name = df6.at[ind[row6],'sub_name']
            infile6.up_limit = df6.at[ind[row6],'up_limit']
            infile6.low_limit = df6.at[ind[row6],'low_limit']
            infile6.g_inter = df6.at[ind[row6],'interpret']
            infile6.if_warn = df6.at[ind[row6],'if_warn']
            infile6.qn_id = thefile
            infile6.qn_name = thefile.title
            infile6.save()    

        df = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'question')#读取问题详细信息文件
        ind = df.index
        rows = len(df.index)
        columns = df.columns
        choicename = re.findall(r'choice+.',str(columns))
        choices = len(choicename)
        for row in range(rows):
            infile = Question()#保存每一道问题
            infile.qn_id = thefile #outkey of 'Question', must be a 'Question' instance
            infile.qn_name = thefile.title
            infile.q_order = df.at[ind[row],'id']
            infile.q_name = df.at[ind[row],'question']
            infile.g_name = df.at[ind[row],'group']
            infile.save()
            for choice in range(choices):
                inf = Option()#保存每一条选项
                inf.q_id = infile
                inf.q_name = infile.q_name
                inf.qn_id = infile.qn_id
                inf.qn_name = infile.qn_name
                oid = choice+1
                inf.o_order = oid 
                choicen = 'choice'+ str(oid)
                scoren = 'score'+ str(oid)
                inf.o_name = df.at[ind[row],choicen]
                inf.o_value = df.at[ind[row],scoren]
                inf.save()
        thefile.if_stored = 'yes'
        thefile.save()
        return render_to_response('qq/message.html', RequestContext(request, {'words':'发布问卷成功','urlname':'qlist'}))
    return render_to_response('qq/message.html', RequestContext(request, {'words':'该问卷已经发布过','urlname':'qlist'}))


               
  
@login_required
def preview(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        thefile = get_object_or_404(Questionare, pk=pp)
        fileread = pd.read_excel(str(thefile.file_path)+str(thefile.file_name),sheetname = 'question')
        filecolumn = fileread.columns
        question = fileread.loc[:,['id','question']]

        
        choicename = re.findall(r'choice+.',str(filecolumn))
        choicename.insert(0,'id')
        choice = fileread.loc[:,choicename]

        scorename = re.findall(r'score+.',str(filecolumn))
        scorename.insert(0,'id')
        score = fileread.loc[:,scorename]

        chsc = pd.merge(choice,score,on='id')

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



@permission_required('accounts.is_teacher', login_url="/")
def qlist(request):
    user = request.user
    qns = Questionare.objects.all().order_by('-created_time')
    qn = qns.filter(created_time__lte=timezone.now()).order_by('-created_time')#连字符“-”在“created_date”前表示降序排列。

    #检查是否已经存在该人的作答记录

    isrecord = QnRecord.objects.filter(taker_id_id=user.id)
  
    return render_to_response('qq/qlist.html', RequestContext(request, {
        'qns':qns,
        'isrecord':isrecord,
         }))

@login_required
def qview(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        qn = get_object_or_404(Questionare, pk=pp)
        qqs = Question.objects.filter(qn_id_id=qn.id)
        qqids = []
        for qq in qqs:
            qqid = int(qq.id)
            qqids.append(qqid)
        ops = Option.objects.filter(q_id_id__in=qqids)
        #检查是否已经存在该人的作答记录
        alreadytaken = 'no'
        isrecord = QnRecord.objects.filter(Q(taker_id=user), Q(qn_id=qn))
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
        qqs = Question.objects.filter(qn_id=qn.id)

    #已经post提交数据
    if request.method == 'POST': 
        #检查是否已经存在该人的作答记录
        alreadytaken = 'no'
        isrecord = QnRecord.objects.filter(taker_id=user)
        for rec in isrecord:
            #检查是否已经存在该问卷的作答记录
            if rec.qn_id == qn:
                alreadytaken = 'yes'
                return render_to_response('qq/message.html', RequestContext(request,
                     {'words':'您已经作答过该问卷','urlname':'javascript:history.go(-1)'}))
        for qq in qqs:
            qqid = qq.id
            op = request.POST.get('q'+ str(qqid), '')#获取input提交的各name(对应模板qview.html里的q{{qq.id}})的value,即题目的选项
            if not op : #搜索values里面的空值
                return render_to_response('qq/message.html', RequestContext(request,
                     {'words':'有题目漏选','urlname':'javascript:history.go(-1)'}))
        #计入问卷原始作答记录数据库
        qnr = QnRecord()
        qnr.taker_id = request.user
        qnr.taker_name = request.user.username
        qnr.taken_time = timezone.now()
        qnr.qn_id = qn
        qnr.qn_name = qn.title
        qnr.qn_score = 0
        qnr.save()

        for qq in qqs:
            qqid = qq.id
            op = request.POST.get('q'+ str(qqid), '')
             #获取选项和对应的值
            opt = Option.objects.get(Q(q_id=qq),Q(o_name=op))
            vl = opt.o_value
            #计入题目原始作答结果数据库
            qr = QResult()
            qr.qnr_id = qnr
            qr.taker_id = request.user
            qr.taker_name = request.user.username
            qr.taken_time = timezone.now()
            qr.q_id = qq
            qr.q_order = qq.q_order
            qr.q_name = qq.q_name
            qr.qn_id = qn
            qr.qn_name = qn.title
            qr.o_id = opt #opt is an instance of Option
            qr.o_name = opt.o_name
            qr.o_value = opt.o_value
            qr.save()
        
       
        qresult = QResult.objects.filter(qnr_id_id=qnr.id)
    return render_to_response('qq/result.html', RequestContext(request, 
            {'qn': qn,
            'qqs': qqs,
            'alreadytaken': alreadytaken,
            'op': op,

            'qnr': qnr,
            'qresult': qresult,
            }))

@login_required
def q_submit0(request,pp):#字典方法,没有数据库读写
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
def q_result(request,pp): #逐条展示原始的作答记录,而没有合成和转换
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        qn = get_object_or_404(Questionare, pk=pp)
        qqs = Question.objects.filter(qn_id=qn.id)

        #问卷作答记录
        qnr = QnRecord.objects.get(Q(qn_id=qn.id), Q(taker_id=user))

        qresult = QResult.objects.filter(qnr_id=qnr)
    return render_to_response('qq/result.html', RequestContext(request, 
            {'qn': qn,
            'qqs': qqs,
            
            'qnr': qnr,
            'qresult': qresult,
            }))



@permission_required('accounts.is_teacher', login_url="/")
def rlist(request):
    user = request.user
    qnrs = QnRecord.objects.all().order_by('-taken_time')

    #检查是否已经存在该人的作答记录

    isrecord = QnRecord.objects.filter(taker_id_id=user.id)
  
    return render_to_response('qq/rlist.html', RequestContext(request, {
        'qnrs':qnrs,
        'isrecord':isrecord,
         }))
@login_required
def rdelete(request,pp):
    generate_user = request.user.username
    #用户合法
    user = User.objects.get(username__exact= generate_user)
    if user is not None and user.is_active:
        rs = QnRecord.objects.filter(qn_id_id=pp)
        for r in rs:
            r.delete()
        # thefile.save()
        return render_to_response('qq/message.html', RequestContext(request, {'words':'删除成功','urlname':'rlist'}))


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


