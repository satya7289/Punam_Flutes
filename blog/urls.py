from django.urls import path

from .views import (
    TestinomialListView,
    BlogsListView,
    BlogDetailView,
)

urlpatterns = [
    path('blogs/', BlogsListView.as_view(), name='blogs'),
    path('blogs/<slug:slug>', BlogDetailView.as_view(), name='blog_detail'),
    path('testinomials/', TestinomialListView.as_view(), name='testinomials'),
]
