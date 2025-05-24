from django.db.models import Q
from django.db import migrations

import codecs
import json
import os

from places.models import Place, Image


def get_images_and_name_of_place(path, filename):
    with codecs.open(f'{path}{filename}', 'r', 'utf_8_sig') as file:
        data = file.read()
    parsed_place = json.loads(data)
    parsed_info = {
        'images': parsed_place['imgs'],
        'name': parsed_place['title']
    }
    return parsed_info


def parse_images(apps, schema_editor):
    path = './static/places/'
    for file_id, filename in enumerate(os.listdir(path)):
        place = get_images_and_name_of_place(path, filename)
        for img_number, img in enumerate(place['images']):
            img_name = '{} {}.jpg'.format(img_number+1, place['name'])
            path_to_img = os.path.join(place['name'], img_name)
            Image.objects.create(
                place = Place.objects.get(Q(title__contains=place['name'])),
                image = path_to_img
            )


def move_backward(apps, schema_editor):
    Image.objects.all().delete()



class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('places', '0003_auto_20250429_2026'),
    ]

    operations = [
        migrations.RunPython(parse_images, move_backward)
    ]
