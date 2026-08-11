# 🎵🎬📚 Diskografie – Sbírka médií

Webová aplikace v Django pro evidenci osobní sbírky alb, filmů a knih. Projekt je součástí portfolia demonstrujícího Python/Django dovednosti.

## Funkce

- Evidence tří typů médií: **Alba**, **Filmy**, **Knihy**
- Sdílená datová struktura (roky vydání, hodnocení, poznámky) postavená na abstraktní bázové třídě
- Přehledová domovská stránka s počty položek v jednotlivých kategoriích
- Samostatné seznamy a detaily pro každý typ média
- Administrace přes Django admin (přidávání, editace, mazání záznamů)
- 🚧 Formuláře pro přidávání/editaci přímo v uživatelském rozhraní (ve vývoji)

## Technologie

- Python 3.12
- Django 6.1
- SQLite (vývojová databáze)

## Struktura projektu
diskografie_project/
├── diskografie_projekt/ # Django konfigurace (settings, hlavní urls)
├── sbirka/ # Hlavní aplikace
│ ├── models.py # MediaItem (abstract) → Album, Film, Kniha
│ ├── views.py # Class-based views (ListView, DetailView, TemplateView)
│ ├── urls.py # URL routing appky (namespace 'sbirka')
│ ├── admin.py # Registrace modelů do administrace
│ └── templates/sbirka/ # HTML šablony
└── manage.py

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

## Stav projektu

🚧 Ve vývoji.

✅ Hotovo:
- Datový model a admin rozhraní
- Class-based views (list/detail) pro všechny tři typy médií
- HTML šablony s dědičností (`base.html` + bloky)

📋 Plánováno:
- Formuláře pro přidávání/editaci/mazání záznamů (CreateView, UpdateView, DeleteView)
- Základní stylování (CSS)
- Testy
- CLI nástroj nad stejnými modely

## Autor

Miroslav Svoboda
