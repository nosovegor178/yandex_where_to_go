from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
            ],
        ),

        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description_short', models.TextField(verbose_name='Краткое описание')),
                ('description_long', models.TextField(verbose_name='Полное описание')),
                ('latitude', models.CharField(max_length=100, verbose_name='Широта')),
                ('longitude', models.CharField(max_length=100, verbose_name='Долгота')),
                ('images', models.ManyToManyField(blank=True, related_name='place', to='places.Image', verbose_name='Изображения'))
            ],
        ),
    ]
