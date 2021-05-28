from django.urls import path

from .views import (
    TestinomialListView,
)

urlpatterns = [
    path('testinomials', TestinomialListView.as_view(), name='testinomials'),
]
