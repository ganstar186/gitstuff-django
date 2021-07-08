from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Post, Category
from api.pagination import CategoryPostPagination
from api.serializers import PostSerializerList, CustomCategorySerializer


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects
    serializer_class = CustomCategorySerializer
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(methods=["get"], detail=True)
    def category_posts(self, request, *args, **kwargs):
        self.pagination_class = CategoryPostPagination
        posts = Post.objects.filter(category=self.get_object())
        queryset = self.filter_queryset(posts)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = PostSerializerList(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = PostSerializerList(queryset, many=True)
        return Response(serializer.data)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializerList
    lookup_field = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            serializer_data = serializer.data
            return self.get_paginated_response(serializer_data)
        serializer = self.get_serializer(queryset, many=True)
        serializer_data = serializer.data
        return Response(serializer_data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        serializer_data = serializer.data
        return Response(serializer_data)


class CurrentUserView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'is_authenticated': True})
        return Response({'is_authenticated': False})


class UserAPIView(APIView):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({'is_authenticated': True})
        return Response({'is_authenticated': False})
