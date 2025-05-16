from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0005_alter_place_description_long'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='place',
            name='description_long',
        ),
        migrations.RemoveField(
            model_name='place',
            name='description_short',
        ),
        migrations.AddField(
            model_name='place',
            name='long_description',
            field=tinymce.models.HTMLField(blank=True, verbose_name='Полное описание'),
        ),
        migrations.AddField(
            model_name='place',
            name='short_description',
            field=models.TextField(blank=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='place',
            name='latitude',
            field=models.IntegerField(verbose_name='Широта'),
        ),
        migrations.AlterField(
            model_name='place',
            name='longitude',
            field=models.IntegerField(verbose_name='Долгота'),
        ),
    ]
