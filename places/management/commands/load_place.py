from places.models import Place, Image
from django.core.management.base import BaseCommand
from django.db.models import Q
import requests
import codecs
import json
import os


def get_json_info(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_image_and_get_path_and_name(img_url, place_name, img_id):
    media_path = '.\media'
    img_name = f'{img_id} {place_name}.jpg'
    django_path = os.path.join(place_name, img_name)
    path_to_download = os.path.join(media_path, place_name)
    path_to_img = os.path.join(path_to_download, img_name)
    if not os.path.exists(path_to_download):
        os.makedirs(path_to_download)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(path_to_img, 'wb') as file:
        file.write(response.content)
    return django_path, img_name
    

def update_place_relationships(place_name):
    place = Place.objects.get(Q(title__contains=place_name))
    place.images.set(Image.objects.filter(Q(title__contains=place_name)))


def parse_place(url):
    place = get_json_info(url)
    Place.objects.get_or_create(
        title = place['title'],
        description_short = place['description_short'],
        description_long = place['description_long'],
        latitude = place['coordinates']['lat'],
        longitude = place['coordinates']['lng']
    )


def parse_images(url):
    place = get_json_info(url)
    for img_number, img in enumerate(place['imgs']):
        path_to_img, img_name = download_image_and_get_path_and_name(img, place['title'], img_number+1)
        Image.objects.create(
            title = img_name,
            image = path_to_img
        )
    update_place_relationships(place['title'])


class Command(BaseCommand):
    help = 'Download json data with url'
    def handle(self, *args, **options):
        parse_place(options['url'])
        parse_images(options['url'])
    def add_arguments(self, parser):
        parser.add_argument(
        'url',
        help='Neccesary path to json-file in the Inthernet'
        )
