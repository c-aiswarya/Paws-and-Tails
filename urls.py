# from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    
    path('',views.index,name='index'),
    path('logout/',views.logout,name='logout'),

    #user
    path('userregistration/',views.userregistration, name='userregistration'), 
    path('userlogin/',views.userlogin, name='userlogin'),
    path('profile/', views.profile, name='profile'),
    path('update_profile/',views.update_profile, name='update_profile'),
    path('proupdate/',views.proupdate,name='proupdate'),
    path('user_home/', views.user_home, name='user_home'),
    path('pet_list/', views.pet_list, name='pet_list'),
    path('pet_detail/<int:pk>/', views.pet_detail, name='pet_detail'),
    path('adopt/<int:id>',views.adopt,name='adopt'),
    path('ado_pt/',views.ado_pt,name='ado_pt'),
    path('add_donate/', views.add_donate, name='add_donate'),
    path('complete_donation/', views.complete_donation, name='complete_donation'),
    path('payment/<int:id>/', views.payment, name='payment'),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('searchdog/', views.searchdog, name='searchdog'),
    path('searchdogmuncipality/', views.searchdogmuncipality, name='searchdogmuncipality'),
    path('user_adopt/',views.user_adopt,name='user_adopt'),
    path('dog_feedback/<int:pet_id>', views.dog_feedback, name='dog_feed'),
    path('dog_feed/', views.dog_feed, name='dog_feed'),




    #muncipality
    path('muncipalitylogin/',views.muncipalitylogin,name='muncipalitylogin'),
    path('muncipalityhome/',views.muncipalityhome,name='muncipalityhome'),
    path('add_pet/', views.add_pet, name='add_pet'),
    path('delete_dogs/<int:id>', views.delete_dogs, name='delete_dogs'),
    path('list_dogs/', views.list_dogs, name='list_dogs'),
    path('trainerreg/',views.trainerreg, name='trainerreg'),
    path('list_trainer/',views.list_trainer, name='list_trainer'),
    path('delete_trainer/<int:id>', views.delete_trainer, name='delete_trainer'),
    path('addwork/<int:trainer_id>', views.addwork, name='addwork'),
    path('list_work/', views.list_work, name='list_work'),
    path('confirmwork/<int:trainer_id>',views.confirmwork, name='confirmwork'),
    path('addvaccination/<int:dog_id>', views.addvaccination,name='addvaccination'),
    path('vaccine_list/<int:dog_id>', views.vaccine_list, name='vaccine_list'),
    path('list_adoption/',views.list_adoption, name='list_adoption'),
    path('list_feedback/<int:id>',views.list_feedback, name='list_feed'),
    path('update_pet_status/<int:pet_id>/', views.update_pet_status, name='update_pet_status'),
    path('user_addvaccination/<int:id>/', views.user_addvaccination, name='user_addvaccination'),
    

    #trainer
    path('trainerlog/',views.trainerlog,name='trainerlog'),
    path('trainerhome/',views.trainerhome,name='trainerhome'),
    path('trainer/',views.trainer,name='trainer'),
    path('trainerupdate_profile/',views.trainerupdate_profile, name='trainerupdate_profile'),
    path('newupdate/',views.newupdate,name='newupdate'),
    path('worklist/',views.worklist,name='worklist'),
    
    
    #admin
    path('adminreg/',views.adminreg,name='adminreg'),
    path('adminlogin/',views.adminlogin,name='adminlogin'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('addmuncipality/', views.add_muncipality, name='addmuncipality'),
    path('adopt_list/',views.adopt_list, name='adopt_list'),
    path('donation_list/', views.donation_list, name='donation_list'),
    path('trainer_list/',views.trainer_list,name='trainer_list'),
    path('muncipalitylist/',views.muncipalitylist,name='muncipalitylist'),
    path('deletemuncipality/<int:id>',views.deletemuncipality,name='deletemuncipality'),

    path('request_password_reset/',views.request_password_reset, name='request_password_reset'),
    path('reset_password/<uidb64>/<token>/', views.reset_password, name='reset_password'),

    path('edittrainer/<int:id>',views.edittrainer, name='edittrainer'),

    
    
    

]   