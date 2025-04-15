from django.db import migrations
from places.models import Place
import codecs
import json
import os



def get_info_about_place(path, filename):
    with codecs.open(f'{path}{filename}', 'r', 'utf_8_sig') as file:
        data = file.read()
    parsed_place = json.loads(data)
    return parsed_place


def parse_places(apps, schema_editor):
    path = 'static/places/'
    for file_id, filename in enumerate(os.listdir(path)):
        place = get_info_about_place(path, filename)
        Place.objects.create(
            title = place['title'],
            description_short = place['description_short'],
            description_long = place['description_long'],
            latitude = place['coordinates']['lat'],
            longitude = place['coordinates']['lng']
        )


def move_backward(apps, schema_editor):
    Place.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(parse_places, move_backward)
    ]
