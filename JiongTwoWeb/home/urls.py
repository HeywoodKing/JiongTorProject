# !-*- coding: utf-8 -*-
# @Author  : ching(opencoding@hotmail.com)
# @Date    : 2019/05/02
# @Link    : www.cnblogs.com/ching126/ or blog.csdn.net/chenhongwu666
# @Version : 
# @Desc    :

from django.urls import path
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from home import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index/', views.index, name='index'),
    path('home/', views.index, name='index'),

    path('about/', views.about, name='about'),
    path('job/', views.job, name='job'),
    path('contact/', views.contact, name='contact'),

    path('user_protocol/', views.user_protocol, name='user_protocol'),
    path('privacy/', views.privacy, name='privacy'),
    path('feedback/', views.feedback, name='feedback'),

    path('send_code/', views.send_code, name='send_code'),

    url(r'^text/(?P<flag>\d+)/$', views.article_list, name='text'),
    url(r'^img/(?P<flag>\d+)/$', views.article_list, name='img'),
    url(r'^video/(?P<flag>\d+)/$', views.article_list, name='video'),

    url(r'^hot/$', views.hot_list, name='hot'),
    url(r'^new/$', views.new_list, name='new'),
    url(r'^detail/(?P<id>\d+)/$', views.article_detail, name='detail'),
    # url(r'^next/$', views.article_next_detail, name='next'),

    url(r'^user/(?P<uid>\d+)/$', views.user, name='user'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
