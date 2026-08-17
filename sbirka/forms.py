import re

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

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn', '')
        if not isbn:
            return isbn

        cislice = re.sub(r'[\s-]', '', isbn).upper()
        if not re.fullmatch(r'\d{9}[\dX]|\d{13}', cislice):
            raise forms.ValidationError(
                'Zadejte platné ISBN-10 nebo ISBN-13 (číslice, volitelně oddělené pomlčkami).'
            )

        if len(cislice) == 10:
            platne = self._je_platne_isbn10(cislice)
        else:
            platne = self._je_platne_isbn13(cislice)

        if not platne:
            raise forms.ValidationError('Zadané ISBN má neplatný kontrolní součet.')

        return isbn

    @staticmethod
    def _je_platne_isbn10(cislice):
        soucet = sum(
            (10 - i) * (10 if znak == 'X' else int(znak))
            for i, znak in enumerate(cislice)
        )
        return soucet % 11 == 0

    @staticmethod
    def _je_platne_isbn13(cislice):
        soucet = sum(
            (1 if i % 2 == 0 else 3) * int(znak)
            for i, znak in enumerate(cislice)
        )
        return soucet % 10 == 0