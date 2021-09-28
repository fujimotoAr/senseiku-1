from django.urls import path

from . import views

urlpatterns = [
    path('loginSensei/', views.loginTutor, name='loginTutor'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('signupSensei/',views.signupTutor, name='signupTutor'),
    path('signupStudent/',views.signupStudent, name='signupStudent')

]