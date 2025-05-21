from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название', unique=True)),
                ('short_description', models.TextField(blank=True, verbose_name='Краткое описание')),
                ('long_description', models.TextField(blank=True, verbose_name='Полное описание')),
                ('latitude', models.DecimalField(decimal_places=14, max_digits=17, verbose_name='Широта')),
                ('longitude', models.DecimalField(decimal_places=14, max_digits=17, verbose_name='Долгота')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('image', models.ImageField(upload_to='', verbose_name='Изображение')),
                ('place', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='places.place', related_name='images', verbose_name='Место')),
                ('images_order', models.PositiveIntegerField(db_index=True, default=0, verbose_name='Порядковый номер')),
            ],
            options={
                'ordering': ['images_order'],
            },
        ),
    ]
