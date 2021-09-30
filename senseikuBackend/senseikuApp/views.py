from json.decoder import JSONDecodeError
from django.contrib import auth
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from datetime import datetime
import json

def exist(usernameInput,passwordInput):
    auth=authenticate(username=usernameInput,password=passwordInput)
    if(auth is not None):
        return True
    else:
        return False

@csrf_exempt
def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=exist(data['username'],data['password'])
    message=""
    if isExist:
        user=User.objects.get(username=data['username'])
        token=Token.objects.get_or_create(user=user)
        message="Login berhasil"
    else:
        token=" "
        message="Username/Password tidak terdaftar"

    current_time = datetime.now() 
    loginDict={
        "isAuth":isExist,
        "username":data['username'],
        "token":str(token[0]),
        "message":message,
        "currentTime":current_time
    }
    return JsonResponse(loginDict,safe=False)
    


@csrf_exempt
def loginStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=exist(data['username'],data['password'])
    message=""
    if isExist:
        user=User.objects.get(username=data['username'])
        token=Token.objects.get_or_create(user=user)
        message="Login berhasil"
    else:
        token=" "
        message="Username/Password tidak terdaftar"

    current_time = datetime.now() 
    loginDict={
        "isAuth":isExist,
        "username":data['username'],
        "token":str(token[0]),
        "message":message,
        "currentTime":current_time
    }
    return JsonResponse(loginDict,safe=False)

@csrf_exempt
def signupTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=User.objects.filter(username=data['username']).exists()
    global message
    if isExist:
        message="User sudah terdaftar"
    else:
        message="Signup berhasil"
    signupDict={
        "username":data['username'],
        "message":message
    }
    if not isExist:
        User.objects.create_user(username=data['username'],password=data['password'])
    else:
        return JsonResponse(signupDict,status=404)
    return JsonResponse(signupDict,status=200)

@csrf_exempt
def signupStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=User.objects.filter(username=data['username']).exists()
    global message
    if isExist:
        message="User sudah terdaftar"
    else:
        message="Signup berhasil"
    signupDict={
        "username":data['username'],
        "message":message
    }
    if not isExist:
        User.objects.create_user(username=data['username'],password=data['password'])
    else:
        return JsonResponse(signupDict,status=404)
    return JsonResponse(signupDict,status=200)