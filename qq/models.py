# coding:utf-8
from django.db import models
from django import forms
from django.contrib.auth.models import User,Group,Permission
from accounts.models import *
import hashlib

# Create your models here.

TOPIC_CHOICES = (
       ('leve1', '标准量表'),
       ('leve2', '填写问卷'),
       ('leve3', '投票调查'),
)
# 问卷Questionare是独立存在的
class Questionare(models.Model):
    # id = models.AutoField(primary_key=True)
    creater = models.ForeignKey(User)
    title = models.CharField(u'名称*',max_length=2000,blank=False, null=True,)
    desc = models.TextField(u'简介',max_length=2000,blank=True, null=True)
    guidance = models.TextField(u'指导语',max_length=2000,blank=True, null=True)
    itemcount = models.CharField(u'题目数',max_length=2000,blank=True, null=True,default = '0')
    subcount = models.CharField(u'子维度数',max_length=2000,blank=True, null=True,default = '0')
    createdtime = models.DateTimeField()
    itemfile = models.FileField(u'上传题目*',blank=False,null=True)
    filename = models.CharField(max_length=2000,blank=True, null=True)
    filepath = models.CharField(max_length=2000,blank=True, null=True)
    #topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='量表类型')
    topic = models.CharField(max_length=2000,blank=True, null=True)
    fileformat = models.CharField(max_length=2000,blank=True, null=True)
    ifstored = models.CharField(max_length=2000,blank=True, null=True,default = 'not')
    ifinuse = models.CharField(max_length=2000,blank=True, null=True,default = 'not')
    def __unicode__(self):
        return str(self.id)
    # class Meta:
    #     permissions = (
    #         ("view_qn", "Can see available questionares"),
    #         ("change_qn_status", "Can change the status of questionares"),
    #         ("close_qn", "Can remove a questionare by setting its status as closed"),
    #     )

class Question(models.Model):
    # id = models.AutoField(primary_key=True)
    qnid = models.ForeignKey(Questionare)#大哥是问卷Questionare
    qid = models.CharField(max_length=2000,blank=False, null=True) 
    question = models.CharField(max_length=2000,blank=True, null=True) 
    group = models.CharField(max_length=2000,blank=True, null=True)   
    def __unicode__(self):
        return str(self.id)
class Option(models.Model):
    # id = models.AutoField(primary_key=True)
    qid = models.ForeignKey(Question)#大哥是问题Question
    oid = models.CharField(max_length=2000,blank=False, null=True) 
    option = models.CharField(max_length=2000,blank=True, null=True)
    value = models.CharField(max_length=2000,blank=True, null=True)   
    def __unicode__(self):
        return str(self.id)

#任务生成依赖于学生和问卷
class QnTask(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=2000,blank=True, null=True)
    desc = models.CharField(max_length=2000,blank=True, null=True)
    createdtime = models.DateTimeField()
    creater = models.CharField(max_length=2000,blank=True, null=True)
    starttime = models.DateTimeField(blank=True,null=True)
    endtime = models.DateTimeField(blank=True,null=True)
    comment = models.CharField(max_length=2000,blank=True,null=True)
    attachment = models.FileField(blank=True,null=True)
    takencode = models.CharField(max_length=70,blank=True,null=True)#每次测试口令
    qnid = models.CharField(max_length=2000,blank=True, null=True)#问卷
    stugroup = models.ForeignKey(StuGroup)#学生
    def __unicode__(self):
        return str(self.id)
    def save(self,*args,**kwargs):
        self.takencode = hashlib.sha1(self.takencode+self.title).hexdigest()
        super(Task,self).save(*args,**kwargs)#测试口令加密


class QnRecord(models.Model):
    # id = models.AutoField(primary_key=True)#每个学生每做一次问卷记录一条
    takerid = models.ForeignKey(User)#被试是从学生外键来的,一对一
    taketime = models.DateTimeField()
    #taskid = models.ForeignKey(QnTask)#任务
    qnid = models.ForeignKey(Questionare)
    #qnscore = models.CharField(max_length=2000,blank=True, null=True)#问卷得分
    def __unicode__(self):
        return str(self.id)

class QResult(models.Model):
    # id = models.AutoField(primary_key=True)#每条题目被提交一次则记录一条
    qnrid = models.ForeignKey(QnRecord)#QnRecord
    qid = models.ForeignKey(Question)#Question
    opt = models.ForeignKey(Option)#Question

    def __unicode__(self):
        return str(self.id)


