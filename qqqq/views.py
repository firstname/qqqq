# coding:utf-8
from django.shortcuts import render_to_response,render,get_object_or_404  
from django.http import HttpResponse, HttpResponseRedirect  
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User 
from django.contrib import messages
from django.template.context import RequestContext
from django.utils import timezone
import time
import os
import re
import pandas as pd
from qq.models import *
from accounts.models import *

# Create your views here.
def home(request):
    qnrss = QnRecord.objects.all().order_by('-taken_time')
    qnrs = qnrss[:2]
    qnss = Questionare.objects.all().order_by('-created_time')
    qns = qnss[:2]

    users = UserProfile.objects.all()
    stus = UserProfile.objects.filter(usergroup='is_student')
    teas = UserProfile.objects.filter(usergroup='is_teacher')
    return render_to_response("index.html", RequestContext(request, {
        'qnrss':qnrss,
        'qnss':qnss,
        'qnrs':qnrs,
        'qns':qns,

        'users':users,
        'stus':stus,
        'teas':teas,
         }))