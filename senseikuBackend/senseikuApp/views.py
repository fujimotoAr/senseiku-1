from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Student,Tutor,Course
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import json

def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDIct={
        "username":data['username'],
        "password":data['password']
    }
    userExist = Tutor.objects.filter(username=loginDIct['username'],password=loginDIct['password']).exists()
    if userExist:
        return JsonResponse(loginDIct)
    else:
        return HttpResponse('<H1>fail!</H1>', status=404)

def loginStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDIct={
        "username":data['username'],
        "password":data['password']
    }
    userExist = Student.objects.filter(username=loginDIct['username'],password=loginDIct['password']).exists()
    if userExist:
        return JsonResponse(loginDIct)
    else:
        return HttpResponse('<H1>fail!</H1>', status=404)

def signupTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDIct={
        "username":data['username'],
        "name":data['username'],
        "password":data['password']
    }
    try:
        Tutor.objects.create(username=loginDIct['username'],password=loginDIct['password'])
        return JsonResponse(loginDIct)
    except IntegrityError:
        return HttpResponse('<H1>fail!</H1>', status=404)

def signupStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDIct={
        "username":data['username'],
        "name":data['username'],
        "password":data['password']
    }
    try:
        Student.objects.create(username=loginDIct['username'],password=loginDIct['password'])
        return JsonResponse(loginDIct)
    except IntegrityError:
        return HttpResponse('<H1>fail!</H1>', status=404)

@csrf_exempt
def getNewCourse(request):
    """
    BAWAH INI SISA KODINGAN PROG WEB

    data = json.loads(request.body.decode('utf-8'))
    output_dictionary={
        "id":data['id'],
        "username":data['username']
     }
    hitung_true=0
    for i in range(1,6): #1 sampai 5
        s="q"+str(i) #q1, q2, ...
        cur=get_list_or_404(Questions,quiz_id=data['id'])
        for j in cur:
            if int(j.id) % 5 == int(i) % 5: #question.id: 1,2,3,4,5,6,7
                if(data[s]==j.corrans):
                    output_dictionary.update({s:"true"})
                    hitung_true+=1
                else:
                    output_dictionary.update({s:"false"})
    
    output_dictionary.update({"score":hitung_true * 20})
    
    #MASUKIN KE DATABASE
    try:
        add_database=Answer.objects.create(username=data['username'],quiz_id=data['id'],score=output_dictionary['score'])
    except IntegrityError: #jika ada duplicate
        add_database=Answer.objects.update(username=data['username'],quiz_id=data['id'],score=output_dictionary['score'])

    ###

    
    return JsonResponse(output_dictionary)
    """