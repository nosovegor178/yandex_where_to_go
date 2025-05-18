from decimal import Decimal
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db.models import Q
import requests

import codecs
import json
import os

from places.models import Place, Image


def get_json_info_by_file(path):
    with codecs.open(path, 'r', 'utf_8_sig') as file:
        data = file.read()
    parsed_place = json.loads(data)
    return parsed_place


def get_json_info_by_url(url):
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def parse_place(url):
    place = get_json_info_by_url(url)
    Place.objects.get_or_create(
        title=place['title'],
        short_description=place['description_short'],
        long_description=place['description_long'],
        latitude=Decimal(place['coordinates']['lat']),
        longitude=Decimal(place['coordinates']['lng'])
    )


def parse_images(url):
    place = get_json_info_by_url(url)
    for img_number, img in enumerate(place['imgs']):
        img_name = '{} {}.jpg'.format(img_number+1, place['title'])
        path_to_img = os.path.join(place['title'], img_name)
        Image.objects.create(
            place = Place.objects.get(Q(title__contains=place['title'])),
            title=img_name,
            image=path_to_img
        )


class Command(BaseCommand):
    help = 'Download json data with url or with local path and parse it to DB.'

    def handle(self, *args, **options):
        parse_place(options['url'])
        parse_images(options['url'])

    def add_arguments(self, parser):
        parser.add_argument(
            'url', help='Path to json-file in the Inthernet'
        )
