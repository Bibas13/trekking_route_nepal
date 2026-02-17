from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Province, TrekkingRoute, Booking
from .forms import BookingForm, UserRegistrationForm


def home(request):
    provinces = Province.objects.all()
    featured_routes = TrekkingRoute.objects.filter(is_featured=True, is_active=True)[:6]
    all_routes = TrekkingRoute.objects.filter(is_active=True)
    context = {
        'provinces': provinces,
        'featured_routes': featured_routes,
        'total_routes': all_routes.count(),
        'total_provinces': provinces.count(),
    }
    return render(request, 'treks/home.html', context)


def province_list(request):
    provinces = Province.objects.all()
    return render(request, 'treks/province_list.html', {'provinces': provinces})


def province_detail(request, pk):
    province = get_object_or_404(Province, pk=pk)
    routes = TrekkingRoute.objects.filter(province=province, is_active=True)

    # Filters
    difficulty = request.GET.get('difficulty')
    season = request.GET.get('season')
    if difficulty:
        routes = routes.filter(difficulty=difficulty)
    if season:
        routes = routes.filter(best_season=season)

    context = {
        'province': province,
        'routes': routes,
        'difficulty_filter': difficulty,
        'season_filter': season,
        'difficulty_choices': TrekkingRoute.DIFFICULTY_CHOICES,
        'season_choices': TrekkingRoute.SEASON_CHOICES,
    }
    return render(request, 'treks/province_detail.html', context)


def route_list(request):
    routes = TrekkingRoute.objects.filter(is_active=True)
    provinces = Province.objects.all()

    # Search and Filters
    query = request.GET.get('q', '')
    province_id = request.GET.get('province')
    difficulty = request.GET.get('difficulty')
    season = request.GET.get('season')
    duration = request.GET.get('duration')

    if query:
        routes = routes.filter(Q(name__icontains=query) | Q(description__icontains=query))
    if province_id:
        routes = routes.filter(province_id=province_id)
    if difficulty:
        routes = routes.filter(difficulty=difficulty)
    if season:
        routes = routes.filter(best_season=season)
    if duration:
        if duration == '1-7':
            routes = routes.filter(duration_days__gte=1, duration_days__lte=7)
        elif duration == '8-14':
            routes = routes.filter(duration_days__gte=8, duration_days__lte=14)
        elif duration == '15+':
            routes = routes.filter(duration_days__gte=15)

    context = {
        'routes': routes,
        'provinces': provinces,
        'query': query,
        'province_filter': province_id,
        'difficulty_filter': difficulty,
        'season_filter': season,
        'duration_filter': duration,
        'difficulty_choices': TrekkingRoute.DIFFICULTY_CHOICES,
        'season_choices': TrekkingRoute.SEASON_CHOICES,
    }
    return render(request, 'treks/route_list.html', context)


def route_detail(request, pk):
    route = get_object_or_404(TrekkingRoute, pk=pk, is_active=True)
    related_routes = TrekkingRoute.objects.filter(province=route.province, is_active=True).exclude(pk=pk)[:3]
    context = {
        'route': route,
        'related_routes': related_routes,
    }
    return render(request, 'treks/route_detail.html', context)


def book_trek(request, pk):
    route = get_object_or_404(TrekkingRoute, pk=pk, is_active=True)
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.route = route
            if request.user.is_authenticated:
                booking.user = request.user
            # Calculate price
            num_trekkers = form.cleaned_data['num_trekkers']
            booking.total_price = route.price_per_person * num_trekkers
            booking.save()
            messages.success(request, f'Booking confirmed! Your reference is {booking.booking_reference}')
            return redirect('treks:booking_success', pk=booking.pk)
    else:
        initial = {}
        if request.user.is_authenticated:
            initial['full_name'] = request.user.get_full_name()
            initial['email'] = request.user.email
        form = BookingForm(initial=initial)

    context = {
        'route': route,
        'form': form,
    }
    return render(request, 'treks/book_trek.html', context)


def booking_success(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    return render(request, 'treks/booking_success.html', {'booking': booking})


@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'treks/my_bookings.html', {'bookings': bookings})


def register(request):
    if request.user.is_authenticated:
        return redirect('treks:home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Nepal Trekking.')
            return redirect('treks:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})
