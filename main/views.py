import decimal
from decimal import *
import floor as floor
import gender as gender
import phone as phone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth import authenticate, login
from django.urls import path
import datetime
from datetime import datetime, timedelta
# Create your views here.
from .models import *
from django.db.models import Sum


# ======== Price ECTS =========
ects_price = 250


# ========== INDEX ==========
def index(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return HttpResponseRedirect('dashboard')
        else:
            return HttpResponseRedirect('/')
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect('dashboard')
        else:
            return render(request, 'main/login.html')


# ========== DASHBOARD ==========
def dashboard(request):
    if request.user.is_authenticated:
        percentage = dashboard_percentage()
        client = dashboard_clients()
        available_rooms = dashboard_available_rooms()
        revenue = dashboard_revenue()
        print(revenue)
        context = {
            'percentage': percentage,
            'client': client,
            'available_rooms': available_rooms,
            'revenue': revenue
        }
        return render(request, 'main/dashboard.html', context=context)
    else:
        return HttpResponseRedirect('/')


def dashboard_percentage():
    rooms = Room.objects.all()
    not_available_rooms = rooms.filter(status='N')
    all_percentage = int((len(not_available_rooms) * 100) / len(rooms))


    family_rooms = Room.objects.filter(room_class__class_name = "Family")
    family_not_available_rooms = family_rooms.filter(status='N')
    family_percentage = int((len(family_not_available_rooms) * 100) / len(family_rooms))

    first_rooms = Room.objects.filter(room_class__class_name="First class")
    first_not_available_rooms = first_rooms.filter(status='N')
    first_percentage = int((len(first_not_available_rooms) * 100) / len(first_rooms))

    lux_rooms = Room.objects.filter(room_class__class_name="Lux")
    lux_not_available_rooms = lux_rooms.filter(status='N')
    lux_percentage = int((len(lux_not_available_rooms) * 100) / len(lux_rooms))

    return {
        'all_percentage': all_percentage,
        'family_percentage': family_percentage,
        'first_percentage': first_percentage,
        'lux_percentage': lux_percentage
    }


def dashboard_clients():
    clients = Client.objects.all()
    null_clients = Client.objects.filter(room=None)
    return len(clients)  - len(null_clients)


def dashboard_available_rooms():
    all_available_rooms = Room.objects.filter(status='A')
    lux_available_rooms = Room.objects.filter(room_class__class_name="Lux").filter(status='A')
    family_available_rooms = Room.objects.filter(room_class__class_name="Family").filter(status='A')
    bisiness_available_rooms = Room.objects.filter(room_class__class_name="Bisiness").filter(status='A')
    first_available_rooms = Room.objects.filter(room_class__class_name="First class").filter(status='A')
    honeymoon_available_rooms = Room.objects.filter(room_class__class_name="Honeymoon").filter(status='A')
    return {
        'all': len(all_available_rooms),
        'lux': len(lux_available_rooms),
        'family': len(family_available_rooms),
        'bisiness': len(bisiness_available_rooms),
        'first': len(first_available_rooms),
        'honeymoon': len(honeymoon_available_rooms)
    }


def dashboard_revenue():
    current_datetime = datetime.today()
    one = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=7)).year,
                                 date_paid__month=(current_datetime - timedelta(days=7)).month,
                                 date_paid__day=(current_datetime - timedelta(days=7)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=7)).strftime('%d-%m-%Y')
    }

    two = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=6)).year,
                                 date_paid__month=(current_datetime - timedelta(days=6)).month,
                                 date_paid__day=(current_datetime - timedelta(days=6)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=6)).strftime('%d-%m-%Y')
    }

    three = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=5)).year,
                                  date_paid__month=(current_datetime - timedelta(days=5)).month,
                                  date_paid__day=(current_datetime - timedelta(days=5)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=5)).strftime('%d-%m-%Y')
    }

    four = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=4)).year,
                                  date_paid__month=(current_datetime - timedelta(days=4)).month,
                                  date_paid__day=(current_datetime - timedelta(days=4)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=4)).strftime('%d-%m-%Y')
    }

    five = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=3)).year,
                                  date_paid__month=(current_datetime - timedelta(days=3)).month,
                                  date_paid__day=(current_datetime - timedelta(days=3)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=3)).strftime('%d-%m-%Y')
    }

    six = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=2)).year,
                                 date_paid__month=(current_datetime - timedelta(days=2)).month,
                                 date_paid__day=(current_datetime - timedelta(days=2)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=2)).strftime('%d-%m-%Y')
    }

    seven = {
        'cost': Payment.objects.filter(date_paid__year=(current_datetime - timedelta(days=1)).year,
                                   date_paid__month=(current_datetime - timedelta(days=1)).month,
                                   date_paid__day=(current_datetime - timedelta(days=1)).day).aggregate(Sum('cost')),
        'date': (current_datetime - timedelta(days=1)).strftime('%d-%m-%Y')
    }

    return {
        'one': one,
        'two': two,
        'three': three,
        'four': four,
        'five': five,
        'six': six,
        'seven': seven
    }

