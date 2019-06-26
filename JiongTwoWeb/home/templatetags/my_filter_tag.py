# !-*- coding: utf-8 -*-
# @Author  : ching(opencoding@hotmail.com)
# @Date    : 2019/05/02
# @Link    : www.cnblogs.com/ching126/ or blog.csdn.net/chenhongwu666
# @Version :
# @Desc    :

from django import template
from django.utils.html import format_html
from django.template.defaultfilters import stringfilter


register = template.Library()


@register.filter
def my_upper(val):
    print('val from template:', val)
    return val.upper()


@register.simple_tag
def circle_page(curr_page, loop_page):
    offset = abs(curr_page - loop_page)

    if offset < 3:
        if curr_page == loop_page:
            page_ele = '<li class="active"><a id="active" href="?page=%s">%s</a></li>' % (loop_page, loop_page)
        else:
            page_ele = '<li><a href="?page=%s">%s</a></li>' % (loop_page, loop_page)

        return format_html(page_ele)

    else:
        return ''


@register.filter(name='displayName')
def display_name(value, arg):
    return eval('value.get_' + arg + '_display()')


@stringfilter
def truncate_point(value, arg):
    """
    Truncates a string after a certain number of words including
    alphanumeric and CJK characters.
    Argument: Number of words to truncate after.
    """
    try:
        bits = []
        for x in arg.split(u':'):
            if len(x) == 0:
                bits.append(None)
            else:
                bits.append(int(x))
        if int(x) < len(value):
            return value[slice(*bits)] + '...'
        return value[slice(*bits)]
    except (ValueError, TypeError):
        return value  # Fail silently.


register.filter('truncate_point', truncate_point)
