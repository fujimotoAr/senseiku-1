from enum import unique
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class Phone(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    username=models.ForeignKey(User,to_field="username",db_column="username",default="",on_delete=models.CASCADE)
    phone_number=models.CharField(max_length=100)

class Location(models.Model):
    username=models.ForeignKey(User,to_field="username",db_column="username",default="",on_delete=models.CASCADE)
    latitude=models.FloatField(null=True)
    longitude=models.FloatField(null=True)
    timestamp=models.IntegerField(null=True)

class Course(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pricing = models.IntegerField()
    tutor_username = models.ForeignKey(User,to_field="username",db_column="username",default="",on_delete=models.CASCADE)

class Schedule(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    tutor_username = models.ForeignKey(User,to_field="username",db_column="username",default="",on_delete=models.CASCADE)
    date = models.CharField(max_length=100,default='01-01-1970')
    hour_start = models.CharField(max_length=100,default="7:30")
    hour_finish = models.CharField(max_length=100,default="9:30")
    availability = models.BooleanField(default=True)
    course_id = models.IntegerField(null=True)
    finish = models.BooleanField(default=False)

class Review(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    student_id = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.FloatField(default=0.0)

class Transaction(models.Model):
    id=models.AutoField(primary_key=True,unique=True)
    student_username = models.ForeignKey(User,to_field="username",db_column="username",default="",on_delete=models.CASCADE)
    timestamp = models.IntegerField()
    total_price=models.IntegerField(default=0)
    status = models.CharField(max_length=100, default="not verified")
    gopay = models.CharField(max_length=300, default="")

class Cart(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    student_username = models.ForeignKey(User,to_field="username",db_column="username",default="",on_delete=models.CASCADE)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    schedule_id = models.ForeignKey(Schedule,on_delete=models.CASCADE)
    course_price = models.IntegerField(default=0)
    transport_price = models.IntegerField(default=0)
    total_price = models.IntegerField(default=0)
    #transaction_id=models.ForeignKey(Transaction, on_delete=models.CASCADE)

class Tracker(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    username = models.ForeignKey(User,to_field="username",db_column="username",default="guest",on_delete=models.CASCADE)
    event = models.IntegerField()
    timestamp = models.IntegerField()

