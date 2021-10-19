from senseikuApp import viewsProduct
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 

from . import views

urlpatterns = [
    path('loginTutor/', views.loginTutor, name='loginTutor'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('signupTutor/',views.signupTutor, name='signupTutor'),
    path('signupStudent/',views.signupStudent, name='signupStudent'),
    path('profileTutor/',views.signupTutor, name='profileTutor'),
    path('profileStudent/',views.signupStudent, name='profileStudent'),

    path('getNewCourse/',viewsProduct.getNewCourse, name='getNewCourse'),
    path('getAllCourse/',viewsProduct.getAllCourse, name='getAllCourse'),
    path('courseDetail/',viewsProduct.getCourseDetail,name='getCourseDetail'),

    path('addCourse/',viewsProduct.addCourse, name='addCourse'),
    path('deleteCourse/',viewsProduct.deleteCourse, name='deleteCourse'),
    path('updateCourse/',viewsProduct.updateCourse,name='updateCourse'),

    path('addSchedule/',viewsProduct.addSchedule, name='addSchedule'),
    path('deleteSchedule/',viewsProduct.deleteSchedule, name='deleteSchedule'),
    path('updateSchedule/',viewsProduct.updateSchedule,name='updateSchedule'),


]