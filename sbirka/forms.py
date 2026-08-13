from django import forms
from .models import Album, Film, Kniha


class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['nazev', 'interpret', 'rok_vydani', 'zanr', 'pocet_skladeb', 'format', 'hodnoceni', 'poznamka']


class FilmForm(forms.ModelForm):
    class Meta:
        model = Film
        fields = ['nazev', 'reziser', 'rok_vydani', 'zanr', 'delka_minuty', 'format', 'hodnoceni', 'poznamka']


class KnihaForm(forms.ModelForm):
    class Meta:
        model = Kniha
        fields = ['nazev', 'autor', 'rok_vydani', 'zanr', 'pocet_stran', 'isbn', 'format', 'hodnoceni', 'poznamka']