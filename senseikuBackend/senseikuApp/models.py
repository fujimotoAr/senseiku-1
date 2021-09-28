from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

class Student(models.Model):
    username = models.CharField(primary_key=True,max_length=100, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)

    

class Tutor(models.Model):
    username = models.CharField(primary_key=True,max_length=100, unique=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=1000)
    #quiz=models.ForeignKey(Quiz,on_delete=models.CASCADE)
    

class Course(models.Model):
    id = models.AutoField(primary_key=True,unique=True)
    course_name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    pricing = models.IntegerField()
    tutor_id = models.ForeignKey(Tutor,on_delete=models.CASCADE)

    
