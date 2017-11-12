#coding:utf8
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.contrib import auth # 登录 推出 验证
from django.contrib.auth.models import User
import uuid
import datetime
import os
import models
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
import json
from common import Player



# Create your views here.
user_dict ={}
@login_required
def index(request):

    return render(request,'index.html')
def upload(request,file):#上传文件
    if file.size / 1024 / 1024 < 2: # 判断文件上传大小
        if file.content_type == 'image/jpeg' or file.content_type == 'image/gif': #判断文件类型
            # 把文件存到服务器上了
            new_name = str(uuid.uuid4()) + '.'+ file.name.split('.')[-1]
            fname = 'upload/head_pic/' + new_name
            dirname = os.path.dirname(fname) #获取路径名称

            if not os.path.exists(dirname): #如果不存在这个路径则创建
                os.makedirs(dirname) # 创建多级目录

            with open(fname,'wb') as f: # 写入方式打开
                if file.multiple_chunks(): # 多块文件
                    for chunk in file.chunks(): # 遍历文件的所有块
                        f.write(chunk)
                else: # 单块文件
                    f.write(file.read())
            return True,new_name
        else:
            return False,'文件类型只能是jpg或者gif' #返回False 和错误描述信息
    else:
        return False,'文件不能超过2M' #返回False 和错误描述信息

def reg(request):
    if request.method =="POST":
        username = request.POST.get('username',None)
        password1 = request.POST.get('password1',None)
        password2 = request.POST.get('password2',None)
        nick = request.POST.get('nick',None)
        head_pic = request.FILES.get('head_pic', None)


        if head_pic is not None:  # 如果文件不是None则获取文件对象成功
            res = upload(request, head_pic)  # 调用自己写的上传函数
            if res[0] is False:  # 如果上传失败则返回错误描述
                return render(request, 'user/reg.html', {'error': res[1]})
            else:
                new_name = res[1]
        else:
            return HttpResponse('没有获取图片')

        if username and password1 and password2:
            if password1 == password2:
                u_count = User.objects.filter(username=username).count()
                if u_count == 0:  # 没有这个用户名

                    # 添加自带用户表
                    user_info = {
                        'username': username,
                        'password': make_password(password1),
                    }
                    user_info = User.objects.create(**user_info)

                    # 添加用户扩展信息
                    user_profile = {
                        'nick': nick,
                        'headr_pic': 'head_pic/'+new_name,
                        'user': user_info
                    }

                    models.UserProfile.objects.create(**user_profile)

                    return HttpResponseRedirect('/login/')

                else:  # 用户名已存在
                    return render(request, 'user/reg.html', {'error': '用户名已存在'})
            else:
                return render(request, 'user/reg.html', {'error': '两次密码不一样'})

        else:
            return render(request, 'user/reg.html',{'error': '没有恍惚明或密码'})
    else:
        return render(request,'user/reg.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('uesrname', None)
        password = request.POST.get('password', None)
        if username and password:
            user = auth.authenticate(username=username, password=password)  # 如果验证成功返回用户对象，如果失败返回None
            if user is not None:
                if user.is_active:
                    # 做登陆操作
                    auth.login(request, user)
                    stuname = request.user.userprofile.nick

                    return HttpResponseRedirect('/')
                else:
                    return render(request, 'user/login.html', {'error': '账号已冻结'})
            else:
                return render(request, 'user/login.html', {'error': '用户名或密码错误'})
    else:
        return render(request, 'user/login.html')

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/login/')

def add_friends(request):
    if request.method == 'POST':

        friend_list = request.POST.getlist('friend_pk',None)
        me = request.user.userprofile


        for f_id in list(friend_list):
            fr = models.UserProfile.objects.get(pk = int(f_id))
            me.friends.add(fr)

        return HttpResponseRedirect('/')
    else:
        fids = [ftp[0] for ftp in request.user.userprofile.friends.all().values_list('id')]
        friends = models.UserProfile.objects.exclude(id__in=fids)
        stu_num = 5
        pn = request.GET.get('pn', 1)
        try:
            pn = int(pn)
        except Exception as e:
            pn = 1
        try:
            paginator = Paginator(friends, stu_num)  # 返回一个分页对象，p1:Queryset p2:每页记录条数
            users = paginator.page(pn)  # 获取某一页的记录
        except (InvalidPage, EmptyPage, PageNotAnInteger) as e:
            if e:
                pn = 1
                users = paginator.page(pn)


                # 分页数字生成
        num_pages = users.paginator.num_pages  # 总页数  由 Paginator 内部的函数生成===
        if num_pages < 5:

            page_nums = range(1, num_pages + 1)
        else:

            if pn - 2 <= 0:
                page_nums = range(1, 6)
            elif pn - 2 > 0 and pn + 3 <= num_pages:
                page_nums = range(pn - 2, pn + 3)
            else:
                page_nums = range(num_pages - 4, num_pages + 1)

        return render(request,'user_page.html',{'friends':users,'page_nums':page_nums})


def sendMsg(reuqest):
    data = reuqest.POST.get('data',None) # 接受前端传过来的json
    data = json.loads(data)  # 把json转成python字典
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') #获取服务器时间
    data['time'] = now
    to_id = int(data['to_id'])  #获取联系人的id
    if to_id not in user_dict: # 如果用户不再全局用户字典中则加入
        user_dict[to_id] = Player()
    try:
        user_dict[to_id].msg_q.put(data)  # 向用户字典中的对象的队列里加入一条消息
        # print user_dict
        # print user_dict[to_id].msg_q.get()
    except Exception,e:
        print e

    # print data,type(data)
    # 往用户字典里加入对象
    return HttpResponse('ok')

# 获取消息

def getMsg(request):
    uid = request.GET.get('uid',None) # 获取请求消息用户ID

    if uid is not None:
        uid = int(uid)
        if uid not in user_dict:  # 如果用户首次请求则建立用户实例
            user_dict[uid] = Player()
        try:
            msgs = user_dict[uid].getMsg() # 返回所有消息列表 [{from_id:111,to_id:111.....},{},{}]
            return HttpResponse(json.dumps(msgs))  # 响应一个json格式字符串
        except Exception,e:
            print str(e)
    else:
        return HttpResponse('get message error')  # 没有用户ID则返回错误信息