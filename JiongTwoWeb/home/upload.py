# !-*- coding: utf-8 -*-
# @Author  : ching(flackmaster@163.com)
# @Date    : 2019/03/16
# @Link    : http://www.cnblogs.com/ching126/
# @Version : $
# @Desc    :

from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import os
import uuid
import json
import datetime as dt


@csrf_exempt
def upload_image(req, dir_name):
    ##################
    # kindeditor图片上传返回数据格式说明：
    # {"error": 1, "message": "出错信息"}
    # {"error": 0, "url": "图片地址"}
    ##################
    result = {"error": 1, "message": "上传出错"}
    files = req.FILES.get("imgFile", None)
    if files:
        result = do_upload_image(files, dir_name)
    return HttpResponse(json.dumps(result), content_type="application/json")


# 目录创建
def upload_generation_dir(dir_name):
    today = dt.datetime.today()
    dir_name = dir_name + '/%s/%s/' % (str(today.year), today.strftime('%m'))

    if not os.path.exists(settings.MEDIA_ROOT + '/' + dir_name):
        os.makedirs(settings.MEDIA_ROOT + '/' + dir_name)
    return dir_name


# 图片上传
def do_upload_image(files, dir_name):
    # 允许上传文件类型
    allow_suffix = ['jpg', 'png', 'jpeg', 'gif', 'bmp']
    file_suffix = files.name.split(".")[-1]
    if file_suffix not in allow_suffix:
        return {"error": 1, "message": "图片格式不正确"}
    relative_path_file = upload_generation_dir(dir_name)
    path = os.path.join(settings.MEDIA_ROOT, relative_path_file)
    if not os.path.exists(path):  # 如果目录不存在创建目录
        os.makedirs(path)
    file_name = str(uuid.uuid1())+"."+file_suffix
    path_file = os.path.join(path, file_name)
    file_url = settings.MEDIA_URL + relative_path_file + file_name

    open(path_file, 'wb').write(files.file.read())  # 保存图片
    return {"error": 0, "url": file_url}
