from django.contrib import admin
from .models import Post,Comment
# Register your models here.
class adminpost(admin.ModelAdmin):
    #it is for admin interface customization
    list_display = ['title','status','author']
    list_filter = ('status', 'author' ,'created', 'publish')
    search_fields = ('title', 'body')
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ['status','publish']
    prepopulated_fields = {'slug':('title',)}


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name','email','body','post','created','updated','active']
    list_filter = ('active','created','updated')
    search_fields = ('name','email','body')


admin.site.register(Post,adminpost)
admin.site.register(Comment,CommentAdmin)