from django import template
from django.utils.translation import get_language_info
from django.conf import settings


LANGUAGES = []
for lang_code in settings.LANGUAGES_SUPPORTED:
    LANGUAGES.append(get_language_info(lang_code))

register = template.Library()


@register.inclusion_tag('app/parts/languages_select_part.html')
def language_select(default):
    return {'languages': LANGUAGES, 'default': default}



