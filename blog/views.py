from django.views.generic import ListView, DetailView
from blog.models import Article, Category, Page


class IndexView(ListView):
    model = Article
    template_name = 'index.html'
    paginate_by = 30
    ordering = ['-date']

    def get_queryset(self):
        if self.kwargs.get('slug'):
            self.category = Category.objects.get(slug=self.kwargs['slug'])
            return Article.objects.filter(category=self.category)
        else:
            self.category = None
            return Article.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['category'] = self.category
        if self.request.is_ajax():
            self.template_name = 'appender.html'
        return context


class PostView(DetailView):
    model = Article
    template_name = 'post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        context['allposts'] = Article.objects.order_by('-date')[:10]
        return context


class PageView(DetailView):
    model = Page
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cats'] = Category.objects.all()
        return context
