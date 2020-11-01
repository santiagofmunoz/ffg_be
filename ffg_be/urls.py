from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from formation import views as formation_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/formation/create_player/', formation_views.create_player),
    path('api/formation/create_formation/', formation_views.create_formation),
    path('api/formation/get_positions/', formation_views.get_positions),
    path('api/formation/get_players_position_detail/', formation_views.get_players_position_detail),
    path('api/formation/get_formations/', formation_views.get_formations),
    path('api/formation/export_formation_as_pdf/<int:formation_id>', formation_views.export_formation_as_pdf),
]