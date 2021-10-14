from json.decoder import JSONDecodeError
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course, Schedule,Review
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def getNewCourse(request):
    courseList=Course.objects.all().order_by('-id')[:5]
    courseData=serializers.serialize('json', courseList, fields=('id','course_name','description','pricing','tutor_id'))
    return HttpResponse(courseData)

@csrf_exempt
def getAllCourse(request):
    courseList=Course.objects.all().order_by('id')
    courseData=serializers.serialize('json', courseList, fields=('id','course_name','description','pricing','tutor_id'))
    return HttpResponse(courseData)

@csrf_exempt
def addCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "course_name":data['course_name'],
        "description":data['description'],
        "pricing":data['pricing'],
        "tutor_username":data['tutor_username'],
    }
    try:
        Course.objects.create(
            course_name=courseDict['course_name'],
            description=courseDict['description'],
            pricing=courseDict['pricing'],
            tutor_username_id=courseDict['tutor_username']
        )
        return JsonResponse(courseDict)
    except IntegrityError:
        return JsonResponse(courseDict, status=404)

@csrf_exempt
def deleteCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "id":data['id'],
        "message":""
    }
    if Course.objects.filter(id=courseDict['id']).exists():
        Course.objects.filter(id=courseDict['id']).delete()
        Schedule.objects.filter(course_id=courseDict['id']).delete()
        Review.objects.filter(course_id=courseDict['id']).delete()
        courseDict.update({
            "message":"Delete success"
        })
        return JsonResponse(courseDict)
    else:
        courseDict.update({
            "message":"Delete failed, id not exist"
        })
        return JsonResponse(courseDict, status=404)

@csrf_exempt
def addSchedule(request):
    data=json.loads(request.body.decode('utf-8'))
    
    scheduleDict={
        "course_id":data['course_id'],
        "day":data['day'],
        "hour":data['hour'],
        "message":""
    }
    try:
        Schedule.objects.create(
            course_id_id=scheduleDict['course_id'],
            day=scheduleDict['day'],
            hour=scheduleDict['hour'],
        )
        return JsonResponse(scheduleDict)
    except IntegrityError:
        return JsonResponse(scheduleDict, status=404)

@csrf_exempt
def deleteSchedule(request):
    data=json.loads(request.body.decode('utf-8'))
    scheduleDict={
        "id":data['id'],
        "message":""
    }
    if Schedule.objects.filter(id=scheduleDict['id']).exists():
        Schedule.objects.filter(id=scheduleDict['id']).delete()
        scheduleDict.update({
            "message":"Delete success"
        })
        return JsonResponse(scheduleDict)
    else:
        scheduleDict.update({
            "message":"Delete failed, id not exist"
        })
        return JsonResponse(scheduleDict, status=404)