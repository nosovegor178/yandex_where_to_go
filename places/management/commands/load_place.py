from places.models import Place, Image
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.conf import settings
import json
import codecs
import requests
import os


def get_json_info_by_file(path):
    with codecs.open(path, 'r', 'utf_8_sig') as file:
        data = file.read()
    parsed_place = json.loads(data)
    return parsed_place


def get_json_info_by_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def download_image_and_get_path_and_name(img_url, place_name, img_id):
    media_path = os.path.join(settings.MEDIA_ROOT, place_name)
    img_name = f'{img_id} {place_name}.jpg'
    path_to_img = os.path.join(media_path, img_name)
    if not os.path.exists(media_path):
        os.makedirs(media_path)
    response = requests.get(img_url)
    response.raise_for_status()
    with open(path_to_img, 'wb') as file:
        file.write(response.content)
    relative_path = os.path.join(place_name, img_name)
    return relative_path, img_name


def update_place_relationships(place_name):
    place = Place.objects.get(Q(title__contains=place_name))
    place.images.set(Image.objects.filter(Q(title__contains=place_name)))


def parse_place(url):
    place = get_json_info_by_url(url)
    Place.objects.get_or_create(
        title=place['title'],
        short_description=place['short_description'],
        long_description=place['long_description'],
        latitude=place['coordinates']['lat'],
        longitude=place['coordinates']['lng']
    )


def parse_images(url):
    place = get_json_info_by_url(url)
    for img_number, img in enumerate(place['imgs']):
        path_to_img, img_name = download_image_and_get_path_and_name(img,
                                                                     place['title'],
                                                                     img_number+1)
        Image.objects.create(
            title=img_name,
            image=path_to_img
        )
    update_place_relationships(place['title'])


class Command(BaseCommand):
    help = 'Download json data with url or with local path and parse it to DB.'

    def handle(self, *args, **options):
        parse_place(options['url'])
        parse_images(options['url'])

    def add_arguments(self, parser):
        parser.add_argument(
            'url', help='Path to json-file in the Inthernet'
        )
