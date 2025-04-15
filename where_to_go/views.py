from django.http import HttpResponse
from places.models import Place
from django.shortcuts import render
import os


def start_page(request):
    places = Place.objects.all()
    places_info = []
    places_json = os.listdir('static/places')
    for place_id, place in enumerate(places):
        places_info.append({
            'title': place.title,
            'place_id': place.id,
            'coords': [float(place.longitude), float(place.latitude)],
            'json': f'./places/{places_json[place_id]}'
        })
    return render(request, 'index.html', context = {'places': places_info})