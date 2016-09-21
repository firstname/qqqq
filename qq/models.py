# coding:utf-8
from django.db import models
from django import forms
from django.contrib.auth.models import User,Group,Permission
from accounts.models import *
import hashlib

# Create your models here.

# 问卷
class Questionare(models.Model):
    # id = models.AutoField(primary_key=True)
    creater = models.ForeignKey(User)
    title = models.CharField(u'名称*',max_length=2000,blank=False, null=True,)
    desc = models.TextField(u'简介',max_length=2000,blank=True, null=True)
    guidance = models.TextField(u'指导语',max_length=2000,blank=True, null=True)
    item_count = models.CharField(u'题目数',max_length=2000,blank=True, null=True,default = '0')
    sub_count = models.CharField(u'子维度数',max_length=2000,blank=True, null=True,default = '0')
    created_time = models.DateTimeField()
    item_file = models.FileField(u'上传*',blank=False,null=True)
    file_name = models.CharField(max_length=2000,blank=True, null=True)
    file_path = models.CharField(max_length=2000,blank=True, null=True)
    topic = models.CharField(max_length=2000,blank=True, null=True)
    file_format = models.CharField(max_length=2000,blank=True, null=True)
    if_stored = models.CharField(max_length=2000,blank=True, null=True,default = 'not')
    if_in_use = models.CharField(max_length=2000,blank=True, null=True,default = 'not')
    def __unicode__(self):
        return str(self.id)
class Question(models.Model):
    # id = models.AutoField(primary_key=True)
    q_order = models.CharField(max_length=2000,blank=True, null=True)# 在问卷内的题目序号
    q_name = models.CharField(max_length=2000,blank=True, null=True) 
    group = models.CharField(max_length=2000,blank=True, null=True) 
    qn_id = models.ForeignKey(Questionare)#大哥是问卷Questionare
    qn_name = models.CharField(max_length=2000,blank=True, null=True)   
    def __unicode__(self):
        return str(self.id)
class Option(models.Model):
    # id = models.AutoField(primary_key=True)
    o_order = models.CharField(max_length=2000,blank=True, null=True)# 在题目内的序号
    o_name = models.CharField(max_length=2000,blank=True, null=True)
    o_value = models.CharField(max_length=2000,blank=True, null=True) 
    q_id = models.ForeignKey(Question)#大哥是问题Question
    q_name = models.CharField(max_length=2000,blank=True, null=True)   
    qn_id = models.ForeignKey(Questionare)#大哥的大哥是问卷Questionare
    qn_name = models.CharField(max_length=2000,blank=True, null=True)#大哥的大哥
    def __unicode__(self):
        return str(self.id)


class QnRecord(models.Model):
    # id = models.AutoField(primary_key=True)#每个学生每做一次问卷记录一条
    taker_id = models.ForeignKey(User)#被试是从学生外键来的,一对一
    taker_name = models.CharField(max_length=2000,blank=True, null=True)
    taken_time = models.DateTimeField()
    #taskid = models.ForeignKey(QnTask)#任务
    qn_id = models.ForeignKey(Questionare)
    qn_name = models.CharField(max_length=2000,blank=True, null=True)
    qn_score = models.CharField(max_length=2000,blank=True, null=True,default = '')#问卷得分
    def __unicode__(self):
        return str(self.id)

class QResult(models.Model):
    # id = models.AutoField(primary_key=True)#每个选项记录一条
    o_id = models.ForeignKey(Option)#Option
    o_name = models.CharField(max_length=2000,blank=True, null=True)
    o_value = models.CharField(max_length=2000,blank=True, null=True) 
    q_id = models.ForeignKey(Question)#大哥是问题Question
    q_order = models.CharField(max_length=2000,blank=True, null=True)  
    q_name = models.CharField(max_length=2000,blank=True, null=True)   
    qn_id = models.ForeignKey(Questionare)#大哥的大哥是问卷Questionare
    qn_name = models.CharField(max_length=2000,blank=True, null=True)#大哥的大哥

    qnr_id = models.ForeignKey(QnRecord)#QnRecord  #大哥
    taker_id = models.ForeignKey(User)#被试是从学生外键来的,一对一
    taker_name = models.CharField(max_length=2000,blank=True, null=True)
    taken_time = models.DateTimeField()

    def __unicode__(self):
        return str(self.id)




#任务生成依赖于学生和问卷
class QnTask(models.Model):
    # id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=2000,blank=True, null=True)
    desc = models.CharField(max_length=2000,blank=True, null=True)
    created_time = models.DateTimeField()
    creater = models.CharField(max_length=2000,blank=True, null=True)
    start_time = models.DateTimeField(blank=True,null=True)
    end_time = models.DateTimeField(blank=True,null=True)
    comment = models.CharField(max_length=2000,blank=True,null=True)
    attachment = models.FileField(blank=True,null=True)
    taken_code = models.CharField(max_length=70,blank=True,null=True)#每次测试口令
    qn_id = models.CharField(max_length=2000,blank=True, null=True)#问卷
    stu_group = models.ForeignKey(StuGroup)#学生
    def __unicode__(self):
        return str(self.id)
    def save(self,*args,**kwargs):
        self.taken_code = hashlib.sha1(self.taken_code+self.title).hexdigest()
        super(Task,self).save(*args,**kwargs)#测试口令加密

