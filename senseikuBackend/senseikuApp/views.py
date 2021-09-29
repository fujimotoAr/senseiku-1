from json.decoder import JSONDecodeError
from django.contrib import auth
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course
from .viewsProduct import getNewCourse,addCourse
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import json


'''
@csrf_exempt
def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "password":data['password']
    }
    temp=authenticate(username=loginDict['username'],password=loginDict['password'])
    return HttpResponse(temp)
'''

@csrf_exempt
def loginStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "password":data['password']
    }
    



@csrf_exempt
def signupTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    User.objects.create_user(username=data['username'],password=data['password'])
    return JsonResponse(data,status=200)

    


@csrf_exempt
def signupStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    User.objects.create_user(username=data['username'],password=data['password'])
    return JsonResponse(data,status=200)

