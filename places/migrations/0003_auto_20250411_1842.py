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
    static_path = './static/media'
    img_name = f'{img_id} {place_name}.jpg'
    path_to_img = os.path.join(place_name, img_name)
    path_to_download = f'{static_path}/{path_to_img}'
    if not os.path.exists(path_to_download):
        os.makedirs(path_to_download)
    response = requests.get(img_url)
    response.raise_for_status()
    if not os.path.exists(path_to_download):
        with open(path_to_download, 'wb') as file:
            file.write(response.content)
    return path_to_img, img_name
    

def update_place_relationships(place_name):
    place = Place.objects.get(Q(title__contains=place_name))
    place.images.set(Image.objects.filter(Q(title__contains=place_name)))


def parse_images(apps, schema_editor):
    path = 'static/places/'
    for file_id, filename in enumerate(os.listdir(path)):
        place = get_images_and_name_of_place(path, filename)
        for img_number, img in enumerate(place['images']):
            path_to_img, img_name = download_image_and_get_path_and_name(img, place['name'], img_number+1)
            Image.objects.create(
                # place = Place.objects.get(id = file_id),
                title = img_name,
                image = path_to_img
            )
        update_place_relationships(place['name'])


def move_backward(apps, schema_editor):
    Image.objects.all().delete()



class Migration(migrations.Migration):

    dependencies = [
        ('places', '0002_auto_20250410_0908'),
    ]

    operations = [
        migrations.RunPython(parse_images, move_backward)
    ]
