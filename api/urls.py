from django.urls import path

from api.router import router
from api import views
urlpatterns = [

]
urlpatterns += router.urls

