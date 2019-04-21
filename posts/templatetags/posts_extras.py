from django import template
from django.utils.html import format_html


register = template.Library()

def formathtml(current, page):
    if current==page:
        source = '<li class="page-item"><a href="?page={0}" class="page-link active">{0}</a></li>'.format(str(current))
        return source
    else    :
        source = '<li class="page-item"><a href="?page={0}" class="page-link">{0}</a></li>'.format(str(page))
        return source

@register.simple_tag
def paginate(current, page, pagenum):
    dist = abs(current-page)
    if current == 1:
        if dist<5:
            source = formathtml(current, page)
            return format_html(source)
        else:
            return ''
    elif current == 2:
        if dist<4:
            source = formathtml(current, page)
            return format_html(source)
        else:
            return ''
    elif current == pagenum:
        if dist<5:
            source = formathtml(current, page)
            return format_html(source)
        else:
            return ''
    elif current == pagenum-1:
        if dist<4:
            source = formathtml(current, page)
            return format_html(source)
        else:
            return ''
    else:
        if dist<3:
            source = formathtml(current, page)
            return format_html(source)
        else:
            return ''
