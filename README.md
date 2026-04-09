# django_blog

## Installation

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Lancer le projet

```powershell
python manage.py migrate
python manage.py runserver
```

Ouvrir `http://127.0.0.1:8000/`.

## Compte administrateur

Créer un admin localement :

```powershell
python manage.py createsuperuser
```
