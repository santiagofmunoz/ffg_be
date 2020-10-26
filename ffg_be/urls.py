from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from formation import views as formation_views

urlpatterns = [
    path('admin/', admin.site.urls),

    url(r'api/formation/create_player/$', formation_views.create_player),
    path('api/formation/get_position_by_type/<typ>/', formation_views.get_position_by_type),
]