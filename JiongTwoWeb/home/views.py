from django.shortcuts import render, redirect, HttpResponse
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django import http
# from django.utils.translation import ugettext as _
from django.utils.timezone import now, timedelta
from datetime import datetime
import logging
import random
import json
import socket
import pytz
from home import models


# Create your views here.
logger = logging.getLogger("me")


def global_setting(req):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    SITE_AUTHOR = settings.SITE_AUTHOR
    MEDIA_URL = settings.MEDIA_URL

    return locals()


# class LogoutView(auth_views.LogoutView):
#     """
#     退出
#     """
#     def get(self, req, *args, **kwargs):
#         auth_logout(req)
#         return HttpResponseRedirect('/login')


# class LoginView(View):
#     """
#     登录
#     """
#     def get(self, req):
#         return render(req, 'login.html')
#
#     def post(self, req):
#         # 实例化
#         login_form = LoginForm(req.POST)
#         if login_form.is_valid():
#             # 获取用户提交的用户名和密码
#             # req.POST.get('username', '') 获取 username 如果不存在则指定默认值 ''
#             username = req.POST.get('username', '')
#             password = req.POST.get('password', '')
#             print('username：', username)
#             print('password：', password)
#
#             # 成功返回user对象,失败None
#             user = authenticate(username=username, password=password)
#             print(user)
#             # 如果不是null说明验证成功
#             if user is not None:
#                 if user.is_active:
#                     print('已激活，并且登录成功')
#                     # 登录
#                     login(req, user)
#                     return render(req, 'index.html', {'name': username})
#                 else:
#                     print('未激活，登录失败')
#                     return render(req, 'login.html', {'msg': '未激活，登录失败', 'login_form': login_form})
#             else:
#                 print('失败')
#                 return render(req, 'login.html', {'msg': '用户名或密码错误', 'login_form': login_form})
#         else:
#             return render(req, 'login.html', {'login_form': login_form})


