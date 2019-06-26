# -*- coding: utf-8 -*-

from django import forms
# from captcha.fields import CaptchaField


class LoginForm(forms.Form):
    """
    登录验证表单
    """
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=4)
