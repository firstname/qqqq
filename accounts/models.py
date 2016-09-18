#coding:utf-8
from django.db import models
from django.contrib.auth.models import User,Group,Permission
import hashlib

# Create your models here.
#扩展用户信息          
class UserProfile(models.Model):  
    user=models.OneToOneField(User,unique=True,verbose_name=('自定义用户'))#和User关联  
    phone=models.CharField(u'电话号码',max_length=20)#电话号码
    usergroup=models.CharField(u'"老师"或"学生"',max_length=20,blank=True,null=True,default='is_student')#是学生还是老师 
    gradename = models.CharField(u'年级',max_length=30,blank=True,null=True)
    classname = models.CharField(u'班级',max_length=30,blank=True,null=True)
    schoolname = models.CharField(u'学校',max_length=30,blank=True,null=True)
    provincename = models.CharField(u'省份',max_length=30,blank=True,null=True)
    def __unicode__(self):
        return self.user

class UserGroups(models.Model):
    class Meta:  
        permissions = (
            ('is_student', u'具有学生权限'),  
            ('is_teacher', u'具有教师权限'),
 
        )


# 学生Student是独立存在的
# class Student(models.Model):
#     id = models.AutoField(primary_key=True)
#     #username = models.CharField(u'用户名',max_length=30)#不使用User
#     user = models.ForeignKey(User)#使用User
#     username = models.CharField(max_length=30,blank=True,null=True)
#     truename = models.CharField(max_length=30,blank=True,null=True)
#     classid = models.CharField(max_length=30,blank=True,null=True)
#     schoolid = models.CharField(max_length=30,blank=True,null=True)
#     province = models.CharField(max_length=30,blank=True,null=True)
#     email = models.EmailField(max_length=70,blank=True,null=True)
#     password = models.CharField(u'密码',max_length=30)
#     creater = models.CharField(max_length=30,blank=True,null=True)
#     createddate = models.DateField()
#     def __unicode__(self):
#         return self.username
    # def save(self,*args,**kwargs):
    #     self.password = hashlib.sha1(self.password+self.username).hexdigest()
    #     super(Student,self).save(*args,**kwargs)#密码加密
class StuGroup(models.Model):
    # id = models.AutoField(primary_key=True)
    groupname = models.FileField(blank=True,null=True)  
    members = models.ManyToManyField(User, through='Membership')#学生
    def __unicode__(self):
        return str(self.id)
class Membership(models.Model):
    # id = models.AutoField(primary_key=True)
    person = models.ForeignKey(User)
    group = models.ForeignKey(StuGroup)
    date_joined = models.DateField()
    invite_person = models.CharField(max_length=30)
