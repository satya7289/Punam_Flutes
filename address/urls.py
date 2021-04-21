from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required

from .views import (
    CreateAddress, 
    UpdateAddress,
    DeleteAddress,
    SetDefaultAddress,
)

urlpatterns = [
    path('create_address', login_required(CreateAddress.as_view()), name='create_address'),
    path('update_address/<int:id>/', login_required(UpdateAddress.as_view()), name='update_address'),
    path('delete_address/<int:id>/', login_required(DeleteAddress.as_view()), name='delete_address'),
    path('set-default-<int:id>', login_required(SetDefaultAddress.as_view()), name='set_default_address'),
]
