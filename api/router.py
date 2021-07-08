from django.urls import path
from rest_framework import routers
from api.views import PostViewSet, CategoryViewSet, UserAPIView, CurrentUserView

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'post', PostViewSet, basename='post')

extra_urlpatterns = [
    path('check-user-is-authenticated/', CurrentUserView.as_view(), name='check-user-is-authenticated'),
    path('user/', UserAPIView.as_view())
]