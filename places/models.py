from django.db import models

# Create your models here.
class Image(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(verbose_name='Изображение')

    def __str__(self):
        return f'{self.title}'


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    description_short = models.TextField(verbose_name='Краткое описание')
    description_long = models.TextField(verbose_name='Полное описание')
    latitude = models.CharField(max_length=100, verbose_name='Широта')
    longitude = models.CharField(max_length=100, verbose_name='Долгота')
    images = models.ManyToManyField(Image,
                                    blank=True,
                                    related_name='place',
                                    verbose_name='Изображения')

    def __str__(self):
        return f'{self.title}'
