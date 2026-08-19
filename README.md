# 🎵🎬📚 Diskografie – Sbírka médií

Webová aplikace v Django pro evidenci osobní sbírky alb, filmů a knih, doplněná o CLI nástroj nad stejnými modely. 
Projekt reprezentuje praktické zvládnutí Django frameworku.

## Funkce

- Evidence tří typů médií: **Alba**, **Filmy**, **Knihy**
- Sdílená datová struktura (roky vydání, hodnocení, poznámky) postavená na abstraktní bázové třídě
- Přehledová domovská stránka s počty položek v jednotlivých kategoriích
- Samostatné seznamy a detaily pro každý typ média
- Plný CRUD přímo v uživatelském rozhraní – přidávání, editace i mazání záznamů (s potvrzovací stránkou u mazání)
- **CLI nástroj** (`python manage.py media`) – stejné operace (list/detail/add/edit/delete) z příkazové řádky, se stejnou validací jako webové rozhraní
- Administrace přes Django admin

## Technologie

- Python 3.12
- Django 6.1
- SQLite (vývojová databáze)

## CLI nástroj

Kromě webového rozhraní je možné se sbírkou pracovat i z příkazové řádky přes vlastní Django management command:

```bash
# Výpis položek daného typu (album / film / kniha)
python manage.py media list album
python manage.py media list film --sort nazev

# Detail jedné položky
python manage.py media detail kniha 3

# Přidání nové položky (interaktivní dotazy na jednotlivá pole)
python manage.py media add album

# Úprava existující položky (Enter ponechá aktuální hodnotu, '-' volitelné pole vymaže)
python manage.py media edit album 3

# Smazání položky (vyžaduje explicitní potvrzení)
python manage.py media delete album 3
```

CLI vrstva **znovupoužívá stejné `ModelForm` třídy jako webové formuláře** – validace (povinná pole, rozsahy hodnot, kontrolní součet ISBN u knih) je tak na obou rozhraních identická a definovaná na jednom místě.

## Automatizované testy

Aplikace `sbirka` má 57 testů v `sbirka/tests.py`, běží nad samostatnou testovací
SQLite databází.

Spuštění:
```bash
python manage.py test sbirka
```

Pokrytí:
- **Modely** (Album, Film, Kniha) – `__str__`, výchozí hodnota `format`, řazení podle
  data přidání (Album)
- **HomeView** – správný počet položek v kontextu
- **CRUD views** (Album, Film, Kniha) – list, detail (i 404 pro neexistující), create
  (GET+POST), update, delete – ověřuje status kódy, šablony, přesměrování a skutečné
  změny v databázi
- **Formulářová validace** (Album, Film, Kniha) – povinná pole, hodnoty mimo povolený
  rozsah (např. hodnocení, rok vydání); u Knihy navíc validace formátu a kontrolního
  součtu ISBN (ISBN-10 i ISBN-13)
- **CLI příkaz `media`** – list (i s řazením a prázdným výsledkem), detail (i chyba
  pro neexistující ID), add (validní data, neplatná data s opravou i s přerušením,
  přerušení pomocí Ctrl+C), edit (ponechání i vymazání volitelného pole pomocí `-`),
  delete (s potvrzením i bez něj), a ošetření neplatného typu média

## Struktura projektu
```
diskografie_project/
├── diskografie_projekt/        # Django konfigurace (settings, hlavní urls)
├── sbirka/                     # Hlavní aplikace
│   ├── models.py                # MediaItem (abstract) → Album, Film, Kniha
│   ├── views.py                 # Class-based views (ListView, DetailView, TemplateView)
│   ├── forms.py                 # ModelFormy (sdílené mezi views a CLI)
│   ├── urls.py                  # URL routing appky (namespace 'sbirka')
│   ├── admin.py                 # Registrace modelů do administrace
│   ├── management/commands/
│   │   └── media.py             # CLI příkaz (list/detail/add/edit/delete)
│   └── templates/sbirka/        # HTML šablony
└── manage.py
```

## Spuštění projektu lokálně

```bash
# Klonování repozitáře
git clone https://github.com/MiroslavSvoboda-prog/diskografie---sbirka-medii.git
cd diskografie---sbirka-medii

# Vytvoření a aktivace virtuálního prostředí
python -m venv venv
source venv/bin/activate   # na Windows: venv\Scripts\activate

# Instalace závislostí
pip install django

# Migrace databáze
python manage.py migrate

# Vytvoření administrátorského účtu
python manage.py createsuperuser

# Spuštění vývojového serveru
python manage.py runserver
```

Aplikace poběží na `http://127.0.0.1:8000/`, administrace na `http://127.0.0.1:8000/admin/`.
CLI nástroj je dostupný po instalaci závislostí a migraci příkazem `python manage.py media --help`.

## Stav projektu

✅ Hotovo:
- Datový model a admin rozhraní
- Class-based views (list/detail) pro všechny tři typy médií
- HTML šablony s dědičností (`base.html` + bloky)
- Formuláře pro přidávání/editaci/mazání záznamů (CreateView, UpdateView, DeleteView)
- Základní stylování (CSS) – barevné odlišení podle typu média
  (alba/filmy/knihy), styling seznamů, detailů, formulářů
  a domovské stránky
- Formulářová validace (povinná pole, rozsahy hodnot, ISBN kontrolní součet)
- CLI nástroj (`python manage.py media`) nad stejnými modely, se sdílenou validací
- Testy (57), pokrývající modely, views i CLI

## Autor

Miroslav Svoboda
