from django.urls import path

from coins.views import index

urlpatterns = [
    path('', index),
]