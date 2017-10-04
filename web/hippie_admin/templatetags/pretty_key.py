# Custom tag for diagnostics
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

from hippie_ss13.models import Player
from django.core.cache import cache


@register.simple_tag()
def pretty_player(admin):
    if not isinstance(admin, Player):
        raise ValueError("you supplied pretty_player with a non Player type!")

    cache_key = "{}_pretty_html".format(admin.ckey)
    result = cache.get(cache_key)
    if result:
        return mark_safe(result)

    html = (
    "<span class='badge' title='{}' style='background-color: {};color: {};'><i class='fa {}'></i> {} </span>".format(
        admin.get_rank(),
        admin.get_rank_bg_colour(),
        admin.get_rank_fg_colour(),
        admin.get_rank_icon(),
        admin.ckey
    ))
    cache.set(cache_key, html)
    return mark_safe(html)
