from json.decoder import JSONDecodeError
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



@csrf_exempt
def loginTutor(request):
    data=json.loads(request.body.decode('utf-8'))
    loginDict={
        "username":data['username'],
        "password":data['password']
    }
    

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


@csrf_exempt
def getNewCourse(request):
    courseList=get_list_or_404(Course)
    courseData=serializers.serialize('json', courseList, fields=('id','course_name','description','pricing','tutor_id'))
    return HttpResponse(courseData)

csrf_exempt
def addCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "id":data['id'],
        "course_name":data['nama'],
        "description":data['deskripsi'],
        "pricing":data['harga'],
        "tutor_id":data['tutor_id']
    }
    try:
        Course.objects.create(
            id=courseDict['id'],
            course_name=courseDict['course_name'],
            description=courseDict['description'],
            pricing=courseDict['pricing'],
            tutor_id_id=courseDict['tutor_id']
        )
        return JsonResponse(courseDict)
    except IntegrityError:
        return JsonResponse(courseDict, status=404)
'''
mohon maaf pak, saya masih mengalami integrityError


csrf_exempt
def updateCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "id":data['id'],
        "course_name":data['nama'],
        "description":data['deskripsi'],
        "pricing":data['harga'],
        "tutor_id":data['tutor_id']
    }
    
    Course.objects.update_or_create(
        id=courseDict['id'],
        course_name=courseDict['course_name'],
        description=courseDict['description'],
        pricing=courseDict['pricing'],
        tutor_id_id=courseDict['tutor_id']
    )
    return JsonResponse(courseDict)
'''