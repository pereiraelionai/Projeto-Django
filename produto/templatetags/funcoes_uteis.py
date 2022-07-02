from django.template import Library
from utils import utils
from atexit import register
from dataclasses import replace

register = Library()


@register.filter
def formata_preco(val):
    return utils.formata_preco(val)
