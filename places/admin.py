from django.contrib import admin
from places.models import Place, Image
from django.utils.html import format_html
from adminsortable2.admin import SortableAdminBase, SortableTabularInline


def preview_inline(obj):
    try:
        return format_html(
            '<img src="{}" style="max-width:300px; max-height: 200px;">',
            obj.image.url)
    except Exception as e:
        return format_html(
            '<span style="color: red;">Ошибка загрузки: {}</span>', e
            )


class AdminInline(SortableTabularInline):
    model = Image
    can_delete = False
    extra = 0
    fields = (('image', preview_inline))
    readonly_fields = [preview_inline,]
    verbose_name_plural = 'Фотографии'


@admin.register(Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ['title',]
    inlines = [
        AdminInline
    ]
    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    def preview(obj):
        return format_html(
            '<img src="{}" style="max-width:300px; max-height:200px;">',
            obj.image.url)
    list_display = ['place',]
    raw_id_fields = ['place',]
    readonly_fields = [preview,]
