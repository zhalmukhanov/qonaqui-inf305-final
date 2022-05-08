import room
from django.db import models
from django.db.models import SET_NULL
from .models import *

from django.utils import timezone
# Create your models here.


class RoomClass(models.Model):
    class_name = models.CharField(max_length=50)
    cost = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return self.class_name


class Room(models.Model):
    room_number = models.IntegerField()
    floor = models.IntegerField()
    status = models.CharField(max_length=1)
    room_class = models.ForeignKey(RoomClass, on_delete=models.SET_NULL, blank=True, null=True)
    room_amount = models.IntegerField()
    ects = models.DecimalField(max_digits=19, decimal_places=1)

    def __str__(self):
        return self.status + " " + str(self.room_number) + " | " + self.room_class.class_name

class Registeration(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date_entered = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.room.room_number) + " | " + self.room.room_class.class_name

class Client(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=50)

    genders = [('Male', 'Male'),
               ('Female', 'Female')]
    gender = models.CharField(choices=genders, max_length=10)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, blank=True, null=True)
    registration = models.ForeignKey(Registeration, on_delete=models.SET_NULL, blank=True, null=True)


    def __str__(self):
        return self.first_name + " " + self.last_name


class History(models.Model):
    room = models.ForeignKey(Room, on_delete=SET_NULL, blank=True, null=True)
    date_entered = models.DateTimeField()
    date_left = models.DateTimeField()

    def __str__(self):
        return str(self.room.room_number)

    def date_entered_format(self):
        return self.date_left.strftime('%d-%m-%Y')

    def date_left_format(self):
        return self.date_left.strftime('%d-%m-%Y')


class Payment(models.Model):
    registration = models.ForeignKey(History, on_delete=models.CASCADE)
    date_paid = models.DateTimeField(auto_now_add=True)
    cost = models.DecimalField(max_digits=19, decimal_places=2)

    def __str__(self):
        return str(self.registration.room.room_number) + "  Payment id: " + str(self.id)
