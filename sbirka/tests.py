from django.test import TestCase
from django.urls import reverse

from .models import Album, Film, Kniha


# --- Modely ---

class AlbumModelTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            nazev='OK Computer', interpret='Radiohead', rok_vydani=1997,
        )

    def test_str(self):
        self.assertEqual(str(self.album), 'OK Computer (1997)')

    def test_default_format(self):
        self.assertEqual(self.album.format, 'cd')

    def test_ordering_nejnovejsi_prvni(self):
        starsi = Album.objects.create(nazev='Kid A', interpret='Radiohead', rok_vydani=2000)
        alba = list(Album.objects.all())
        self.assertEqual(alba[0], starsi)
        self.assertEqual(alba[1], self.album)


class FilmModelTest(TestCase):
    def setUp(self):
        self.film = Film.objects.create(
            nazev='Matrix', reziser='Wachowski', rok_vydani=1999,
        )

    def test_str(self):
        self.assertEqual(str(self.film), 'Matrix (1999)')

    def test_default_format(self):
        self.assertEqual(self.film.format, 'dvd')


class KnihaModelTest(TestCase):
    def setUp(self):
        self.kniha = Kniha.objects.create(
            nazev='1984', autor='George Orwell', rok_vydani=1949,
        )

    def test_str(self):
        self.assertEqual(str(self.kniha), '1984 (1949)')

    def test_default_format(self):
        self.assertEqual(self.kniha.format, 'papir')


# --- Home view ---

class HomeViewTest(TestCase):
    def test_pocty_polozek(self):
        Album.objects.create(nazev='A', interpret='X', rok_vydani=2020)
        Film.objects.create(nazev='F', reziser='Y', rok_vydani=2020)
        Kniha.objects.create(nazev='K', autor='Z', rok_vydani=2020)
        Kniha.objects.create(nazev='K2', autor='Z', rok_vydani=2021)

        response = self.client.get(reverse('sbirka:home'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['pocet_alb'], 1)
        self.assertEqual(response.context['pocet_filmu'], 1)
        self.assertEqual(response.context['pocet_knih'], 2)


# --- CRUD views ---
# Společná logika je otestována jednou v AlbumViewsTest a poté zopakována
# pro Film a Knihu, protože views mají stejný tvar (list/detail/create/update/delete).

class AlbumViewsTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            nazev='OK Computer', interpret='Radiohead', rok_vydani=1997,
        )
        self.valid_data = {
            'nazev': 'Kid A', 'interpret': 'Radiohead', 'rok_vydani': 2000,
            'zanr': 'Alternative rock', 'pocet_skladeb': 10, 'format': 'vinyl',
            'hodnoceni': 5, 'poznamka': '',
        }

    def test_list_view(self):
        response = self.client.get(reverse('sbirka:album_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/album_list.html')
        self.assertContains(response, 'OK Computer')

    def test_detail_view(self):
        response = self.client.get(reverse('sbirka:album_detail', args=[self.album.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/album_detail.html')
        self.assertContains(response, 'Radiohead')

    def test_detail_view_neexistujici_404(self):
        response = self.client.get(reverse('sbirka:album_detail', args=[9999]))
        self.assertEqual(response.status_code, 404)

    def test_create_view_get(self):
        response = self.client.get(reverse('sbirka:album_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/album_form.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('sbirka:album_create'), self.valid_data)
        self.assertEqual(Album.objects.count(), 2)
        novy = Album.objects.get(nazev='Kid A')
        self.assertRedirects(response, reverse('sbirka:album_list'))
        self.assertEqual(novy.format, 'vinyl')

    def test_update_view_post(self):
        response = self.client.post(
            reverse('sbirka:album_update', args=[self.album.pk]), self.valid_data,
        )
        self.assertRedirects(response, reverse('sbirka:album_list'))
        self.album.refresh_from_db()
        self.assertEqual(self.album.nazev, 'Kid A')
        self.assertEqual(self.album.rok_vydani, 2000)

    def test_delete_view_post(self):
        response = self.client.post(reverse('sbirka:album_delete', args=[self.album.pk]))
        self.assertRedirects(response, reverse('sbirka:album_list'))
        self.assertEqual(Album.objects.count(), 0)


class FilmViewsTest(TestCase):
    def setUp(self):
        self.film = Film.objects.create(
            nazev='Matrix', reziser='Wachowski', rok_vydani=1999,
        )
        self.valid_data = {
            'nazev': 'Matrix Reloaded', 'reziser': 'Wachowski', 'rok_vydani': 2003,
            'zanr': 'Sci-fi', 'delka_minuty': 138, 'format': 'bluray',
            'hodnoceni': 4, 'poznamka': '',
        }

    def test_list_view(self):
        response = self.client.get(reverse('sbirka:film_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/film_list.html')
        self.assertContains(response, 'Matrix')

    def test_detail_view(self):
        response = self.client.get(reverse('sbirka:film_detail', args=[self.film.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/film_detail.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('sbirka:film_create'), self.valid_data)
        self.assertEqual(Film.objects.count(), 2)
        self.assertRedirects(response, reverse('sbirka:film_list'))

    def test_update_view_post(self):
        response = self.client.post(
            reverse('sbirka:film_update', args=[self.film.pk]), self.valid_data,
        )
        self.assertRedirects(response, reverse('sbirka:film_list'))
        self.film.refresh_from_db()
        self.assertEqual(self.film.nazev, 'Matrix Reloaded')

    def test_delete_view_post(self):
        response = self.client.post(reverse('sbirka:film_delete', args=[self.film.pk]))
        self.assertRedirects(response, reverse('sbirka:film_list'))
        self.assertEqual(Film.objects.count(), 0)


class KnihaViewsTest(TestCase):
    def setUp(self):
        self.kniha = Kniha.objects.create(
            nazev='1984', autor='George Orwell', rok_vydani=1949,
        )
        self.valid_data = {
            'nazev': 'Farma zvířat', 'autor': 'George Orwell', 'rok_vydani': 1945,
            'zanr': 'Satira', 'pocet_stran': 112, 'isbn': '978-0451526342',
            'format': 'ekniha', 'hodnoceni': 5, 'poznamka': '',
        }

    def test_list_view(self):
        response = self.client.get(reverse('sbirka:kniha_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/kniha_list.html')
        self.assertContains(response, '1984')

    def test_detail_view(self):
        response = self.client.get(reverse('sbirka:kniha_detail', args=[self.kniha.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'sbirka/kniha_detail.html')

    def test_create_view_post(self):
        response = self.client.post(reverse('sbirka:kniha_create'), self.valid_data)
        self.assertEqual(Kniha.objects.count(), 2)
        self.assertRedirects(response, reverse('sbirka:kniha_list'))

    def test_update_view_post(self):
        response = self.client.post(
            reverse('sbirka:kniha_update', args=[self.kniha.pk]), self.valid_data,
        )
        self.assertRedirects(response, reverse('sbirka:kniha_list'))
        self.kniha.refresh_from_db()
        self.assertEqual(self.kniha.nazev, 'Farma zvířat')

    def test_delete_view_post(self):
        response = self.client.post(reverse('sbirka:kniha_delete', args=[self.kniha.pk]))
        self.assertRedirects(response, reverse('sbirka:kniha_list'))
        self.assertEqual(Kniha.objects.count(), 0)