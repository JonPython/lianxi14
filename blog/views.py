from django import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, redirect
from .models import *

# Create your views here.
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密　码',widget=forms.PasswordInput())


def index(request):
    return render(request,'index.html')


def regist(request):
    if request.method == 'POST':
        uf = UserForm(request.POST)#包括用户及密码
        if uf.is_valid():

            # 获取表单内容
            username = uf.cleaned_data['username']#cleaned_data 类型是字典
            password = uf.cleaned_data['password']

            # 添加到数据库
            registAdd = User.objects.create_user(username=username,password=password)

            if registAdd == False:
                return render(request,'share.html',locals())

            else:

                return render(request,'share.html',{'registAdd':registAdd})

    else:
        uf = UserForm()

    return render(request,'regist.html',{'uf':uf})


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username,password)
        re = auth.authenticate(username=username,password=password)#用户认证
        if re is not None:
            auth.login(request,re)
            return redirect('/article',{'user':re})#跳转
        else:
            return render(request,'login.html',{'login_error':'用户名或密码错误'})
    return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return render(request,'index.html')

def article(request):
    article_list = Article.objects.all()

    return render(request,'article.html',{'article_list':article_list})

def detail(request,id):
    try:
        article = Article.objects.get(id=id)
    except Article.DoesNotExist:
        raise Http404
    return render(request,'detail.html',locals())