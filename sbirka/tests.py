from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase
from django.urls import reverse

from .forms import AlbumForm, FilmForm, KnihaForm
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


# --- Formuláře ---
# Pokrývají jen validace, které skutečně existují ve forms.py/models.py:
# nazev/interpret/reziser/autor jsou povinná pole, rok_vydani má
# MinValueValidator(0) (z PositiveIntegerField), hodnoceni má choices 1-5
# a isbn je omezeno na max_length=20 (žádný regex/checksum validátor pro
# formát ISBN v kódu není, proto se netestuje).

class AlbumFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nazev': 'Kid A', 'interpret': 'Radiohead', 'rok_vydani': 2000,
            'zanr': 'Alternative rock', 'pocet_skladeb': 10, 'format': 'vinyl',
            'hodnoceni': 5, 'poznamka': '',
        }

    def test_validni_data(self):
        form = AlbumForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_chybejici_nazev(self):
        data = self.valid_data.copy()
        data['nazev'] = ''
        form = AlbumForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nazev', form.errors)

    def test_zaporny_rok_vydani(self):
        data = self.valid_data.copy()
        data['rok_vydani'] = -1
        form = AlbumForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rok_vydani', form.errors)

    def test_hodnoceni_mimo_rozsah(self):
        data = self.valid_data.copy()
        data['hodnoceni'] = 6
        form = AlbumForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('hodnoceni', form.errors)


class FilmFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nazev': 'Matrix Reloaded', 'reziser': 'Wachowski', 'rok_vydani': 2003,
            'zanr': 'Sci-fi', 'delka_minuty': 138, 'format': 'bluray',
            'hodnoceni': 4, 'poznamka': '',
        }

    def test_validni_data(self):
        form = FilmForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_chybejici_nazev(self):
        data = self.valid_data.copy()
        data['nazev'] = ''
        form = FilmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nazev', form.errors)

    def test_zaporny_rok_vydani(self):
        data = self.valid_data.copy()
        data['rok_vydani'] = -1
        form = FilmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rok_vydani', form.errors)

    def test_hodnoceni_mimo_rozsah(self):
        data = self.valid_data.copy()
        data['hodnoceni'] = 6
        form = FilmForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('hodnoceni', form.errors)


class KnihaFormTest(TestCase):
    def setUp(self):
        self.valid_data = {
            'nazev': 'Farma zvířat', 'autor': 'George Orwell', 'rok_vydani': 1945,
            'zanr': 'Satira', 'pocet_stran': 112, 'isbn': '978-0451526342',
            'format': 'ekniha', 'hodnoceni': 5, 'poznamka': '',
        }

    def test_validni_data(self):
        form = KnihaForm(data=self.valid_data)
        self.assertTrue(form.is_valid())

    def test_chybejici_nazev(self):
        data = self.valid_data.copy()
        data['nazev'] = ''
        form = KnihaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('nazev', form.errors)

    def test_zaporny_rok_vydani(self):
        data = self.valid_data.copy()
        data['rok_vydani'] = -1
        form = KnihaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('rok_vydani', form.errors)

    def test_hodnoceni_mimo_rozsah(self):
        data = self.valid_data.copy()
        data['hodnoceni'] = 6
        form = KnihaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('hodnoceni', form.errors)

    def test_isbn_prilis_dlouhe(self):
        data = self.valid_data.copy()
        data['isbn'] = '1' * 25
        form = KnihaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)

    def test_isbn_neplatny_format(self):
        data = self.valid_data.copy()
        data['isbn'] = 'ABCDEFGHIJ'
        form = KnihaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)

    def test_isbn_neplatny_kontrolni_soucet(self):
        data = self.valid_data.copy()
        data['isbn'] = '978-0451526343'  # poslední číslice pozměněna, formát OK, součet ne
        form = KnihaForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('isbn', form.errors)

    def test_isbn_platne_isbn10(self):
        data = self.valid_data.copy()
        data['isbn'] = '0-306-40615-2'
        form = KnihaForm(data=data)
        self.assertTrue(form.is_valid())


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


# --- CLI příkaz `media` ---
# Pořadí polí zadávaných přes input() odpovídá pořadí AlbumForm.Meta.fields:
# nazev, interpret, rok_vydani, zanr, pocet_skladeb, format, hodnoceni, poznamka.

class MediaCommandListTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            nazev='OK Computer', interpret='Radiohead', rok_vydani=1997,
        )

    def test_list_vypise_polozky(self):
        out = StringIO()
        call_command('media', 'list', 'album', stdout=out)
        self.assertIn('OK Computer', out.getvalue())
        self.assertIn('Radiohead', out.getvalue())

    def test_list_se_sortem(self):
        Album.objects.create(nazev='Absolution', interpret='Muse', rok_vydani=2003)
        out = StringIO()
        call_command('media', 'list', 'album', sort='nazev', stdout=out)
        pozice_absolution = out.getvalue().find('Absolution')
        pozice_ok_computer = out.getvalue().find('OK Computer')
        self.assertNotEqual(pozice_absolution, -1)
        self.assertLess(pozice_absolution, pozice_ok_computer)

    def test_list_prazdny_typ(self):
        out = StringIO()
        call_command('media', 'list', 'film', stdout=out)
        self.assertIn('Žádné položky nenalezeny', out.getvalue())

    def test_list_neplatny_typ_vyvola_chybu(self):
        with self.assertRaises(CommandError):
            call_command('media', 'list', 'neplatny-typ')


