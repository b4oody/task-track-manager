from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def get_referer(context, default="/"):
    request = context.get("request", None)
    return request.META.get("HTTP_REFERER", default)
