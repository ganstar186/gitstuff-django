import json
from io import BytesIO

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.core.files import File
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='Название')
    slug = models.SlugField(unique=True, db_index=True, max_length=150, verbose_name='URL')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    @property
    def posts(self):
        return json.dumps(Post.objects.filter(category=self).values())

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = "Категории"


class Post(models.Model):
    """Класс постов"""
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_author', verbose_name='Автор')
    name = models.CharField(max_length=100, verbose_name='Название')
    slug = models.SlugField(unique=True, db_index=True, max_length=150, null=True, verbose_name='URL')
    desc = models.TextField(max_length=1000, verbose_name='Описание')
    image = models.ImageField(upload_to='uploads', blank=True, verbose_name='Изображение')
    thumbnail = models.ImageField(upload_to='uploads', blank=True, null=True, verbose_name='Миниатюра')
    date_added = models.TimeField(auto_now_add=True, verbose_name='Время создания')
    is_published = models.BooleanField(default=True, verbose_name='Опубликованно')


    @property
    def get_comments(self):
        return json.dumps(Comments.objects.filter())

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def __str__(self):
        return self.name

    """Получаем URL изображения"""

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    """Получаем URL миниатюры"""

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    """Создаем миниатюру"""

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Посты"
        ordering = ('-date_added',)


class Comments(models.Model):
    """Модель коммеентариев"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comment',
                             verbose_name='Комметарий для поста')
    text = models.TextField(verbose_name='Текст комментария', max_length=1000)
    time_create = models.DateTimeField(auto_now=True, verbose_name='Время создания')

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
