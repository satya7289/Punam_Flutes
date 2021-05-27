from django.views.generic.list import View
from django.shortcuts import render
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger

from blog.models import Testimonial
# Create your views here.


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
