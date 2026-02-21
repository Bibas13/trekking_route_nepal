# 🏔️ Nepal Trek Explorer

A full featured Django website for exploring and booking trekking routes across all 7 provinces of Nepal.

## Features
- 🗺️ Browse all 7 provinces of Nepal with their trekking routes
- 🔍 Search & filter routes by difficulty, season, duration, province
- 📋 Detailed route pages with highlights, inclusions/exclusions
- 📅 Full booking system with guide/porter requests
- 👤 User registration & login system
- 📊 Admin dashboard to manage all data
- 📱 Responsive design that works on mobile & desktop


## how to make it display in your local computer
```
##Quick Start

1. Install Dependencies

pip install -r requirements.txt


### 2. Run Database Migrations

python manage.py makemigrations treks

python manage.py migrate


### 3. Load Sample Data (7 Provinces and 8 sample Trek Routes)

python manage.py loaddata treks/fixtures/initial_data.json


 4. Create Admin User

python manage.py createsuperuser


5. Start the Server

python manage.py runserver


Visit: http://<host:ip>:8000
Admin: http://<host:ip>:8000/admin/

```

```
## Adding Content via Admin
1. Go to `/admin/`
2. Add **Provinces** (or use the sample fixture)
3. Add **Trekking Routes** linked to provinces
4. View and manage **Bookings**

## Adding Route Images
Place images in the `/media/routes/` folder and assign them via admin.

## Deployment Notes
- Change `SECRET_KEY` in settings.py
- Set `DEBUG = False` in production
- Configure a proper database (PostgreSQL recommended)
- Run `python manage.py collectstatic`
