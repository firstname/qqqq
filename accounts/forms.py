#coding:utf-8
from django import forms
from django.contrib.auth.models import User
#from bootstrap_toolkit.widgets import BootstrapDateInput, BootstrapTextInput, BootstrapUneditableInput

USER_GROUPS = (
       ('is_student', '学生'),
       ('is_teacher', '老师'),
       ('is_other', '其他'),
)
class LoginForm(forms.Form):
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
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码",
            }
        ),
    ) 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"用户名和密码为必填项")
        else:
            cleaned_data = super(LoginForm, self).clean()


def validate_phone(value):
    if not value.isdigit():
        raise forms.ValidationError(u'%s不是电话号码' % value)
def validate_user(username):
    user = User.objects.filter(username=username)
    if user.count():
        raise forms.ValidationError(u'%s已经被注册' % username)
def validate_psw(value):
    if len(value) < 6:
        raise forms.ValidationError(u'密码长度不够' )

class RegisterForm(forms.Form):
    username = forms.CharField(
        required=True,validators=[validate_user],
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名,必填",
            }
        )
    )    
    password1 = forms.CharField(
        required=True,validators=[validate_psw],
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码,必填,长度6位以上的数字、字符",
            }
        ),
    )  
    password2 = forms.CharField(
        required=True,validators=[validate_psw],
        label=u"密码确认",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码,必填",
            }
        ),
    ) 
    email = forms.CharField(
        required=False,
        label=u"电子邮件",
        error_messages={'required': u'请输入电子邮件地址'},
        widget=forms.EmailInput(
            attrs={
                'placeholder':u"电子邮件,选填",
            }
        ),
    )  
    phone = forms.CharField(
        required=False,validators=[validate_phone],
        label=u"电话号码",
        error_messages={'required': u'请输入电话号码'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"电话号码,选填",
            }
        ),
    ) 
    #usergroup = forms.ChoiceField(choices=USER_GROUPS,label='用户类型') 
    #不做选择,默认以学生身份注册;管理员可以修改userprofile将用户改为教师类型
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        elif len(self.cleaned_data['password1']) < 6 or len(self.cleaned_data['password2']) < 6:
            raise forms.ValidationError(u"密码长度不够,必须大于6位")
        elif self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(u"两次输入的密码不一样")
        else:
            cleaned_data = super(RegisterForm, self).clean()
        return cleaned_data


class PasswordForm(forms.Form):
    oldpassword = forms.CharField(
        required=True,
        label=u"原密码",
        error_messages={'required': u'请输入原密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"原密码",
            }
        ),
    ) 
    newpassword1 = forms.CharField(
        required=True,
        label=u"新密码",
        error_messages={'required': u'请输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"新密码",
            }
        ),
    )
    newpassword2 = forms.CharField(
        required=True,
        label=u"确认密码",
        error_messages={'required': u'请再次输入新密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码",
            }
        ),
    ) 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"所有项都为必填项")
        elif len(self.cleaned_data['newpassword1']) < 6 or len(self.cleaned_data['newpassword2']) < 6:
            raise forms.ValidationError(u"新密码长度不够,必须大于6位")
        elif self.cleaned_data['newpassword1'] != self.cleaned_data['newpassword2']:
            raise forms.ValidationError(u"两次输入的新密码不一样")
        else:
            cleaned_data = super(PasswordForm, self).clean()
        return cleaned_data


class AddStuForm(forms.Form):
    username = forms.CharField(
        required=True,validators=[validate_user],
        label=u"用户名",
        error_messages={'required': '请输入用户名'},
        widget=forms.TextInput(
            attrs={
                'placeholder':u"用户名,必填",
            }
        )
    )    
    password1 = forms.CharField(
        required=True,validators=[validate_psw],
        label=u"密码",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"密码,必填,长度6位以上的数字、字符",
            }
        ),
    )  
    password2 = forms.CharField(
        required=True,validators=[validate_psw],
        label=u"密码确认",
        error_messages={'required': u'请输入密码'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder':u"确认密码,必填",
            }
        ),
    ) 
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        elif len(self.cleaned_data['password1']) < 6 or len(self.cleaned_data['password2']) < 6:
            raise forms.ValidationError(u"密码长度不够,必须大于6位")
        elif self.cleaned_data['password1'] != self.cleaned_data['password2']:
            raise forms.ValidationError(u"两次输入的密码不一样")
        else:
            cleaned_data = super(AddStuForm, self).clean()
        return cleaned_data

class ImpStuForm(forms.Form):
    stufile = forms.FileField(required=False,label=u"选择excel文件,请确保有username,email(可以为空),password三个字段")
    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"错误")
        else:
            cleaned_data = super(ImpStuForm, self).clean()
        return cleaned_data