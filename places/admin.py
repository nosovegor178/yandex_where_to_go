from django.contrib import admin
from places.models import Place, Image


class AdminInline(admin.TabularInline):
    model = Place.images.through

@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title',]
    raw_id_fields = ('images',)
    inlines = [
        AdminInline
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ['title',]
