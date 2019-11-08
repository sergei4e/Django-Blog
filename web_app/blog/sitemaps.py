from django.contrib.sitemaps import Sitemap
from blog.models import Article, Category, Page


class ArticleSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return obj.date


class CategorySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.9

    def items(self):
        return Category.objects.all()


class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Page.objects.all()
