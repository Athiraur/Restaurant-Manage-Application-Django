from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.db import connection
from django.contrib import messages
from.models import resort,room,signup,Booking,reg,card

from.forms import resortform,roomForm,signupForm,availableForm,BookingForm,CardPaymentForm,ResorteditForm
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse,Http404
from datetime import datetime

# Create your views here.
def home(request):
    return render(request,'front.html')

def admi_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = reg.objects.filter(username=username, password=password).first()

        if user:
            request.session['username'] = user.username
            return redirect('resort_reg')
        else:
            return render(request, 'admi_login.html', {'error': 'Invalid login'})

    return render(request, 'admi_login.html')


def resort_reg(request):
    resort_instance = None  # Initialize the variable

    if request.method == 'POST':
        form = resortform(request.POST, request.FILES)
        if form.is_valid():
            resort_instance = form.save()
            messages.success(request, 'Resort registration completed successfully!')
            # Redirect to resort list or a page with the newly created resort
            return redirect('resort_reg')  # or another page showing the resort details
    else:
        form = resortform()

    return render(request, 'resort_reg.html', {'form': form, 'resort_instance': resort_instance})



from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import resort
from .forms import resortform

def edit_resort(request, name):
    res = get_object_or_404(resort, name=name)
    if request.method == "POST":
        form = ResorteditForm(request.POST, instance=res)
        if form.is_valid():
            form.save()
            messages.success(request, "Resort details updated successfully!")
            return redirect('resort_list')  # Change to your resort list view name
    else:
        form = ResorteditForm(instance=res)

    return render(request, 'edit_resort.html', {'form': form})



def resort_delete(request, name):
    resort_instance = get_object_or_404(resort, name=name)
    
    if request.method == 'POST':
        resort_instance.delete()
        messages.success(request, 'Resort deleted successfully!')
        return redirect('resort_list')  # Redirect to the resort list page
    
    return render(request, 'resort_confirm_delete.html', {'resort': resort_instance})



def resort_list(request):
    resorts = resort.objects.all()
    return render(request, 'resort_list.html', {'resorts': resorts})

def add(request):
    add_room = resort.objects.all()  # Fetch all users
    return render(request, 'add_room.html', {'add_room': add_room})

def room_reg(request, resort_name):
    # Retrieve the resort instance based on the resort name from the URL
    resort_instance = get_object_or_404(resort, name=resort_name)

    if request.method == 'POST':
        form = roomForm(request.POST)
        if form.is_valid():
            room_instance = form.save(commit=False)
            room_instance.resort = resort_instance  # Associate the resort with the room
            room_instance.save()
            messages.success(request, 'Room registered successfully!')
            return redirect('room_reg', resort_name=resort_name)  # Stay on the room registration page
        else:
            print(form.errors)  # Print any errors for debugging
    else:
        form = roomForm(initial={'resort_name': resort_name})

    return render(request, 'room_reg.html', {'form': form, 'resort_name': resort_name})



def room_update(request, room_id):
    room_instance = get_object_or_404(room, id=room_id)

    if request.method == 'POST':
        form = roomForm(request.POST, instance=room_instance)
        if form.is_valid():
            form.save()  # Save the updated room instance
            messages.success(request, 'Room updated successfully!')
            return redirect('room_list')  # Redirect to room list page
        else:
            print(form.errors)
    else:
        form = roomForm(instance=room_instance)

    return render(request, 'edit_room.html', {'form': form, 'room': room_instance})

def room_delete(request, room_id):
    room_instance = get_object_or_404(room, id=room_id)

    if request.method == 'POST':
        room_instance.delete()
        messages.success(request, 'Room deleted successfully!')
        return redirect('room_list')  # Redirect to room list page
    
    return render(request, 'room_confirm_delete.html', {'room': room_instance})


def room_list(request):
    rooms = room.objects.all()
    return render(request, 'room_list.html', {'rooms': rooms})


def signup_view(request):
    if request.method == 'POST':
        form = signupForm(request.POST)
        if form.is_valid():
            form.save()  # Just save the form, no hashing
            return redirect('login')
    else:
        form = signupForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = signup.objects.filter(username=username).first()

        if user and user.password == password:  # Directly compare the raw password
            request.session['user_id'] = user.id
            return redirect('check_avilable')
        else:
            error_message = "Invalid username or password"
            return render(request, 'login.html', {'error': error_message})

    return render(request, 'login.html')


def get_resorts(request):
    room_type = request.GET.get('room_type')
    resorts = resort.objects.filter(rooms__room_type=room_type).distinct().values('name')
    return JsonResponse(list(resorts), safe=False)

from datetime import datetime