# 登录校验
def my_view(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/login/?next=%s' % request.path)
    # ...


# 登录
def login(req):
    if req.method == 'GET':
        return render(req, 'login.html')
    else:
        res = {
            'code': -1,
            'flag': 'fail',
            'msg': '异常错误！',
            'data': None
        }
        # 接收参数
        username = req.POST.get('username', None)
        password = req.POST.get('password', None)

        # 验证
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(req, user)

                res['code'] = 0
                res['flag'] = 'success'
                res['msg'] = '登录成功！'
                res['data'] = None

                # 跳转到成功页面
                redirect(hot_list)
            else:
                res['code'] = 2
                res['flag'] = 'fail'
                res['msg'] = '登录失败！'
                res['data'] = None
        else:
            res['code'] = 1
            res['flag'] = 'fail'
            res['msg'] = '用户名或密码错误！'
            res['data'] = None

        return HttpResponse(json.dumps(res), content_type='application/json')


# 退出
def logout(req):
    logout(req)
    # 重定向到成功登出界面
    return render(req, 'login.html')


# 注册
def reg(req):
    return render(req, 'reg.html')


def send_code(req):
    phone = req.POST.get('phone', '')
    if phone == '':
        res = {
            'code': 1,
            'flag': 'fail',
            'msg': '手机号码不能为空！',
            'data': None
        }
        return HttpResponse(json.dumps(res), 'application/json')
    else:
        # 调用阿里云短信发送接口
        aliyun_res = send_sms(phone)
        if aliyun_res['code'] != 0:
            res = {
                'code': 2,
                'flag': 'fail',
                'msg': aliyun_res['msg'],
                'data': None
            }
            return HttpResponse(json.dumps(res), 'application/json')
        else:
            res = {
                'code': 0,
                'flag': 'success',
                'msg': aliyun_res['msg'],
                'data': aliyun_res['data']
            }
            return HttpResponse(json.dumps(res), 'application/json')


def send_sms(phone):
    res = {
        'code': 0,
        'flag': 'success',
        'msg': '验证码发送成功！',
        'data': phone[-6]
    }

    # res = {
    #     'code': 1,
    #     'flag': 'fail',
    #     'msg': '验证码发送失败！',
    #     'data': None
    # }
    return res


# 个人中心
def user(req, uid):
    return render(req, 'userinfo.html', locals())


# def set_language(req):
#     from django.utils.translation import check_for_language
#     next = req.REQUEST.get('next', None)
#
#     if not next:
#         next = req.META.get('HTTP_REFERER', None)
#     if not next:
#         next = '/'
#
#     response = http.HttpResponseRedirect(next)
#     if req.method == 'POST':
#         lang_code = req.POST.get('language', None)
#
#     if lang_code and check_for_language(lang_code):
#         if hasattr(req, 'session'):
#             req.session['django_language'] = lang_code
#
#         max_age = 60*60*24*365
#         expires = datetime.datetime.strftime(datetime.datetime.utctime() +
#         datetime.timedelta(seconds=max_age), "%a, %d-%b-%Y %H:%M:%S GMT")
#         response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang_code, max_age, expires)
#     return response


# 首页
def index(req):
    index = 0

    # water_qty_model = models.ChfWateringQty.objects.all()
    # if water_qty_model:
    #     water_qty = water_qty_model[0]
    # else:
    #     water_qty = models.ChfWateringQty()
    #
    # index_plate_list = models.ChfIndexPlate.objects.filter(is_enable=True)

    # return render(req, 'index.html', locals())

    return redirect(hot_list)


# 文章列表 - 热门
# @login_required
def hot_list(req):
    index = 1

    data_lists = models.JtArticle.objects.filter(is_enable=True).order_by('-like_count', '-read_count')[:50]
    paginator = Paginator(data_lists, 10, 2)
    page = req.GET.get('page')
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
        logger.error('传入的页码错误')
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
        logger.error('空页')

    # 按照时间取前10条
    data_lasted = models.JtArticle.objects.filter(is_enable=True).order_by('-create_time')[:10]

    return render(req, 'article_list.html', locals())


# 文章列表 - 神马
def new_list(req):
    index = 2

    # 取最近7天的数据

    data_lists = models.JtArticle.objects.filter(is_enable=True).order_by('-create_time')
    paginator = Paginator(data_lists, 10, 2)
    page = req.GET.get('page')
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
        logger.error('传入的页码错误')
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
        logger.error('空页')

    # 按照时间取前10条
    data_lasted = models.JtArticle.objects.filter(is_enable=True)[:10]

    return render(req, 'article_list.html', locals())


# 文章列表
def article_list(req, flag):

    template_name = "article_list.html"
    if flag == '0':
        index = 3  # 文字
    elif flag == '1':
        index = 4  # 图片
        template_name = "article_img.html"
    else:
        index = 5  # 视频
        template_name = "article_img.html"

    data_lists = models.JtArticle.objects.filter(type=flag, is_enable=True)
    paginator = Paginator(data_lists, 10, 2)
    page = req.GET.get('page')
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
        logger.error('传入的页码错误')
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
        logger.error('空页')

    data_lasted = models.JtArticle.objects.filter(type=0)[:10]

    return render(req, template_name, locals())


# 文章详情
def article_detail(req, id):
    index = 6
    path = 'hot'

    data_lists = models.JtArticle.objects.filter(is_enable=True).order_by('-like_count', '-read_count')
    paginator = Paginator(data_lists, 1, 1)
    page = req.GET.get('page')
    try:
        data_list = paginator.page(page)
    except PageNotAnInteger:
        data_list = paginator.page(1)
        logger.error('传入的页码错误')
    except EmptyPage:
        data_list = paginator.page(paginator.num_pages)
        logger.error('空页')

    try:
        if id:
            if page:
                article = data_list[0]
            else:
                article = models.JtArticle.objects.get(id=id)

            article.read_count += 1
            article.save()
    except Exception as e:
        logger.error(e)

    data_lasted = models.JtArticle.objects.all()[:10]

    return render(req, 'article_detail.html', locals())


# 关于我们
def about(req):
    index = 7

    # try:
    #     comp_about_models = models.ChfAbout.objects.filter(is_enable=True)
    #     if comp_about_models:
    #         comp_about_model = comp_about_models[0]
    #
    #         # 反向查找
    #         culture = comp_about_model.about_resource.filter(type_code=1)
    #         honor = comp_about_model.about_resource.filter(type_code=2)
    #         aptitude = comp_about_model.about_resource.filter(type_code=3)
    # except Exception as e:
    #     comp_about_model = models.ChfAbout()
    #     culture = []
    #     honor = []
    #     aptitude = []
    #     logger.error(e)
    #
    # comp_history_list = models.ChfCompanyHistory.objects.filter(is_enable=True)

    return render(req, 'about.html', locals())


# 联系我们
def contact(req):
    index = 8

    return render(req, 'contact.html', locals())


# 加入我们
def job(req):
    index = 9

    job_list = models.JtJob.objects.filter(is_enable=True)

    return render(req, 'job_list.html', locals())


# 用户协议
def user_protocol(req):
    index = 10
    job_list = models.JtJob.objects.filter(is_enable=True)
    return render(req, 'user_protocol.html', locals())


# 隐私政策
def privacy(req):
    index = 11
    job_list = models.JtJob.objects.filter(is_enable=True)
    return render(req, 'privacy.html', locals())


# 在线反馈
def feedback(req):
    index = 12
    job_list = models.JtJob.objects.filter(is_enable=True)
    return render(req, 'feedback.html', locals())


# 返回反馈结果
@login_required
def post_feedback(req):
    res = {}
    return HttpResponse(req, json.dumps(res))
