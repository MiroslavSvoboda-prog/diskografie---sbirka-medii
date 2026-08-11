from django.urls import path
from . import views

app_name = 'sbirka'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('alba/', views.AlbumListView.as_view(), name='album_list'),
    path('alba/<int:pk>/', views.AlbumDetailView.as_view(), name='album_detail'),
    path('filmy/', views.FilmListView.as_view(), name='film_list'),
    path('filmy/<int:pk>/', views.FilmDetailView.as_view(), name='film_detail'),
    path('knihy/', views.KnihaListView.as_view(), name='kniha_list'),
    path('knihy/<int:pk>/', views.KnihaDetailView.as_view(), name='kniha_detail'),
]