def check_avilable(request):
    if request.method == 'POST':
        form = availableForm(request.POST)
        if form.is_valid():
            # Extract form data
            from_date = form.cleaned_data['from_date']
            to_date = form.cleaned_data['to_date']
            adults = form.cleaned_data['adults']
            children = form.cleaned_data['children']
            rooms = form.cleaned_data['rooms']
            room_type = form.cleaned_data['room_type']
            
            # Convert dates to string before saving in session
            from_date_str = from_date.strftime('%Y-%m-%d')  # Convert to string in 'YYYY-MM-DD' format
            to_date_str = to_date.strftime('%Y-%m-%d')  # Convert to string in 'YYYY-MM-DD' format
            
            # Calculate total days
            total_days = (to_date - from_date).days
            
            # Check for valid date range
            if total_days < 0:
                form.add_error('to_date', 'To date must be after from date.')
                return render(request, 'check_avilable.html', {'form': form})

            # Filter rooms based on room_type selected by the user
            available_rooms = room.objects.filter(room_type=room_type)

            # Check if any rooms are available for the selected type
            if not available_rooms.exists():
                form.add_error('room_type', 'No rooms available for the selected type.')
                return render(request, 'check_avilable.html', {'form': form})

            # Get resorts with available rooms of the selected room type
            resorts_with_rooms = resort.objects.filter(rooms__in=available_rooms).distinct()

            # Prepare data to pass to template: resorts with room price
            resorts_data = []
            for resort_instance in resorts_with_rooms:
                # Get the first room of the selected type for the resort
                room_instance = resort_instance.rooms.filter(room_type=room_type).first()
                if room_instance:
                    resorts_data.append({
                        'resort': resort_instance,
                        'room_price': room_instance.price,
                    })

            # Select the first available room (for booking)
            selected_room = available_rooms.first()  # Choose the first available room for simplicity

            # Save the form data to the session (store dates as strings)
            request.session['from_date'] = from_date_str
            request.session['to_date'] = to_date_str
            request.session['adults'] = adults
            request.session['children'] = children
            request.session['rooms'] = rooms
            request.session['room_type'] = room_type
            request.session['total_amount'] = total_days * rooms * selected_room.price if selected_room else 0
            request.session['total_days'] = total_days
            request.session['selected_room_price'] = selected_room.price if selected_room else 0

            context = {
                'from_date': from_date,
                'to_date': to_date,
                'adults': adults,
                'children': children,
                'rooms': rooms,
                'room_type': room_type,
                'total_days': total_days,
                'total_amount': request.session['total_amount'],
                'resorts': resorts_data,
                'selected_room': selected_room,  # Pass the selected room object to the template
            }

            return render(request, 'check_avilable.html', context)

    else:
        form = availableForm()

    return render(request, 'check_avilable.html', {'form': form})



def parse_date(date_str):
    formats = [
        "%b. %d, %Y",  # Nov. 21, 2024
        "%Y-%m-%d",    # 2024-11-21
        "%m/%d/%Y",    # 11/21/2024
        "%d-%m-%Y",    # 21-11-2024
    ]
    
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass  # Try next format
    raise ValueError(f"Invalid date format: {date_str}")

# The book_room view

from datetime import datetime



 # Ensure the user is logged in
def book_room(request, room_id):
    # Check if the user is authenticated manually
    if 'user_id' not in request.session:  # Check if the user is authenticated based on your custom session management
        return redirect('login')  # Redirect to the login page if the user is not logged in

    # Your booking logic here...
    from_date_str = request.session.get('from_date')
    to_date_str = request.session.get('to_date')
    adults = request.session.get('adults')
    children = request.session.get('children')
    rooms = request.session.get('rooms')
    room_type = request.session.get('room_type')

    if not from_date_str or not to_date_str or not adults or not children or not rooms or not room_type:
        return redirect('check_avilable')  # Redirect back to the check availability page if data is missing

    # Get the selected room based on room_id
    selected_room = get_object_or_404(room, id=room_id)

    # Convert from_date and to_date back from string to date
    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date()
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date()

    # Calculate the total amount based on the session data
    total_amount = (to_date - from_date).days * rooms * selected_room.price if selected_room else 0
    #request.session['total_amount'] = total_amount
    # Fetch the signup instance related to the user
    try:
        user_signup = signup.objects.get(id=request.session['user_id'])  # Fetch signup instance using session user_id
    except signup.DoesNotExist:
        return redirect('check_avilable')  # sIf the user does not exist, redirect to the login page

    # Save the new booking details to the Booking model
    booking = Booking.objects.create(
        user=user_signup,  # Use the signup instance here
        room=selected_room,
        from_date=from_date,
        to_date=to_date,
        rooms=rooms,
        adults=adults,
        children=children,
        total_days=(to_date - from_date).days,
        booked_amount=total_amount,
    )

    # Optionally, clear the session data after the booking is saved
    request.session.flush()

    # Redirect or render a booking confirmation page
    return redirect('booking-info', booking_id=booking.id)


def card_transaction(request, booking_id):

    # get total amount from session
    total_amount = request.session.get('total_amount', 0)

    if request.method == 'POST':
        form = CardPaymentForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # check card details using ORM
            cardd = card.objects.filter(username=username, password=password).first()

            if cardd:
                messages.success(request, 'Transaction successful!')
                return redirect('check_avilable')
            else:
                messages.error(request, 'Invalid username or password.')

    else:
        form = CardPaymentForm()

    return render(request, 'trans_page.html', {
        'form': form,
        'total_amount': total_amount
    })

def user_list_view(request):
    users = signup.objects.all()  # Fetch all users
    return render(request, 'user_list.html', {'users': users})


def booking_info_view(request, booking_id):  # Accept booking_id here
    # Fetch the booking using the provided booking_id
    booking = get_object_or_404(Booking, id=booking_id)

    # Now, you can pass the booking data to the template
    context = {
        'booking': booking
    }

    return render(request, 'booking_info.html', context)


def manage_users(request):
    users = signup.objects.all()  # Fetch all users
    return render(request, 'manage_user.html', {'users': users})


def manage_booking(request):
    # Fetch all bookings with related user, room, and resort data
    bookings = Booking.objects.select_related('user', 'room', 'room__resort').all()  # Optimize queries with select_related

    # Pass the bookings to the template
    return render(request, 'manage_booking.html', {'bookings': bookings})