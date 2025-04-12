from django.db import models

# Create your models here.
class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    latitude = models.CharField(max_length=100, verbose_name='Широта')
    longitude = models.CharField(max_length=100, verbose_name='Долгота')
    

class Image(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(verbose_name='Изображение')