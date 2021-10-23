from json.decoder import JSONDecodeError
from django.contrib.auth.models import User
from django.db.models import fields
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course, Schedule,Review,Tracker
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict

import json

def getNewCourse(request):
    courseList=[*Course.objects.order_by('-id')[:5], *User.objects.order_by('-course__id')[:5]]
    courseData=serializers.serialize(
        'json', courseList,
        fields=('id','course_name','description','pricing','tutor_username','username','first_name')
    )
    return HttpResponse(courseData)

def getMyCourse(request):
    data = request.GET.get('username')
    courseList = Course.objects.filter(tutor_username=data)
    courseData = serializers.serialize(
        'json', courseList, fields=('id','course_name','description','pricing','tutor_username')
    )
    return HttpResponse(courseData)

def getAllCourse(request):
    courseList=[*Course.objects.order_by('id'), *User.objects.order_by('course__id')]
    courseData=serializers.serialize(
        'json', courseList,
        fields=('id','course_name','description','pricing','tutor_username','username','first_name')
    )
    return HttpResponse(courseData)

def getCourseDetail(request):
    data = request.GET.get('id')
    selectedCourse = [
        *Course.objects.filter(id=data),
        *User.objects.filter(course__id=data),
        *Schedule.objects.filter(course_id=data)
    ]
    serialized = serializers.serialize(
        'json', selectedCourse,
        fields=('id','course_name','description','pricing','first_name','day','hour_start','hour_finish')
    )
    return HttpResponse(serialized)

@csrf_exempt
def addCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "course_name":data['course_name'],
        "description":data['description'],
        "pricing":data['pricing'],
        "tutor_username":data['tutor_username'],
        "message":"addCourse success"
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
        courseDict.update(
            {
                "message":"addCourse failed, id already exists"
            }
        )
        return JsonResponse(courseDict, status=404)

@csrf_exempt
def updateCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "id":data['id'],
        "course_name":data['course_name'],
        "description":data['description'],
        "pricing":data['pricing'],
        "tutor_username":data['tutor_username'],
        "message":"Update success"
    }
    if Course.objects.filter(id=courseDict['id']).exists():
        Course.objects.filter(id=courseDict['id']).update(
            course_name=courseDict['course_name'],
            description=courseDict['description'],
            pricing=courseDict['pricing'],
            tutor_username_id=courseDict['tutor_username']
        )
        return JsonResponse(courseDict)
    else:
        courseDict.update({
            "message":"Update failed, id not exist"
        })
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
        "hour_start":data['hour_start'],
        "hour_finish":data['hour_finish'],
        "message":""
    }
    try:
        Schedule.objects.create(
            course_id_id=scheduleDict['course_id'],
            day=scheduleDict['day'],
            hour_start=scheduleDict['hour_start'],
            hour_finish=scheduleDict['hour_finish'],
        )
        return JsonResponse(scheduleDict)
    except IntegrityError:
        return JsonResponse(scheduleDict, status=404)

@csrf_exempt
def updateSchedule(request):
    data=json.loads(request.body.decode('utf-8'))
    
    scheduleDict={
        "id":data['id'],
        "day":data['day'],
        "hour_start":data['hour_start'],
        "hour_finish":data['hour_finish'],
        "message":""
    }
    try:
        Schedule.objects.filter(id=scheduleDict['id']).update(
            day=scheduleDict['day'],
            hour_start=scheduleDict['hour_start'],
            hour_finish=scheduleDict['hour_finish'],
        )
        scheduleDict.update({
            "message":"Update success"
        })
        return JsonResponse(scheduleDict)
    except IntegrityError:
        scheduleDict.update({
            "message":"Update failed, id not exist"
        })
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

@csrf_exempt
def tracker(request):
    data=json.loads(request.body.decode('utf-8'))
    trackerDict={
        "course_id":data['course_id'],
        "username":data['username'],
        "event":data['event'],
        "timestamp":data['timestamp']
    }
    statusDict={
        "message":"success"
    }
    try:
        Tracker.objects.create(
            course_id=trackerDict['course_id'],
            username=trackerDict['username'],
            event=trackerDict['event'],
            timestamp=trackerDict['timestamp']
        )
        return JsonResponse(statusDict, status=200)
    except IntegrityError:
        statusDict['message']="failed"
        return JsonResponse(statusDict, status=404)
    