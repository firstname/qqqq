#coding:utf-8
from django import forms
from django.forms import ModelForm

from .models import *


TOPIC_CHOICES = (
       ('questionare', '标准量表'),
       ('words', '文字反馈'),
       ('vote', '投票调查'),
)
FILE_FORMAT = (
       ('EXCEL', 'Excel格式'),
       ('TXT', 'Txt格式(暂不支持)'),
       ('CSV', 'CSV格式(暂不支持)'),
)
        
class QForm(ModelForm):
    # topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='量表类型')
    # file_format = forms.ChoiceField(choices=FILE_FORMAT,label='文件格式')
    #if_often = models.BooleanField(required=False ,label='加入常用')
    #if_homepage = models.BooleanField(required=False ,label='首页推荐')
    class Meta:
        model = Questionare
        fields = ('item_file', 'if_often','if_homepage',) #'title','desc','guidance','topic','file_format',
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"必填项没有填写")
        else:
            cleaned_data = super(QForm, self).clean()
        return cleaned_data

class StuLoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"密码",
        error_messages={'required': '请输入密码'},
        widget=forms.Textarea(
            attrs={
                'placeholder':u"密码",
            }
        ),
    ) 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        else:
            cleaned_data = super(StuLoginForm, self).clean()
        return cleaned_data
class RemarkForm(forms.Form):
        subject = forms.CharField(max_length=100 ,label='留言标题')
        mail = forms.EmailField(label='电子邮件')
        topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='选择评分')  
        message = forms.CharField(label='留言内容',widget=forms.Textarea)
        cc_myself = forms.BooleanField(required=False ,label='订阅该贴')


class QuestionUpForm(forms.Form):
    questionarename = forms.CharField(
        required=True,
        label=u"文件名",
        error_messages={'required': '请输入文件名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"文件名",
            }
        ),
    )
    filedescr = forms.CharField(
        required=True,
        label=u"文件描述",
        error_messages={'required': '请输入文件描述'},
        widget=forms.Textarea(
            attrs={
                'placeholder':u"文件描述",
            }
        ),
    ) 
    topic = forms.ChoiceField(choices=TOPIC_CHOICES,label='量表类型')       
    thefile = forms.FileField(required=False,label=u"选择文件")
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        else:
            cleaned_data = super(QuestionUpForm, self).clean()
        return cleaned_data


