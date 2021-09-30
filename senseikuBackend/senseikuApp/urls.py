from senseikuApp import viewsProduct
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token 

from . import views

urlpatterns = [
    path('loginSensei/', views.loginTutor, name='loginTutor'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('signupSensei/',views.signupTutor, name='signupTutor'),
    path('signupStudent/',views.signupStudent, name='signupStudent'),
    path('newCourse/',viewsProduct.getNewCourse, name='getNewCourse'),
    path('addCourse/',viewsProduct.addCourse, name='addCourse'),



]