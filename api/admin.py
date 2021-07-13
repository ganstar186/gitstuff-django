from django.contrib import admin
from api.models import Category, Post, Comments

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Comments)
