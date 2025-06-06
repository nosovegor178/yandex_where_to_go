from decimal import Decimal
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
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


def parse_place_with_images(url):
    place = get_json_info_by_url(url)
    parsed_place = Place.objects.get_or_create(
        title=place['title'],
        defaults={
            'short_description': place['description_short'],
            'long_description': place['description_long'],
            'latitude': Decimal(place['coordinates']['lat']),
            'longitude': Decimal(place['coordinates']['lng']),
        }
    )[0]
    for img_number, img_url in enumerate(place['imgs']):
        try:
            response = requests.get(img_url)
            response.raise_for_status()
            img_content = ContentFile(response.content)
            img_name = '{} {}.jpg'.format(img_number+1, parsed_place.title)
            image_instance = Image(place=parsed_place)
            image_instance.image.save(img_name, img_content, save=True)
        except requests.exceptions.HTTPError or\
                requests.exceptions.ConnectionError:
            pass


class Command(BaseCommand):
    help = 'Download json data with url or with local path and parse it to DB.'

    def handle(self, *args, **options):
        parse_place_with_images(options['url'])

    def add_arguments(self, parser):
        parser.add_argument(
            'url', help='Path to json-file in the Inthernet'
        )
