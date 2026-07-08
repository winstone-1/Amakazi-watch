from django.urls import path
from .views import DonationListView, InitiateDonationView, VerifyDonationView

urlpatterns = [
    path('', DonationListView.as_view(), name='donation-list'),
    path('initiate/', InitiateDonationView.as_view(), name='donation-initiate'),
    path('verify/', VerifyDonationView.as_view(), name='donation-verify'),
]
