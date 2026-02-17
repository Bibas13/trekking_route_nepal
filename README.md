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


Visit: http://127.0.0.1:8000
Admin: http://127.0.0.1:8000/admin/

```


## Project Structure

nepal_trekking/
├── manage.py
├── requirements.txt
├── nepal_trekking/          # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── treks/                   # Main app
│   ├── models.py            # Province, TrekkingRoute, Booking
│   ├── views.py             # All page views
│   ├── urls.py              # URL patterns
│   ├── forms.py             # Booking & registration forms
│   ├── admin.py             # Admin configuration
│   └── fixtures/
│       └── initial_data.json  # Sample data (7 provinces, 8 routes)
├── templates/
│   ├── base.html              # Base template with navbar/footer
│   ├── treks/
│   │   ├── home.html          # Landing page
│   │   ├── province_list.html
│   │   ├── province_detail.html
│   │   ├── route_list.html    # Search & filter page
│   │   ├── route_detail.html
│   │   ├── book_trek.html     # Booking form
│   │   ├── booking_success.html
│   │   └── my_bookings.html
│   └── registration/
│       ├── login.html
│       └── register.html
├── static/
│   ├── css/
│   ├── js/
│   └── images/
└── media/                     # Uploaded images



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
