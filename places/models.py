from django.db import models
from tinymce import models as tinymce_models


class Image(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(verbose_name='Изображение')

    def __str__(self):
        return f'{self.title}'


class Place(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    short_description = models.TextField(verbose_name='Краткое описание', blank=True)
    long_description = tinymce_models.HTMLField(verbose_name='Полное описание', blank=True)
    latitude = models.IntegerField(verbose_name='Широта')
    longitude = models.IntegerField(verbose_name='Долгота')
    images = models.ManyToManyField(Image,
                                    through='PlaceImage',
                                    blank=True,
                                    related_name='place',
                                    verbose_name='Изображения')

    def __str__(self):
        return f'{self.title}'


class PlaceImage(models.Model):
    place = models.ForeignKey('Place', on_delete=models.CASCADE)
    image = models.ForeignKey('Image', on_delete=models.CASCADE)
    images_order = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ['images_order']
