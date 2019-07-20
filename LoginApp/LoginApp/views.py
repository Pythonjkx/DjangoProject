from django.shortcuts import render,HttpResponse
from django.http import HttpResponseRedirect,JsonResponse
import hashlib
from LoginApp1.models import *
# Create your views here.

# 加密
def setpassword(password):
    md5 = hashlib.md5()
    md5.update(password.encode())
    return md5.hexdigest()

# 验证
def register(request):
    result = {'content': ''}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password :
            user = User.objects.filter(username = username).first()
            if user:
                result['content'] = '用户名已存在'
            else:
                user = User()
                user.username = username
                user.password = setpassword(password)
                user.save()
                return HttpResponseRedirect('/login/')
        else:
            result['content'] = '用户名或者密码不能为空'

    return render(request, 'register.html',locals())

# 检查登录用户是否存在
def userValid(username):
    user = User.objects.filter(username = username).first()
    return user


# 登录
def login(request):
    result = {'content':''}
    if request.method == 'POST':
        user = request.POST.get('username')
        password = request.POST.get('password')
        if user and password:
            use = User.objects.filter(username = user).first()
            if use:
                if setpassword(password) == use.password:
                    res = HttpResponseRedirect('/index/')
                    res.set_cookie('username',use.username)
                    request.session['username'] = use.username #设置session
                    return res
                else:
                    result['content'] = '密码错误'
            else:
                result['content'] = '用户不存在'
        else:
            result['content'] = '用户名或密码不能为空'
    return render(request,'login.html',locals())


# 登录验证装饰器
def out(fun):
    def inner(request,*args,**kwargs):
        username = request.COOKIES.get('username')
        if username:
            user = User.objects.filter(username = username).first()
            if user:
                return fun(request,*args,**kwargs)
        return HttpResponseRedirect('/login/')
    return inner

@out
# 首页
def index(request):

    return render(request,"index.html",locals())

# 退出
def loginOut(request):
    h=HttpResponseRedirect('/login/')
    h.delete_cookie('username')
    return h


# ajax校验
def ajax(request):
    result = {'status':'error','content':''}
    username=request.GET.get('username')
    if username:
        user = userValid(username)
        if user:

            result['content'] = '用户名已存在'
        else:
            result['content'] = '用户名可以使用'
            result['status'] = 'success'
    else:
        result['content'] = '用户名不可为空'
    return JsonResponse(result)

