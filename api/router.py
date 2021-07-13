from django.urls import path
from rest_framework import routers
from api.views import PostViewSet, CategoryViewSet, CommentViewSet

router = routers.SimpleRouter()
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'post', PostViewSet, basename='post')
router.register(r'comment', CommentViewSet, basename='comment')

