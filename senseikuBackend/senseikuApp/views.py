from json.decoder import JSONDecodeError
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Student,Tutor,Course
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import json



@csrf_exempt
def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "password":data['password']
    }
    userExist = Tutor.objects.filter(username=loginDict['username'],password=loginDict['password']).exists()
    if userExist:
        return JsonResponse(loginDict, status=200)
    else:
        return JsonResponse(loginDict, status=404)
@csrf_exempt
def loginStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "password":data['password']
    }
    userExist = Student.objects.filter(username=loginDict['username'],password=loginDict['password']).exists()
    if userExist:
        return JsonResponse(loginDict, status=200)
    else:
        return JsonResponse(loginDict, status=404)
@csrf_exempt
def signupTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "name":data['username'],
        "password":data['password']
    }
    try:
        Tutor.objects.create(username=loginDict['username'],password=loginDict['password'])
        return JsonResponse(loginDict)
    except IntegrityError:
        return JsonResponse(loginDict, status=404)
@csrf_exempt
def signupStudent(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "name":data['username'],
        "password":data['password']
    }
    try:
        Student.objects.create(username=loginDict['username'],password=loginDict['password'])
        return JsonResponse(loginDict)
    except IntegrityError:
        return JsonResponse(loginDict, status=404)

@csrf_exempt
def getNewCourse(request):
    courseList=get_list_or_404(Course)
    courseData=serializers.serialize('json', courseList, fields=('id','course_name','description','pricing','tutor_id'))
    return HttpResponse(courseData)
