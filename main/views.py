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
# Create your views here.
from .models import *


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

        context = {

        }
        return render(request, 'main/dashboard.html', context=context)
    else:
        return HttpResponseRedirect('/')


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
        context = {
            'room': room,
            'clients': clients
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
    current_datetime = datetime.datetime.now()

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
    current_datetime = datetime.datetime.now()

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