# ========== REGISTRATION ==========
def registration(request):
    available_rooms_list = Room.objects.filter(status='A')
    if request.user.is_authenticated:
        if request.method == 'POST':
            filter_class = request.POST.get('class')
            filter_amount = request.POST.get('amount')
            filter_floor = request.POST.get('floor')

            if filter_class != 'All':
                available_rooms_list = available_rooms_list.filter(room_class=filter_class)
            if filter_amount != 'All':
                available_rooms_list = available_rooms_list.filter(room_amount=filter_amount)
            if filter_floor != 'All':
                available_rooms_list = available_rooms_list.filter(floor=filter_floor)

        context = {
            'rooms_list': available_rooms_list,
        }
        return render(request, 'main/registration_rooms.html', context=context)
    else:
        return HttpResponseRedirect('/')


def registration_room(request, pk):
    if request.user.is_authenticated:
        room = Room.objects.get(pk=pk)
        clients = Client.objects.filter(room=pk)
        search_clients = 0
        if request.method == 'POST':
            search_name = request.POST.get('search_name')
            search_surname = request.POST.get('search_surname')

            search_clients = Client.objects.all()
            if search_name != '':
                search_clients = search_clients.filter(first_name=search_name)
            if search_surname != '':
                search_clients = search_clients.filter(last_name=search_surname)

        context = {
            'room': room,
            'clients': clients,
            'search_clients': search_clients
        }
        return render(request, 'main/reg_room.html', context=context)
    else:
        return HttpResponseRedirect('/')


def add_client(request, pk):
    if request.method == 'POST':
        room = Room.objects.get(pk=pk)
        name = request.POST.get('name')
        surname = request.POST.get('surname')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        gender = request.POST.get('gender')

        if not Registeration.objects.filter(room=pk).exists():
            Registeration(
                room=room,
            ).save()

        Room.objects.filter(id=room.id).update(status="N")
        registration = Registeration.objects.get(room=pk)
        Client(
            first_name=name,
            last_name=surname,
            email=email,
            phone=phone,
            gender=gender,
            room=room,
            registration=registration
        ).save()
    else:
        return HttpResponseRedirect('/')

    room = Room.objects.get(pk=pk)
    clients = Client.objects.filter(room=pk)
    context = {
        'room': room,
        'clients': clients
    }
    return render(request, 'main/reg_room.html', context=context)

def add_search_client(request, pk, id):

    room = Room.objects.get(pk=pk)
    search_clients = Client.objects.filter(pk=id)

    print(room)
    print(search_clients)

    if not Registeration.objects.filter(room=pk).exists():
        Registeration(
            room=room,
        ).save()

    Room.objects.filter(id=room.id).update(status="N")
    registration = Registeration.objects.get(room=pk)
    search_clients.update(registration=registration)
    search_clients.update(room=room)

    clients = Client.objects.filter(room=pk)
    context = {
        'room': room,
        'clients': clients
    }
    return render(request, 'main/reg_room.html', context=context)


# ========== ROOMS ==========
def rooms(request):
    rooms_list = Room.objects.all()
    if request.user.is_authenticated:
        if request.method == 'POST':
            filter_status = request.POST.get('status')
            filter_class = request.POST.get('class')
            filter_amount = request.POST.get('amount')
            filter_floor = request.POST.get('floor')

            if filter_status != 'All':
                rooms_list = rooms_list.filter(status=filter_status)
            if filter_class != 'All':
                rooms_list = rooms_list.filter(room_class=filter_class)
            if filter_amount != 'All':
                rooms_list = rooms_list.filter(room_amount=filter_amount)
            if filter_floor != 'All':
                rooms_list = rooms_list.filter(floor=filter_floor)

        context = {
            'rooms': rooms_list,
        }
        return render(request, 'main/rooms.html', context=context)
    else:
        return HttpResponseRedirect('/')


