from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from formation import views as formation_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/formation/create_player/', formation_views.create_player),
    path('api/formation/get_players_by_position_type/<str:typ>', formation_views.get_players_by_position_type),
    path('api/formation/get_positions/', formation_views.get_positions),
]