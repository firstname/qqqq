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

# Create your views here.
def home(request):
    return render_to_response("index.html", RequestContext(request, { }))

