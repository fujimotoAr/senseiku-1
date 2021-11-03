from json.decoder import JSONDecodeError
from django.contrib.auth.models import User
from django.db.models import fields, query
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course, Schedule, Cart, Tracker, Review 
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from sklearn.metrics.pairwise import haversine_distances
from math import radians
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

def getMySchedule(request):
    data = request.GET.get('username')
    scheduleList = Schedule.objects.filter(tutor_username=data)
    scheduleData = serializers.serialize(
        'json', scheduleList, fields=('id','tutor_username','date','hour_start','hour_finish','availability')
    )
    return HttpResponse(scheduleData)

def getAllCourse(request):
    courseList=[*Course.objects.order_by('id'), *User.objects.order_by('course__id')]
    courseData=serializers.serialize(
        'json', courseList,
        fields=('id','course_name','description','pricing','tutor_username','username','first_name')
    )
    return HttpResponse(courseData)

def getCourseDetail(request):
    data = request.GET.get('id')
    username = Course.objects.filter(id=data).values_list('tutor_username')
    selectedCourse = [*Course.objects.filter(id=data), *User.objects.filter(course__id=data),
                      *Schedule.objects.filter(tutor_username__in=username)]
    serialized = serializers.serialize(
        'json', selectedCourse,
        fields=('course_name','description','pricing','username','first_name',
                'date','hour_start','hour_finish','availability')
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
        "tutor_username":data['tutor_username'],
        "date":data['date'],
        "hour_start":data['hour_start'],
        "hour_finish":data['hour_finish'],
        "message":"success"
    }
    try:
        Schedule.objects.create(
            tutor_username_id=scheduleDict['tutor_username'],
            date=scheduleDict['date'],
            hour_start=scheduleDict['hour_start'],
            hour_finish=scheduleDict['hour_finish'],
            availability=True
        )
        return JsonResponse(scheduleDict)
    except IntegrityError:
        scheduleDict['message'] = 'failed'
        return JsonResponse(scheduleDict, status=404)

@csrf_exempt
def updateSchedule(request):
    data=json.loads(request.body.decode('utf-8'))
    
    scheduleDict={
        "id":data['id'],
        "date":data['date'],
        "hour_start":data['hour_start'],
        "hour_finish":data['hour_finish'],
        "message":""
    }
    try:
        Schedule.objects.filter(id=scheduleDict['id']).update(
            date=scheduleDict['date'],
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
def addCart(request):
    data = json.loads(request.body.decode('utf-8'))
    cartDict = {
        "student_username": data['student_username'],
        "schedule_id": data['schedule_id'],
        "course_id": data['course_id'],
        "message": "success"
    }
    try:
        Cart.objects.create(
            student_username_id = cartDict['student_username'],
            schedule_id_id = cartDict['schedule_id'],
            course_id_id = cartDict['course_id'],
        )
        Schedule.objects.filter(id=data['schedule_id']).update(
            availability = False
        )
        return JsonResponse(cartDict)
    except IntegrityError:
        cartDict['message'] = "failed"
        return JsonResponse(cartDict, status=404)

def getMyCart(request):
    data = request.GET.get('username')
    if Cart.objects.filter(student_username=data).exists():
        cartList = list(Cart.objects.filter(student_username=data).values(
            'id','student_username','course_id','course_id__course_name',
            'course_id__description','course_id__pricing',
            'course_id__tutor_username','course_id__tutor_username__first_name',
            'schedule_id','schedule_id__date',
            'schedule_id__hour_start','schedule_id__hour_finish',
            'course_id__tutor_username__location__latitude',
            'course_id__tutor_username__location__longitude',
            'student_username__location__latitude',
            'student_username__location__longitude',
        ))
        for key in cartList:
            key['course_name'] = key.pop('course_id__course_name')
            key['description'] = key.pop('course_id__description')
            key['pricing'] = key.pop('course_id__pricing')
            key['tutor_username'] = key.pop('course_id__tutor_username')
            key['first_name'] = key.pop('course_id__tutor_username__first_name')
            key['date'] = key.pop('schedule_id__date')
            key['hour_start'] = key.pop('schedule_id__hour_start')
            key['hour_finish'] = key.pop('schedule_id__hour_finish')
            tutor_latitude = key.pop('course_id__tutor_username__location__latitude')
            tutor_longitude = key.pop('course_id__tutor_username__location__longitude')
            student_latitude = key.pop('student_username__location__latitude')
            student_longitude = key.pop('student_username__location__longitude')
            price = 0
            if tutor_latitude and tutor_longitude and student_latitude and student_longitude is not None:
                tutor_loc = [tutor_latitude, tutor_longitude]
                student_loc = [student_latitude, student_longitude]
                tutor_loc_rad = [radians(_) for _ in tutor_loc]
                student_loc_rad = [radians(_) for _ in student_loc]
                distance = haversine_distances([tutor_loc_rad, student_loc_rad])
                distance = distance * 6371000/1000
                price = round(5000*distance[0][1])
            key['transport_price'] = price
    else:
        cartList = {'student_username': data, 'message': 'empty cart'}
    return JsonResponse(cartList, safe=False)

def deleteMyCart(request):
    data = request.GET.get('username')
    output={
        "message":"remove success"
    }
    if Cart.objects.filter(student_username=data).exists():
        Cart.objects.filter(student_username=data).delete()
        return JsonResponse(output,status=200)
    else:
        output['message']="already empty"
        return JsonResponse(output,status=404)

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
            course_id_id=trackerDict['course_id'],
            username_id=trackerDict['username'],
            event=trackerDict['event'],
            timestamp=trackerDict['timestamp']
        )
        return JsonResponse(statusDict, status=200)
    except IntegrityError:
        statusDict['message']="failed"
        return JsonResponse(statusDict, status=404)
    