def room_page(request, pk):
    if request.user.is_authenticated:
        room = Room.objects.get(pk=pk)
        clients = Client.objects.filter(room=pk)
        context = {
            'room': room,
            'clients': clients
        }
        return render(request, 'main/room_page.html', context=context)
    else:
        return HttpResponseRedirect('/')


def add_room(request):
    room_number = request.POST.get('number')
    room_class = RoomClass.objects.get(pk=int(request.POST.get('class')))
    floor = request.POST.get('floor')
    amount = request.POST.get('amount')

    # calculate ects
    getcontext().prec = 2
    ects = room_class.cost + decimal.Decimal(int(amount) * 0.2)

    Room(
        room_number = room_number,
        room_class = room_class,
        floor = floor,
        room_amount = amount,
        ects = ects,
        status = 'A'
    ).save()
    return HttpResponseRedirect('/rooms')


def remove_room(request, pk):
    Room.objects.filter(pk=pk).delete()
    return HttpResponseRedirect('/rooms')


# ========== CLIENTS ==========
def clients(request):
    if request.user.is_authenticated:
        clients = Client.objects.all()

        if request.method == 'POST':
            room = request.POST.get('room')
            if room != '':
                clients = clients.filter(room__room_number=room)

        context = {
            'clients': clients
        }
        return render(request, 'main/clients.html', context=context)
    else:
        return HttpResponseRedirect('/')


# ========== PAYMENT ==========
def payment(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            room = request.POST.get('room')
            if room != '':
                if Registeration.objects.filter(room__room_number=room).exists():
                    registration = Registeration.objects.get(room__room_number=room)
                    room_id = registration.room.pk

                    url = '/payment/room/' + str(room_id)
                    return HttpResponseRedirect(url)
        context = {}
        return render(request, 'main/payment.html', context=context)
    else:
        return HttpResponseRedirect('/')


def payment_room(request, pk):
    registration = Registeration.objects.get(room=pk)
    room = Room.objects.get(pk=pk)
    clients = Client.objects.filter(room=pk)

    entered_datetime =  registration.date_entered
    current_datetime = datetime.now()

    days = int(current_datetime.strftime("%d")) - int(entered_datetime.strftime("%d"))
    total_ects = room.ects * days

    total_price = total_ects * ects_price
    context = {
        'current_datetime': current_datetime,
        'entered_datetime': entered_datetime,
        'total_ects': total_ects,
        'total_price': total_price,
        'registration': registration,
        'room': room,
        'clients': clients
    }
    return render(request, 'main/payment_room.html', context=context)


def pay(request, pk):
    registration = Registeration.objects.get(pk=pk)

    entered_datetime = registration.date_entered
    current_datetime = datetime.now()

    days = int(current_datetime.strftime("%d")) - int(entered_datetime.strftime("%d"))
    total_ects = registration.room.ects * days

    total_price = total_ects * ects_price

    History(
        room=registration.room,
        date_entered=registration.date_entered,
        date_left=current_datetime
    ).save()

    new_history = History.objects.order_by('-pk')[0]
    new_payment = Payment(
        registration = new_history,
        date_paid = current_datetime,
        cost = total_price
    ).save()

    Room.objects.filter(pk=registration.room.pk).update(status='A')
    room = Room.objects.filter(pk=registration.room.pk)
    Client.objects.filter(registration = registration).update(room = None)
    registration.delete()

    return HttpResponseRedirect('/payment')


# ========== HISTORY ==========
def history(request):
    if request.user.is_authenticated:
        historys = Payment.objects.all()
        if request.method == 'POST':
            at = request.POST.get('at')
            to = request.POST.get('to')
            if at and to:
                historys = Payment.objects.filter(registration__date_entered__range=(at, to))

        context = {
            'historys': historys
        }
        return render(request, 'main/history.html', context=context)
    else:
        return HttpResponseRedirect('/')


