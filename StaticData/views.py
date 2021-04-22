from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.
@staff_member_required
def SyncCurrencyRate(request):
    print('dyhuj')
    return HttpResponseRedirect(request.META["HTTP_REFERER"])