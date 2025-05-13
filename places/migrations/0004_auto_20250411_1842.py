from places.models import Place, Image
from django.db.models import Q
from django.db import migrations
import requests
import codecs
import json
import os


def get_images_and_name_of_place(path, filename):
    with codecs.open(f'{path}{filename}', 'r', 'utf_8_sig') as file:
        data = file.read()
    parsed_place = json.loads(data)
    parsed_info = {
        'images': parsed_place['imgs'],
        'name': parsed_place['title']
    }
    return parsed_info


def download_image_and_get_path_and_name(img_url, place_name, img_id):
    media_path = '.\media'
    img_name = f'{img_id} {place_name}.jpg'
    path_to_download = os.path.join(media_path, place_name)
    path_to_img = os.path.join(path_to_download, img_name)
    if not os.path.exists(path_to_download):
        os.makedirs(path_to_download)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(path_to_img, 'wb') as file:
        file.write(response.content)
    return path_to_img, img_name
    

def update_place_relationships(place_name):
    place = Place.objects.get(Q(title__contains=place_name))
    place.images.set(Image.objects.filter(Q(title__contains=place_name)))


def parse_images(apps, schema_editor):
    path = './static/places/'
    for file_id, filename in enumerate(os.listdir(path)):
        place = get_images_and_name_of_place(path, filename)
        for img_number, img in enumerate(place['images']):
            path_to_img, img_name = download_image_and_get_path_and_name(img, place['name'], img_number+1)
            Image.objects.create(
                title = img_name,
                image = path_to_img
            )
        update_place_relationships(place['name'])


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
