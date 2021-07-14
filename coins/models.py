from django.db import models


class Coin(models.Model):
    name = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50)
    price = models.FloatField(blank=True, default=0)
    rank = models.IntegerField(blank=True, default=0)
    image = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['rank']