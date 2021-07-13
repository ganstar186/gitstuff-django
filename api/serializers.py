from django.contrib.auth.models import User
from rest_framework import serializers

from api.models import Category, Post, Comments


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CustomCategorySerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'get_absolute_url', 'posts')

    @staticmethod
    def get_posts(obj):
        return PostSerializerList(Post.objects.filter(category=obj), many=True).data


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CommentViewSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Comments
        fields = ('id', 'user', 'text', 'time_create')

    @staticmethod
    def get_user(obj):
        if not (obj.user.first_name and obj.user.last_name):
            return obj.user.username
        return ' '.join([obj.user.first_name, obj.user.last_name])

class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'




class PostSerializerList(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(read_only=True, slug_field='name')
    comment = CommentViewSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            'id',
            "category",
            "name",
            "desc",
            "get_image",
            "get_thumbnail",
            "get_absolute_url",
            'date_added',
            'author',
            "is_published",
            'comment',

        )

    @staticmethod
    def get_author(obj):
        if not (obj.author.first_name and obj.author.last_name):
            return obj.author.username
        return ' '.join([obj.author.first_name, obj.author.last_name])


class CreatePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('name', 'category', 'slug', 'author', 'image', 'desc')
