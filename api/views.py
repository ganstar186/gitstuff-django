from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import Post, Category, Comments
from api.pagination import CategoryPostPagination
from api.serializers import (PostSerializerList, CustomCategorySerializer, CreatePostSerializer,
                             CommentViewSerializer, CommentCreateSerializer)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects
    serializer_class = CustomCategorySerializer
    lookup_field = 'slug'

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
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.action == 'create':
            return CreatePostSerializer
        else:
            return PostSerializerList

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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CommentViewSet(ModelViewSet):
    serializer_class = CommentViewSerializer
    queryset = Comments.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return CommentViewSerializer
        else:
            return CommentCreateSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)





