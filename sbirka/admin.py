from django.contrib import admin
from .models import Album, Film, Kniha


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'interpret', 'rok_vydani', 'format', 'hodnoceni']
    list_filter = ['format', 'zanr']
    search_fields = ['nazev', 'interpret']


@admin.register(Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'reziser', 'rok_vydani', 'format', 'hodnoceni']
    list_filter = ['format', 'zanr']
    search_fields = ['nazev', 'reziser']


@admin.register(Kniha)
class KnihaAdmin(admin.ModelAdmin):
    list_display = ['nazev', 'autor', 'rok_vydani', 'format', 'hodnoceni']
    list_filter = ['format', 'zanr']
    search_fields = ['nazev', 'autor']
