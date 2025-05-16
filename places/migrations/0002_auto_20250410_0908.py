from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
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
            ],
        ),
        migrations.CreateModel(
            name='PlaceImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images_order', models.PositiveIntegerField(db_index=True, default=0)),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.image')),
                ('place', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.place')),
            ],
            options={
                'ordering': ['images_order'],
            },
        ),
        migrations.AddField(
            model_name='place',
            name='images',
            field=models.ManyToManyField(blank=True, related_name='place', through='places.PlaceImage', to='places.image', verbose_name='Изображения'),
        ),
    ]
