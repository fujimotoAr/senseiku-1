from django.urls import path

from . import views

urlpatterns = [
    path('loginSensei/', views.loginTutor, name='loginTutor'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('signupSensei/',views.signupTutor, name='signupTutor'),
    path('signupStudent/',views.signupStudent, name='signupStudent'),
    path('newCourse/',views.getNewCourse, name='getNewCourse'),
    path('addCourse/',views.addCourse, name='addCourse'),
    path('updateCourse/',views.updateCourse, name='updateCourse')


]