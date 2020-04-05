from django.urls import path

from srodunia.views import SroduniaHomeView

urlpatterns = [
    path('', SroduniaHomeView.as_view(), name='home_view'),
]