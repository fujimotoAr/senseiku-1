from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User


class Course(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pricing = models.IntegerField()
    tutor_id = models.ForeignKey(User,on_delete=models.CASCADE)

    
class Schedule(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    day = models.CharField(max_length=100)
    hour = models.TimeField()

class Review(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_id = models.ForeignKey(Course,on_delete=models.CASCADE)
    student_id = models.ForeignKey(User,on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.FloatField(default=0.0)

