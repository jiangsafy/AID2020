from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import Liaotianuser


# Create your views here.
def reg_view(request):
    if request.method == 'GET':
        # 获取页面
        return render(request, 'user/register.html')
    elif request.method == 'POST':
        # 处理请求
        username = request.POST.get('username')
        password_1 = request.POST.get('password_1')
        password_2 = request.POST.get('password_2')
        # TODO 判断有没有
        print(username)
        # 判断username是否已经注册
        users = Liaotianuser.objects.filter(username=username)
        if users:
            # 用户已经注册
            return HttpResponse("用户已存在!!!")
        if password_1 != password_2:
            return HttpResponse("密码不一致，重新输入！！！")

        # hash md5 加密明文密码
        import hashlib
        m = hashlib.md5()
        m.update(password_1.encode())

        try:
            user = Liaotianuser.objects.create(username=username, password=m.hexdigest())
        except Exception as e:
            print('error')
            print(e)
            return HttpResponse('注册失败')

        # 注册成功
        resp = render(request,'tiao.html',locals())

        resp.set_cookie('username', username, 3600 * 24)
        resp.set_cookie('uid', user.id, 3600 * 24)
        return resp



def login_view(request):
    # 登录处理
    if request.method == "GET":
        # 优先检查 session
        if request.session.get('uid') and request.session.get('username'):
            return render(request,'chat.html',locals())

        uid = request.COOKIES.get('uid')
        username = request.COOKIES.get('username')

        if uid and username:
            # 证明用户之前点过checkbox
            # 回写session
            request.session['uid'] = uid
            request.session['username'] = username
            # return HttpResponse('你登录过')
            return render(request,"chat.html")

        return render(request, 'user/login.html')
    elif request.method == "POST":
        # 处理数据
        username = request.POST.get('username')

        password = request.POST.get('password')

        old_users = Liaotianuser.objects.filter(username=username)

        if not old_users:
            return HttpResponse('---用户错误---')

        # 校验密码
        import hashlib
        m = hashlib.md5()
        m.update(password.encode())

        user = old_users[0]

        if user.password != m.hexdigest():
            # 密码错误
            return HttpResponse('---用户密码错误---')
        # 保存登录状态
        # 1 存 session

        request.session['uid'] = user.id
        request.session['username'] = username

        # 2, 检查是否要存cookies
        # resp = HttpResponseRedirect('/')

        resp = render(request,"tiao.html")

        if 'isSaved' in request.POST.keys():
            # 用户勾选了 下次免登陆
            resp.set_cookie('uid', user.id, 3600 * 24 * 30)

            resp.set_cookie('uid', user.id, 3600 * 24 * 30)

        # 保存登录状态

        return resp
        # isSaved = request.POST.get("isSaved")
        # print('-----')
        # print(request.POST.keys())
        # print(isSaved)
        # return HttpResponse('--text--')


def logout(request):
    # 登录
    # 删除 session
    # 删除 Cookies
    if 'uid' in request.session:
        del request.session['uid']
    if 'username' in request.session:
        del request.session['username']

    # 删除 Cookies
    resp = HttpResponse("--已经登出")

    if 'uid' in request.COOKIES:
        resp.delete_cookie('uid')
    if 'username' in request.COOKIES:
        resp.delete_cookie('username')
    return resp
