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

🚧 Ve vývoji – aktuálně hotový datový model a admin rozhraní.
Plánováno: uživatelské rozhraní (views, šablony), následně CLI nástroj nad stejnými modely.

## Autor

Miroslav Svoboda