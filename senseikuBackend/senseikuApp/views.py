from json.decoder import JSONDecodeError
from django.contrib import auth
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User, Group
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

def is_member(user, group_name):
    return user.groups.filter(name=group_name).exists()

@csrf_exempt
def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=exist(data['username'],data['password'])
    message=""
    loginDict={
        "isAuth":isExist,
        "username":data['username'],
    }
    if isExist:
        user=User.objects.get(username=data['username'])
        if not is_member(user, 'tutor'):
            message = "Tidak terdaftar sebagai tutor"
            loginDict.update({"message": message})
            return JsonResponse(loginDict, status=404)
        token=Token.objects.get_or_create(user=user)
        message="Login berhasil"
    else:
        token=" "
        message="Username/Password tidak terdaftar"

    current_time = datetime.now() 
    loginDict.update({
        "token":str(token[0]),
        "message":message,
        "currentTime":current_time
    })
    return JsonResponse(loginDict,safe=False)

@csrf_exempt
def loginStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=exist(data['username'],data['password'])
    message=""
    loginDict = {
        "isAuth":isExist,
        "username":data['username'],
    }
    if isExist:
        user=User.objects.get(username=data['username'])
        if not is_member(user, 'student'):
            message = "Tidak terdaftar sebagai student"
            loginDict.update({"message": message})
            return JsonResponse(loginDict,status=404)
        token=Token.objects.get_or_create(user=user)
        message="Login berhasil"
    else:
        token=" "
        message="Username/Password tidak terdaftar"

    current_time = datetime.now() 
    loginDict.update({
        "token":str(token[0]),
        "message":message,
        "currentTime":current_time
    })
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
        user = User.objects.create_user(username=data['username'],password=data['password'])
        group = Group.objects.get(name='tutor')
        user.groups.add(group)
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
        user = User.objects.create_user(username=data['username'],password=data['password'])
        group = Group.objects.get(name='student')
        user.groups.add(group)
    else:
        return JsonResponse(signupDict,status=404)
    return JsonResponse(signupDict,status=200)