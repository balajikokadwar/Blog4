from django import template
from blog.models import Post
register = template.Library()

@register.simple_tag(name='count_tag')
def total_post():
    return Post.objects.count()
@register.inclusion_tag('blog/latest_post123.html')
def show_latest_post(count=3):
    latest_post = Post.objects.order_by('-publish')[:count]
    return {'latest_post':latest_post}

from django.db.models import Count
@register.inclusion_tag('blog/latest_post123.html')
def most_commented_post(count=5):
    most_Commented_post =  Post.objects.annotate(total_comments = Count('comments')).order_by('-total_comments')[:count]
    return {'latest_post':most_Commented_post}