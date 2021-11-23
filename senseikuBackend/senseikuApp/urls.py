from senseikuApp import viewsProduct
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('loginTutor/', views.loginTutor, name='loginTutor'),
    path('loginStudent/', views.loginStudent, name='loginStudent'),
    path('loginAdmin/',views.loginAdmin,name="loginAdmin"),
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
    path('addTransaction/',viewsProduct.addTransaction,name="addTransaction"),
    path('getTransaction/',viewsProduct.getTransactions,name="getTransaction"),
    path('confirmPayment/',viewsProduct.confirmPayment,name="confirmPayment"),
    path('confirmFinish/', viewsProduct.confirmFinish, name="confirmFinish"),
    path('myCart/',viewsProduct.getMyCart,name='getMyCart'),
    path('deleteMyCart/',viewsProduct.deleteMyCart,name="deleteMyCart"),
    path('deleteCart/', viewsProduct.deleteCart,name="deleteCart"),
    path('tracker/',viewsProduct.tracker,name="tracker"),
    path('getWishlist/',viewsProduct.getWishlist,name="getWishlist"),
    path('addWishlist/',viewsProduct.addWishlist,name="addWishlist"),
    path('deleteWishlist/',viewsProduct.deleteWishlist,name="deleteWishlist"),
    path('adminGetTransactions/',viewsProduct.adminGetTransactions,name="adminGetTransactions"),
    path('editStatus/',viewsProduct.editStatus,name="editStatus")
]