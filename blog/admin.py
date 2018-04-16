from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Page, Article, Category


admin.site.site_header = 'Seoshnik.Top'


class ArticleAdmin(SummernoteModelAdmin):
    list_display = ['h1', 'date']
    list_filter = ['category', 'automatic', 'date']
    search_fields = ['h1', 'post']
    summernote_fields = ('post', 'short')
    list_per_page = 50


admin.site.register(Category, SummernoteModelAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Page, SummernoteModelAdmin)
