from django import forms
from .models import Album, Film, Kniha

HODNOCENI_PRAZDNA_VOLBA = "Vyber hodnocení"


class MediaFormMixin:
    """Nastaví český text prázdné volby pro pole hodnocení."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hodnoceni'].choices = [
            (hodnota, popisek) if hodnota != '' else (hodnota, HODNOCENI_PRAZDNA_VOLBA)
            for hodnota, popisek in self.fields['hodnoceni'].choices
        ]


class AlbumForm(MediaFormMixin, forms.ModelForm):
    class Meta:
        model = Album
        fields = ['nazev', 'interpret', 'rok_vydani', 'zanr', 'pocet_skladeb', 'format', 'hodnoceni', 'poznamka']
        labels = {
            'nazev': 'Název',
            'interpret': 'Interpret',
            'rok_vydani': 'Rok vydání',
            'zanr': 'Žánr',
            'pocet_skladeb': 'Počet skladeb',
            'format': 'Formát',
            'hodnoceni': 'Hodnocení',
            'poznamka': 'Poznámka',
        }


class FilmForm(MediaFormMixin, forms.ModelForm):
    class Meta:
        model = Film
        fields = ['nazev', 'reziser', 'rok_vydani', 'zanr', 'delka_minuty', 'format', 'hodnoceni', 'poznamka']
        labels = {
            'nazev': 'Název',
            'reziser': 'Režisér',
            'rok_vydani': 'Rok vydání',
            'zanr': 'Žánr',
            'delka_minuty': 'Délka (minuty)',
            'format': 'Formát',
            'hodnoceni': 'Hodnocení',
            'poznamka': 'Poznámka',
        }


class KnihaForm(MediaFormMixin, forms.ModelForm):
    class Meta:
        model = Kniha
        fields = ['nazev', 'autor', 'rok_vydani', 'zanr', 'pocet_stran', 'isbn', 'format', 'hodnoceni', 'poznamka']
        labels = {
            'nazev': 'Název',
            'autor': 'Autor',
            'rok_vydani': 'Rok vydání',
            'zanr': 'Žánr',
            'pocet_stran': 'Počet stran',
            'isbn': 'ISBN',
            'format': 'Formát',
            'hodnoceni': 'Hodnocení',
            'poznamka': 'Poznámka',
        }