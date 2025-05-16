from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from where_to_go import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.start_page),
    path('places/<int:place_id>/', views.build_page_with_json),
    path('tinymce/', include('tinymce.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
