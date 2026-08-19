"""CLI rozhraní nad sbírkou médií (alba, filmy, knihy).

Nabízí stejné operace jako webové views (list/detail/add/edit/delete),
ale z příkazové řádky, a validuje data přes stejné ModelFormy jako views.
"""
from django.core.management.base import BaseCommand, CommandError

from sbirka.forms import AlbumForm, FilmForm, KnihaForm
from sbirka.models import Album, Film, Kniha


class Command(BaseCommand):
    help = "Správa položek sbírky (alba, filmy, knihy) z příkazové řádky."

    # Typ -> (model, ModelForm, název pole, které se u výpisu zobrazí navíc k názvu)
    TYPY = {
        'album': (Album, AlbumForm, 'interpret'),
        'film': (Film, FilmForm, 'reziser'),
        'kniha': (Kniha, KnihaForm, 'autor'),
    }

    def add_arguments(self, parser):
        """Definuje podpříkazy (list/detail/add/edit/delete) a jejich argumenty."""
        subparsers = parser.add_subparsers(
            dest='action', required=True, help='Podpříkaz, který se má provést',
        )
        typy = list(self.TYPY.keys())

        list_parser = subparsers.add_parser('list', help='Vypíše přehled všech položek daného typu')
        list_parser.add_argument('typ', choices=typy, help='Typ média: album, film nebo kniha')
        list_parser.add_argument(
            '--sort', choices=['nazev', 'rok_vydani'], default=None,
            help='Volitelné seřazení výpisu podle pole (výchozí: nejnovější první)',
        )

        detail_parser = subparsers.add_parser('detail', help='Vypíše všechna pole vybrané položky')
        detail_parser.add_argument('typ', choices=typy, help='Typ média: album, film nebo kniha')
        detail_parser.add_argument('id', type=int, help='ID položky')

        add_parser = subparsers.add_parser('add', help='Interaktivně přidá novou položku daného typu')
        add_parser.add_argument('typ', choices=typy, help='Typ média: album, film nebo kniha')

        edit_parser = subparsers.add_parser('edit', help='Interaktivně upraví existující položku')
        edit_parser.add_argument('typ', choices=typy, help='Typ média: album, film nebo kniha')
        edit_parser.add_argument('id', type=int, help='ID položky')

        delete_parser = subparsers.add_parser('delete', help='Smaže položku po explicitním potvrzení')
        delete_parser.add_argument('typ', choices=typy, help='Typ média: album, film nebo kniha')
        delete_parser.add_argument('id', type=int, help='ID položky')

    def handle(self, *args, **options):
        """Rozcestník - podle podpříkazu (`action`) zavolá odpovídající metodu."""
        akce = options['action']
        typ = options['typ']
        model, form_class, popis_pole = self.TYPY[typ]

        if akce == 'list':
            self._list(model, popis_pole, options['sort'])
        elif akce == 'detail':
            self._detail(model, typ, options['id'])
        elif akce == 'add':
            self._add(model, form_class, typ)
        elif akce == 'edit':
            self._edit(model, form_class, typ, options['id'])
        elif akce == 'delete':
            self._delete(model, typ, options['id'])

    # --- podpříkazy ---

    def _list(self, model, popis_pole, razeni):
        """Vypíše id, název a doplňkové pole (interpret/režisér/autor) všech položek daného typu."""
        queryset = model.objects.all()
        if razeni:
            queryset = queryset.order_by(razeni)

        if not queryset.exists():
            self.stdout.write('Žádné položky nenalezeny.')
            return

        for polozka in queryset:
            doplnek = getattr(polozka, popis_pole)
            self.stdout.write(f'[{polozka.pk}] {polozka.nazev} — {doplnek} ({polozka.rok_vydani})')

    def _detail(self, model, typ, id_):
        """Vypíše hodnoty všech polí jedné položky, nebo srozumitelnou chybu pro neexistující ID."""
        polozka = self._najdi_nebo_chyba(model, typ, id_)
        self.stdout.write(f'--- {model._meta.verbose_name} #{polozka.pk} ---')
        for pole in model._meta.fields:
            self.stdout.write(f'{pole.verbose_name}: {getattr(polozka, pole.name)}')

    def _add(self, model, form_class, typ):
        """Interaktivně načte hodnoty pro novou položku, ověří je přes ModelForm a uloží ji."""
        self.stdout.write(f'Přidání nové položky typu „{typ}“ (Ctrl+C pro přerušení).')
        try:
            objekt = self._interaktivni_formular(form_class)
        except KeyboardInterrupt:
            self.stdout.write('\nOperace přerušena uživatelem, žádná data nebyla uložena.')
            return
        if objekt is None:
            self.stdout.write('Přidání zrušeno, žádná data nebyla uložena.')
            return
        self.stdout.write(self.style.SUCCESS(f'Položka byla vytvořena, id={objekt.pk}.'))

    def _edit(self, model, form_class, typ, id_):
        """Načte existující položku a u každého pole nabídne úpravu (Enter ponechá původní hodnotu)."""
        instance = self._najdi_nebo_chyba(model, typ, id_)
        self.stdout.write(
            f'Úprava položky #{instance.pk}: {instance} (Ctrl+C pro přerušení). '
            f'Enter ponechá aktuální hodnotu.',
        )
        try:
            objekt = self._interaktivni_formular(form_class, instance=instance)
        except KeyboardInterrupt:
            self.stdout.write('\nOperace přerušena uživatelem, položka nebyla změněna.')
            return
        if objekt is None:
            self.stdout.write('Úprava zrušena, položka nebyla změněna.')
            return
        self.stdout.write(self.style.SUCCESS(f'Položka #{objekt.pk} byla upravena.'))

    def _delete(self, model, typ, id_):
        """Smaže položku, ale pouze pokud uživatel smazání výslovně potvrdí zadáním „ano“."""
        instance = self._najdi_nebo_chyba(model, typ, id_)
        self.stdout.write(f'Ke smazání: [{instance.pk}] {instance}')
        try:
            potvrzeni = input(
                'Opravdu smazat? Zadejte „ano“ pro potvrzení (Ctrl+C pro přerušení): ',
            ).strip().lower()
        except KeyboardInterrupt:
            self.stdout.write('\nOperace přerušena uživatelem, položka nebyla smazána.')
            return
        if potvrzeni != 'ano':
            self.stdout.write('Smazání zrušeno.')
            return
        instance.delete()
        self.stdout.write(self.style.SUCCESS(f'Položka #{id_} byla smazána.'))

    # --- pomocné metody ---

    def _najdi_nebo_chyba(self, model, typ, id_):
        """Vrátí instanci podle ID, nebo ukončí příkaz srozumitelnou chybou (bez tracebacku)."""
        try:
            return model.objects.get(pk=id_)
        except model.DoesNotExist:
            raise CommandError(f'{typ} s id={id_} nebyl nalezen.')

    def _interaktivni_formular(self, form_class, instance=None):
        """Opakovaně načte data od uživatele a validuje je přes ModelForm, dokud nejsou platná.

        Po neplatném zadání vypíše chyby po polích a nechá uživatele buď opravit
        vstup (předchozí hodnoty se použijí jako výchozí), nebo operaci přerušit.
        Vrací uloženou instanci, nebo None, pokud uživatel operaci přerušil.
        """
        data = None
        while True:
            data = self._nacti_data_formulare(form_class, instance=instance, predchozi_data=data)
            form = form_class(data=data, instance=instance)
            if form.is_valid():
                return form.save()

            self.stderr.write(self.style.ERROR('Zadaná data nejsou platná:'))
            for pole, chyby in form.errors.items():
                for chyba in chyby:
                    self.stderr.write(f'  {pole}: {chyba}')

            znovu = input('Opravit zadání a zkusit to znovu? (ano/ne): ').strip().lower()
            if znovu != 'ano':
                return None

    def _nacti_data_formulare(self, form_class, instance=None, predchozi_data=None):
        """Interaktivně vyzve uživatele k zadání hodnoty pro každé pole formuláře.

        Jako výchozí hodnotu (zobrazenou v hranatých závorkách, použije se při
        prázdném Enteru) nabídne buď předchozí (neplatné) zadání, nebo - pokud
        se upravuje existující položka - její aktuální hodnotu.
        """
        data = {}
        prazdny_formular = form_class(instance=instance)

        for jmeno, pole in prazdny_formular.fields.items():
            if predchozi_data is not None:
                vychozi = predchozi_data.get(jmeno, '')
            else:
                hodnota = prazdny_formular.initial.get(jmeno)
                vychozi = '' if hodnota is None else str(hodnota)

            napoveda_castky = []
            if pole.help_text:
                napoveda_castky.append(pole.help_text)
            if getattr(pole, 'choices', None):
                moznosti = ', '.join(str(klic) for klic, _ in pole.choices if klic != '')
                napoveda_castky.append(f'možnosti: {moznosti}')
            if not pole.required:
                napoveda_castky.append("zadejte '-' pro vymazání pole")
            napoveda = f' ({"; ".join(napoveda_castky)})' if napoveda_castky else ''

            vyzva = f'{pole.label}{napoveda}'
            if vychozi != '':
                vyzva += f' [{vychozi}]'
            vyzva += ': '

            zadano = input(vyzva)
            if zadano == '-':
                zadano = ''
            elif zadano == '' and vychozi != '':
                zadano = vychozi
            data[jmeno] = zadano

        return data