class MediaCommandDetailTest(TestCase):
    def setUp(self):
        self.kniha = Kniha.objects.create(
            nazev='1984', autor='George Orwell', rok_vydani=1949, isbn='978-0451524935',
        )

    def test_detail_vypise_vsechna_pole(self):
        out = StringIO()
        call_command('media', 'detail', 'kniha', self.kniha.pk, stdout=out)
        self.assertIn('1984', out.getvalue())
        self.assertIn('George Orwell', out.getvalue())
        self.assertIn('978-0451524935', out.getvalue())

    def test_detail_neexistujici_id_vyvola_chybu(self):
        with self.assertRaises(CommandError) as chyba:
            call_command('media', 'detail', 'kniha', 9999)
        self.assertIn('9999', str(chyba.exception))


class MediaCommandAddTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            nazev='OK Computer', interpret='Radiohead', rok_vydani=1997,
        )

    def test_add_s_validnimi_daty_ulozi_polozku(self):
        vstupy = ['Kid A', 'Radiohead', '2000', 'Alternative rock', '10', 'vinyl', '5', '']
        out = StringIO()
        with patch('builtins.input', side_effect=vstupy):
            call_command('media', 'add', 'album', stdout=out)

        self.assertEqual(Album.objects.count(), 2)
        nova = Album.objects.get(nazev='Kid A')
        self.assertEqual(nova.interpret, 'Radiohead')
        self.assertEqual(nova.rok_vydani, 2000)
        self.assertEqual(nova.format, 'vinyl')
        self.assertIn(str(nova.pk), out.getvalue())

    def test_add_s_nevalidnimi_daty_a_prerusenim_nic_neulozi(self):
        # nazev je prázdný (povinné pole) -> formulář je neplatný, uživatel operaci přeruší
        vstupy = ['', 'Radiohead', '2000', '', '', 'cd', '', '', 'ne']
        out, err = StringIO(), StringIO()
        with patch('builtins.input', side_effect=vstupy):
            call_command('media', 'add', 'album', stdout=out, stderr=err)

        self.assertEqual(Album.objects.count(), 1)
        self.assertIn('nazev', err.getvalue())
        self.assertIn('zrušeno', out.getvalue())

    def test_add_prerusena_ctrl_c_nic_neulozi(self):
        vstupy = ['Kid A', KeyboardInterrupt]
        out = StringIO()
        with patch('builtins.input', side_effect=vstupy):
            call_command('media', 'add', 'album', stdout=out)

        self.assertEqual(Album.objects.count(), 1)
        self.assertIn('přerušena', out.getvalue())

    def test_add_s_nevalidnimi_daty_umozni_opravu(self):
        # 1. pokus: prázdný název -> chyba; uživatel odpoví "ano" a opraví jen název,
        # ostatní pole ponechá prázdná, takže se použijí hodnoty z prvního pokusu.
        prvni_pokus = ['', 'Radiohead', '2000', '', '', 'cd', '', '']
        oprava = ['Kid A', '', '', '', '', '', '', '']
        vstupy = prvni_pokus + ['ano'] + oprava
        out, err = StringIO(), StringIO()
        with patch('builtins.input', side_effect=vstupy):
            call_command('media', 'add', 'album', stdout=out, stderr=err)

        self.assertEqual(Album.objects.count(), 2)
        nova = Album.objects.get(nazev='Kid A')
        self.assertEqual(nova.interpret, 'Radiohead')
        self.assertEqual(nova.rok_vydani, 2000)
        self.assertEqual(nova.format, 'cd')


class MediaCommandEditTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            nazev='OK Computer', interpret='Radiohead', rok_vydani=1997,
        )

    def test_edit_zmeni_pouze_zadane_pole(self):
        # Prázdný Enter u všech ostatních polí ponechá jejich aktuální hodnotu.
        vstupy = ['OK Computer (Reedice)', '', '', '', '', '', '', '']
        out = StringIO()
        with patch('builtins.input', side_effect=vstupy):
            call_command('media', 'edit', 'album', self.album.pk, stdout=out)

        self.album.refresh_from_db()
        self.assertEqual(self.album.nazev, 'OK Computer (Reedice)')
        self.assertEqual(self.album.interpret, 'Radiohead')
        self.assertEqual(self.album.rok_vydani, 1997)

    def test_edit_pomlckou_vyprazdni_volitelne_pole(self):
        self.album.poznamka = 'Oblíbené album'
        self.album.save()
        # Enter u ostatních polí ponechá aktuální hodnotu, '-' u poznámky ji vymaže.
        vstupy = ['', '', '', '', '', '', '', '-']
        out = StringIO()
        with patch('builtins.input', side_effect=vstupy):
            call_command('media', 'edit', 'album', self.album.pk, stdout=out)

        self.album.refresh_from_db()
        self.assertEqual(self.album.poznamka, '')
        self.assertEqual(self.album.nazev, 'OK Computer')

    def test_edit_neexistujici_id_vyvola_chybu(self):
        with self.assertRaises(CommandError):
            call_command('media', 'edit', 'album', 9999)


class MediaCommandDeleteTest(TestCase):
    def setUp(self):
        self.album = Album.objects.create(
            nazev='OK Computer', interpret='Radiohead', rok_vydani=1997,
        )

    def test_delete_s_potvrzenim_smaze_polozku(self):
        out = StringIO()
        with patch('builtins.input', return_value='ano'):
            call_command('media', 'delete', 'album', self.album.pk, stdout=out)
        self.assertEqual(Album.objects.count(), 0)

    def test_delete_bez_potvrzeni_nic_nesmaze(self):
        out = StringIO()
        with patch('builtins.input', return_value='ne'):
            call_command('media', 'delete', 'album', self.album.pk, stdout=out)
        self.assertEqual(Album.objects.count(), 1)
        self.assertIn('zrušeno', out.getvalue())

    def test_delete_neexistujici_id_vyvola_chybu(self):
        with self.assertRaises(CommandError):
            call_command('media', 'delete', 'album', 9999)