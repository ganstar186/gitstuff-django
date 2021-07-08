from rest_framework import serializers

from api.models import Category, Post


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CustomCategorySerializer(serializers.ModelSerializer):
    posts = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'get_absolute_url','posts')

    @staticmethod
    def get_posts(obj):
        return PostSerializerList(Post.objects.filter(category=obj), many=True).data


class PostSerializerList(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "category",
            "name",
            "slug",
            "desc",
            "image",
            "thumbnail",
            "get_image",
            "get_thumbnail",
            "get_absolute_url",
            'date_added',
            'author',
            "is_published",
        )
