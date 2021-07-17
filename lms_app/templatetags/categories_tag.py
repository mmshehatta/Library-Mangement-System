

from django import template
from lms_app.forms import GenreForm
from lms_app.models import Genre , Language
from django.contrib import messages
register = template.Library()

@register.inclusion_tag('parts/sidebar.html')
def all_genres():
 
    context ={
    'genres':Genre.objects.all(),
    'languages':Language.objects.all()
    }
    return context
