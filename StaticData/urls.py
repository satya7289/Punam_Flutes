from django.urls import path

from .views import (
    internationalStore,
    indianStore,
    SupportView,
    indianStoreDetail,
    internationalStoreDetail
)

urlpatterns = [
    # path('terms-and-conditions/', termsCondition, name='termsCondition'),
    # path('return-policy/', returnPolicy, name='returnPolicy'),
    # path('refund-policy/', refundPolicy, name='refundPolicy'),
    path('support/<slug:slug>', SupportView.as_view(), name='support'),
    path('store/indian-store', indianStore, name='indianStore'),
    path('store/international-store', internationalStore, name='internationalStore'),
    path('store/international-store/<slug:slug>', internationalStoreDetail.as_view(), name='internationalStore_detail'),
    path('store/indian-store/<slug:slug>', indianStoreDetail.as_view(), name='indianStore_detail'),
]
