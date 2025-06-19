from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from datetime import datetime,date, timedelta
from .models import Contact, Dining, MenuItem, Accommodation, RoomType, Highlights, BedType
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.core import signing
from django.db.models import Sum

# Create your views here.
def home(request):
    highlights = Highlights.objects.all()
    return render(request, 'staydine/home.html', {'highlights': highlights})

def about(request):
    return render(request, 'staydine/about.html', {'title': 'About Us'})

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')
        date = timezone.now().date()

        contact = Contact(name=name, email=email, phone=phone, desc=desc, date=date)
        contact.save()

        messages.success(request, 'Your message has been successfully submitted!')
        return redirect('staydine-contact')

    return render(request, 'staydine/contact.html', {'title': 'Contact Us'})

def bed_types(request):
    bed_types = BedType.objects.all()
    return render(request, 'staydine/bed_types.html', {'bed_types': bed_types})

@login_required(login_url='login')
def my_orders(request):
    bookings = Accommodation.objects.filter(email=request.user.email).order_by('-start_date')
    return render(request, 'staydine/my_orders.html', {
        'bookings': bookings,
        'title': 'My Orders'
    })


@login_required(login_url='login')
def delete_order(request):
    booking = get_object_or_404(Accommodation, email=request.user.email)
    booking.delete()
    return redirect('my-orders')


@login_required(login_url='login')
def bookings(request):
    if request.method == "POST":
        email = request.user.email
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        try:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('staydine-room-bookings')

        if start_date >= end_date:
            messages.error(request, "Start date must be before end date.")
            return redirect('staydine-room-bookings')
        if start_date <= date.today():
            messages.error(request, "Bookings must be made at least 1 day in advance.")
            return redirect('staydine-room-bookings')

        # Get submitted room counts
        classic = int(request.POST.get('classic_rooms', 0))
        premium = int(request.POST.get('premium_rooms', 0))
        suite = int(request.POST.get('suite_rooms', 0))

        # Fetch total room limits from DB
        try:
            classic_limit = RoomType.objects.get(name__icontains="Classic").total_rooms
            premium_limit = RoomType.objects.get(name__icontains="Premium").total_rooms
            suite_limit = RoomType.objects.get(name__icontains="Suite").total_rooms
        except RoomType.DoesNotExist:
            messages.error(request, "Room type not configured properly in DB.")
            return redirect('staydine-room-bookings')

        overlapping = Accommodation.objects.filter(
            start_date__lt=end_date,
            end_date__gt=start_date
        )
        totals = overlapping.aggregate(
            c=Sum('classic_rooms'),
            p=Sum('premium_rooms'),
            s=Sum('suite_rooms')
        )

        # Already booked
        booked_classic = totals['c'] or 0
        booked_premium = totals['p'] or 0
        booked_suite = totals['s'] or 0

        if booked_classic + classic > classic_limit:
            messages.error(request, "Not enough Classic rooms available.")
            return redirect('staydine-room-bookings')
        if booked_premium + premium > premium_limit:
            messages.error(request, "Not enough Premium rooms available.")
            return redirect('staydine-room-bookings')
        if booked_suite + suite > suite_limit:
            messages.error(request, "Not enough Suite rooms available.")
            return redirect('staydine-room-bookings')

        # Calculate price per night from DB
        price_map = {
            "Classic": RoomType.objects.get(name__icontains="Classic").price_per_night,
            "Premium": RoomType.objects.get(name__icontains="Premium").price_per_night,
            "Suite": RoomType.objects.get(name__icontains="Suite").price_per_night
        }

        nights = (end_date - start_date).days
        total_amount = (
            classic * price_map["Classic"] +
            premium * price_map["Premium"] +
            suite * price_map["Suite"]
        ) * nights

        # Save or update booking (since email is PK)
        Accommodation.objects.update_or_create(
            email=email,
            defaults={
                "classic_rooms": classic,
                "premium_rooms": premium,
                "suite_rooms": suite,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        return render(request, 'staydine/booking_confirmation.html', {
            'classic_rooms': classic,
            'premium_rooms': premium,
            'suite_rooms': suite,
            'start_date': start_date,
            'end_date': end_date,
            'total_amount': total_amount,
            'title': 'Booking Confirmation'
        })

    # For GET requests
    rooms = RoomType.objects.all()
    bed_types = BedType.objects.all()
    return render(request, 'staydine/bookings.html', {
        'rooms': rooms,
        'bed_types': bed_types,
        'title': 'Bookings'
    })

@login_required(login_url='login')
def restaurant(request):
    menu_items = MenuItem.objects.all()

    if request.method == "POST":
        email = request.user.email
        item_nos = request.POST.getlist('item_no')
        quantities = request.POST.getlist('quantity')

        if not item_nos or not quantities or len(item_nos) != len(quantities):
            messages.error(request, "Please fill all fields correctly.")
            return redirect('staydine-restaurant')

        total_amount = 0
        orders = []

        for item_no, quantity in zip(item_nos, quantities):
            try:
                item_no = int(item_no)
                quantity = int(quantity)
                menu_item = MenuItem.objects.get(pk=item_no)
            except (ValueError, MenuItem.DoesNotExist):
                messages.error(request, f"Invalid item or quantity.")
                return redirect('staydine-restaurant')

            total_amount += float(menu_item.price) * quantity
            orders.append(Dining(email=email, item_no=item_no, quantity=quantity))

        # Bulk create orders
        Dining.objects.bulk_create(orders)
        messages.success(request, "Your order has been placed successfully.")

        # Securely sign the payment data
        data = {
            'email': email,
            'orders': list(zip(item_nos, quantities)),
            'amount': total_amount
        }
        signed_data = signing.dumps(data)

        return redirect(f"{reverse('initiate_payment')}?data={signed_data}")

    return render(request, 'staydine/restaurant.html', {
        'menu_items': menu_items,
        'title': 'Menu Bookings'
    })

