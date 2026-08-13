from django.urls import path
from . import views

app_name = 'sbirka'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),

    path('alba/', views.AlbumListView.as_view(), name='album_list'),
    path('alba/nove/', views.AlbumCreateView.as_view(), name='album_create'),
    path('alba/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('alba/<int:pk>/upravit/', views.AlbumUpdateView.as_view(), name='album_update'),
    path('alba/<int:pk>/smazat/', views.AlbumDeleteView.as_view(), name='album_delete'),

    path('filmy/', views.FilmListView.as_view(), name='film_list'),
    path('filmy/nove/', views.FilmCreateView.as_view(), name='film_create'),
    path('filmy/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
    path('filmy/<int:pk>/upravit/', views.FilmUpdateView.as_view(), name='film_update'),
    path('filmy/<int:pk>/smazat/', views.FilmDeleteView.as_view(), name='film_delete'),

    path('knihy/', views.KnihaListView.as_view(), name='kniha_list'),
    path('knihy/nove/', views.KnihaCreateView.as_view(), name='kniha_create'),
    path('knihy/<int:pk>/', views.KnihaDetailView.as_view(), name='kniha_detail'),
    path('knihy/<int:pk>/upravit/', views.KnihaUpdateView.as_view(), name='kniha_update'),
    path('knihy/<int:pk>/smazat/', views.KnihaDeleteView.as_view(), name='kniha_delete'),
]