from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .views import CreateAddress, UpdateAddress

urlpatterns = [
    path('create_address', login_required(CreateAddress.as_view()), name='create_address'),
    path('update_address', login_required(UpdateAddress.as_view()), name='update_address'),
]
