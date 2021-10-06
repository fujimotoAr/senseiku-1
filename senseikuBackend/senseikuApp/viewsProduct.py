from json.decoder import JSONDecodeError
from django.shortcuts import render, get_object_or_404, get_list_or_404
from .models import Course, Schedule
from django.core import serializers
from django.http import HttpResponse,JsonResponse
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt

import json

@csrf_exempt
def getNewCourse(request):
    courseList=get_list_or_404(Course)
    courseData=serializers.serialize('json', courseList, fields=('id','course_name','description','pricing','tutor_id'))
    return HttpResponse(courseData)

csrf_exempt
def addCourse(request):
    data=json.loads(request.body.decode('utf-8'))
    courseDict={
        "course_name":data['nama'],
        "description":data['deskripsi'],
        "pricing":data['harga'],
        "tutor_id":data['tutor_id'],
        "message":"Add course berhasil"
    }
    try:
        Course.objects.create(
            course_name=courseDict['course_name'],
            description=courseDict['description'],
            pricing=courseDict['pricing'],
            tutor_id_id=courseDict['tutor_id']
        )
        return JsonResponse(courseDict)
    except IntegrityError:
        courseDict.update({
            "message":"Add course gagal"
        })
        return JsonResponse(courseDict, status=404)

csrf_exempt
def addSchedule(request):
    data=json.loads(request.body.decode('utf-8'))
    
    scheduleDict={
        "course_id":data['course_id'],
        "day":data['day'],
        "hour":data['hour'],
        "message":"Add schedule berhasil"
    }
    try:
        Schedule.objects.create(
            course_id=scheduleDict['course_id'],
            day=scheduleDict['day'],
            hour=scheduleDict['hour'],
        )
        return JsonResponse(scheduleDict)
    except IntegrityError:
        scheduleDict.update({
            "message":"Add schedule gagal"
        })
        return JsonResponse(scheduleDict, status=404)
