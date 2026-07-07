from django.urls import path
from .views import LicensingView

urlpatterns = [
    path('', LicensingView.as_view(), name='licensing-list'),
]
