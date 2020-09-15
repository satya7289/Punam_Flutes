from django.urls import path
from django.views.generic.base import TemplateView

from .views import CreateAddress

urlpatterns = [
    path('create_address', CreateAddress.as_view(), name='create_address'),
    path('update_address', CreateAddress.as_view(), name='update_address'),
]
