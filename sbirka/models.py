from django.db import models


class MediaItem(models.Model):
    """Abstraktní základ – společné vlastnosti všech typů médií."""
    nazev = models.CharField(max_length=200)
    rok_vydani = models.PositiveIntegerField()
    hodnoceni = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)],
        blank=True, null=True,
        help_text="Hodnocení 1-5 hvězdiček"
    )
    poznamka = models.TextField(blank=True)
    datum_pridani = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-datum_pridani']

    def __str__(self):
        return f"{self.nazev} ({self.rok_vydani})"


class Album(MediaItem):
    FORMAT_VOLBY = [
        ('cd', 'CD'),
        ('vinyl', 'Vinyl'),
        ('digital', 'Digitální'),
    ]
    interpret = models.CharField(max_length=200)
    zanr = models.CharField(max_length=100, blank=True)
    pocet_skladeb = models.PositiveSmallIntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, choices=FORMAT_VOLBY, default='cd')

    class Meta(MediaItem.Meta):
        verbose_name = "Album"
        verbose_name_plural = "Alba"

class Film(MediaItem):
    FORMAT_VOLBY = [
        ('dvd', 'DVD'),
        ('bluray', 'Blu-ray'),
        ('streaming', 'Streaming'),
    ]
    reziser = models.CharField(max_length=200)
    zanr = models.CharField(max_length=100, blank=True)
    delka_minuty = models.PositiveSmallIntegerField(blank=True, null=True)
    format = models.CharField(max_length=10, choices=FORMAT_VOLBY, default='dvd')

    class Meta(MediaItem.Meta):
        verbose_name = "Film"
        verbose_name_plural = "Filmy"

class Kniha(MediaItem):
    FORMAT_VOLBY = [
        ('papir', 'Papírová'),
        ('ekniha', 'E-kniha'),
        ('audiokniha', 'Audiokniha'),
    ]
    autor = models.CharField(max_length=200)
    zanr = models.CharField(max_length=100, blank=True)
    pocet_stran = models.PositiveSmallIntegerField(blank=True, null=True)
    isbn = models.CharField(max_length=20, blank=True)
    format = models.CharField(max_length=10, choices=FORMAT_VOLBY, default='papir')

    class Meta(MediaItem.Meta):
        verbose_name = "Kniha"
        verbose_name_plural = "Knihy"