from json.decoder import JSONDecodeError
from django.contrib import auth
from django.core.checks import messages
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course, Location
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

@csrf_exempt
def logout(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=User.objects.filter(username=data['username']).exists()
    logoutDict={"username":data['username']}
    if isExist:
        user=User.objects.get(username=data['username'])
        Token.objects.filter(user=user).delete()
        message="Logout berhasil"
        logoutDict.update({'message': message})
        return JsonResponse(logoutDict,status=200)
    message="Logout gagal"
    logoutDict.update({'message': message})
    return JsonResponse(logoutDict,status=404)

@csrf_exempt
def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=exist(data['username'],data['password'])
    role="tutor"
    token=" "
    if isExist:
        user=User.objects.get(username=data['username'])
        if user.groups.filter(name='tutor').exists():
            token=Token.objects.get_or_create(user=user)
            message="Login berhasil"
        else:
            message = "Tidak terdaftar sebagai tutor"
            isExist=False
    else:
        message="Username/Password tidak terdaftar"
    current_time = datetime.now() 
    loginDict = {
        "isAuth":isExist,
        "username":data['username'],
        "token":str(token[0]),
        "message":message,
        "currentTime":current_time,
        "role":role
    }
    return JsonResponse(loginDict,safe=False)

@csrf_exempt
def loginStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=exist(data['username'],data['password'])
    token=" "
    role="student"
    if isExist:
        user=User.objects.get(username=data['username'])
        if user.groups.filter(name='student').exists():
            token=Token.objects.get_or_create(user=user)
            message="Login berhasil"
        else:
            message = "Tidak terdaftar sebagai student"
            isExist=False

    else:
        message="Username/Password tidak terdaftar"
    current_time = datetime.now() 
    loginDict = {
        "isAuth":isExist,
        "username":data['username'],
        "token":str(token[0]),
        "message":message,
        "currentTime":current_time,
        "role":role
    }
    return JsonResponse(loginDict,safe=False)

@csrf_exempt
def signupTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=User.objects.filter(username=data['username']).exists()
    signupDict={"username":data['username']}
    if isExist:
        message="User sudah terdaftar"
        signupDict.update({'message': message})
        return JsonResponse(signupDict,status=404)
    user = User.objects.create_user(username=data['username'],first_name=data['first_name'],
                                    email=data['email'],password=data['password'])
    group = Group.objects.get(name='tutor')
    user.groups.add(group)
    message="Signup berhasil"
    signupDict.update({'message': message})
    return JsonResponse(signupDict,status=200)

@csrf_exempt
def signupStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    isExist=User.objects.filter(username=data['username']).exists()
    signupDict={"username":data['username']}
    if isExist:
        message="User sudah terdaftar"
        signupDict.update({'message': message})
        return JsonResponse(signupDict,status=404)
    user = User.objects.create_user(username=data['username'],first_name=data['first_name'],
                                    email=data['email'],password=data['password'])
    group = Group.objects.get(name='student')
    user.groups.add(group)
    message="Signup berhasil"
    signupDict.update({'message': message})
    return JsonResponse(signupDict,status=200)

def profileTutor(request):
    username = request.GET.get('username')
    user_filter = User.objects.filter(username=username)
    user_get = User.objects.get(username=username)
    if not user_get.groups.filter(name='tutor').exists():
        message = "Tidak terdaftar sebagai tutor"        
        profile_dict = {
            'username': username,
            'message': message
        }
        return JsonResponse(profile_dict,status=404)
    profile_dict = serializers.serialize('json', user_filter, fields=('username', 'email', 'first_name'))
    return HttpResponse(profile_dict)

def profileStudent(request):
    username = request.GET.get('username')
    user_filter = User.objects.filter(username=username)
    user_get = User.objects.get(username=username)
    if not user_get.groups.filter(name='student').exists():
        message = "Tidak terdaftar sebagai student"        
        profile_dict = {
            'username': username,
            'message': message
        }
        return JsonResponse(profile_dict,status=404)
    profile_dict = serializers.serialize('json', user_filter, fields=('username', 'email', 'first_name'))
    return HttpResponse(profile_dict)

@csrf_exempt
def editProfile(request):
    data=json.loads(request.body.decode('utf-8')) #username,password, first_name, email, latitude, longitude, timestamp
    editDict={
        "message":"edit success"
    }
    isExist=User.objects.filter(username=data['username']).exists()
    if isExist:
        if data['password'] != "":
            User.objects.filter(username=data['username']).update(
                password=data['password']
            )
        if data['first_name'] != "":
            User.objects.filter(username=data['username']).update(
                first_name=data['first_name']
            )
        if data['email'] != "":
            User.objects.filter(username=data['username']).update(
                email=data['email']
            )
        if data['latitude'] != "":
            Location.objects.filter(username=data['username']).update(
                latitude=data['latitude']
            )
        if data['longitude'] != "":
            Location.objects.filter(username=data['username']).update(
                longitude=data['longitude']
            )
        if data['timestamp'] != "":
            Location.objects.filter(username=data['username']).update(
                timestamp=data['timestamp']
            )
        return JsonResponse(editDict,status=200)
    editDict['message']="edit failed"
    return JsonResponse(editDict,status=404)
