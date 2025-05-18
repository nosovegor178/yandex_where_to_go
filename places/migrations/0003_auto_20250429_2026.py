from decimal import Decimal
from django.db import migrations

import codecs
import json
import os

from places.models import Place


def get_info_about_place(path, filename):
    with codecs.open(f'{path}{filename}', 'r', 'utf_8_sig') as file:
        data = file.read()
    parsed_place = json.loads(data)
    return parsed_place


def parse_places(apps, schema_editor):
    path = './static/places/'
    for filename in os.listdir(path):
        place = get_info_about_place(path, filename)
        Place.objects.get_or_create(
            title = place['title'],
            short_description = place['description_short'],
            long_description = place['description_long'],
            latitude = Decimal(place['coordinates']['lat']),
            longitude = Decimal(place['coordinates']['lng'])
        )


def move_backward(apps, schema_editor):
    Place.objects.all().delete()


class Migration(migrations.Migration):

    atomic = False

    dependencies = [
        ('places', '0002_auto_20250410_0908'),
    ]

    operations = [
        migrations.RunPython(parse_places, move_backward)
    ]
