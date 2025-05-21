from django.db import models
from tinymce import models as tinymce_models


class Image(models.Model):
    place = models.ForeignKey('Place',
                              on_delete=models.CASCADE,
                              related_name='images',
                              verbose_name='Место')
    title = models.CharField(max_length=255, verbose_name='Название')
    image = models.ImageField(verbose_name='Изображение')
    images_order = models.PositiveIntegerField(default=0,
                                               db_index=True,
                                               verbose_name='Порядковый номер')

    class Meta:
        ordering = ['images_order']

    def __str__(self):
        return f'{self.title}'


class Place(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name='Название',
        unique=True)
    short_description = models.TextField(
        verbose_name='Краткое описание',
        blank=True)
    long_description = tinymce_models.HTMLField(
        verbose_name='Полное описание',
        blank=True)
    latitude = models.DecimalField(
        verbose_name='Широта',
        max_digits=17,
        decimal_places=14)
    longitude = models.DecimalField(
        verbose_name='Долгота',
        max_digits=17,
        decimal_places=14)

    def __str__(self):
        return f'{self.title}'
