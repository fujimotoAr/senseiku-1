from senseikuApp import viewsProduct
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('loginTutor/', views.loginTutor, name='loginTutor'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('signupTutor/',views.signupTutor, name='signupTutor'),
    path('signupStudent/',views.signupStudent, name='signupStudent'),
    path('profileTutor/',views.profileTutor, name='profileTutor'),
    path('profileStudent/',views.profileStudent, name='profileStudent'),
    path('editProfile/',views.editProfile,name='editProfile'),
    path('logout/',views.logout,name="logout"),

    path('newCourse/',viewsProduct.getNewCourse, name='getNewCourse'),
    path('myCourse/',viewsProduct.getMyCourse, name='getMyCourse'),
    path('allCourse/',viewsProduct.getAllCourse, name='getAllCourse'),
    path('courseDetail/',viewsProduct.getCourseDetail,name='getCourseDetail'),
    path('mySchedule/',viewsProduct.getMySchedule,name='getMySchedule'),

    path('addCourse/',viewsProduct.addCourse, name='addCourse'),
    path('deleteCourse/',viewsProduct.deleteCourse, name='deleteCourse'),
    path('updateCourse/',viewsProduct.updateCourse,name='updateCourse'),

    path('addSchedule/',viewsProduct.addSchedule, name='addSchedule'),
    path('deleteSchedule/',viewsProduct.deleteSchedule, name='deleteSchedule'),
    path('updateSchedule/',viewsProduct.updateSchedule,name='updateSchedule'),

    path('addCart/',viewsProduct.addCart,name='addCart'),
    path('myCart/',viewsProduct.getMyCart,name='getMyCart'),
    path('deleteMyCart/',viewsProduct.deleteMyCart,name="deleteMyCart"),
    path('tracker/',viewsProduct.tracker,name="tracker")


]