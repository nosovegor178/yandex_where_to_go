from django.http import JsonResponse
from places.models import Place
from django.shortcuts import render
import os


def start_page(request):
    places = Place.objects.all()
    places_info = []
    for place_id, place in enumerate(places):
        place_info = build_page_with_json(place_id=place_id).content
        places_info.append({
            'title': place.title,
            'place_id': place.id,
            'coords': [float(place.longitude), float(place.latitude)],
            'json': place_info
        })
    return render(request, 'index.html', context = {'places': places_info})


def build_page_with_json(request, place_id):
    place = Place.objects.all()[place_id]
    places_images = []
    for img in place.images.all():
        places_images.append(img.image.url)
    place_info = {
        'title': place.title,
        'imgs': places_images,
        'description_short': place.description_short,
        'description_long': place.description_long,
        'coords': [place.longitude, place.latitude]
    }
    json_place_info = JsonResponse(place_info, json_dumps_params={'ensure_ascii': False, 'indent': 2})
    return json_place_info