from django.contrib import admin
from .models import Post
from django_summernote.admin import SummernoteModelAdmin


class PostAdmin(SummernoteModelAdmin):
    list_display = ('id', 'title_post', 'author_post', 'date_post',
                    'categorie_post','published_post' 
                )
    list_editable = ('published_post',)
    list_display_links = ('id', 'title_post')
    summernote_fields = ('content_post',)


admin.site.register(Post, PostAdmin)