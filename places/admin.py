from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html
from django.utils.safestring import mark_safe


def preview_inline(obj):
        try:
            if obj.image_id:
                image = Image.objects.get(pk=obj.image_id)
                return format_html('<img src="{}" style="max-height: 200px;">', image.image.url)
        except Exception as e:
            return format_html('<span style="color: red;">Ошибка загрузки: {}</span>', e)


class AdminInline(admin.TabularInline):
    model = Place.images.through
    can_delete = False
    fields = (('image', preview_inline))
    readonly_fields = [preview_inline,]
    verbose_name_plural = 'Фотографии'


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    list_display = ['title',]
    raw_id_fields = ('images',)
    inlines = [
        AdminInline
    ]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def preview(obj):
        return format_html('<img src="{url}" style="width:300px; height:200px;">', url=obj.image.url)
    list_display = ['title',]
    readonly_fields = [preview,]

    def has_delete_permission(self, request, obj=None):
        return False
    