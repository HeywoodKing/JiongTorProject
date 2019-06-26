"""JiongTwoWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf import settings
# from django.conf.urls.i18n import i18n_patterns
from django.views.static import serve
from django.views.generic.base import RedirectView
from home import upload
from home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),

    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('reg/', views.reg, name='reg'),

    # path('jet/', include('jet.urls', 'jet')),  # Django JET URLS
    # path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS

    url(r'^uploads/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT, }),  # 单独上传图片后显示图片的url地址路径
    url(r'^admin/upload/(?P<dir_name>[^/]+)$', upload.upload_image, name='upload_image'),  # 富文本编辑器上传图片路径
    # url(r'^i18n/', include('django.conf.urls.i18n')),
    # url(r'^i18n/setlang', 'home.views.set_language'),
    url(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),
]

# urlpatterns += i18n_patterns(
#     url(r'^chf/', include('home.urls')),
# )
