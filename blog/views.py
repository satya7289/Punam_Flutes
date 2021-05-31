
from django.urls import reverse
from django.conf import settings
from django.views.generic.list import View
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.shortcuts import render, redirect
from django.core.paginator import PageNotAnInteger

from blog.models import Testimonial, Blog
# Create your views here.


class BlogsListView(View):
    template_name = 'blogs.html'

    def get(self, request):
        blogs = Blog.objects.filter(publish=True)
        for blog in blogs:
            blog.share_url = settings.SITE_URL + reverse('blog_detail', kwargs={'slug': blog.slug})
        context = {
            'blogs': blogs
        }
        return render(request, self.template_name, context)


class BlogDetailView(View):
    template_name = 'blogDetail.html'

    def get(self, request, *args, **kwargs):
        slug = kwargs['slug']
        blog = Blog.objects.filter(slug=slug).first()
        if blog:
            share_url = settings.SITE_URL + reverse('blog_detail', kwargs={'slug': blog.slug})
            return render(request, self.template_name, {'blog': blog, 'share_url': share_url})
        return redirect('dashboard')


class TestinomialListView(View):
    paginate_by = 6
    template_name = 'testinomial_list.html'

    def get(self, request):
        testinomials = Testimonial.objects.filter(publish=True)
        return self.pagination(testinomials)

    def pagination(self, testinomials):
        paginator = Paginator(testinomials, self.paginate_by)
        page = self.request.GET.get("page")
        try:
            testinomials = paginator.page(page)
        except PageNotAnInteger:
            testinomials = paginator.page(1)
        except EmptyPage:
            testinomials = paginator.page(paginator.num_pages)

        # Build the context that to be returned
        context = {
            'testinomials': testinomials,
        }
        return render(self.request, self.template_name, context)
