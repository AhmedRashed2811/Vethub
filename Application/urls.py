
# ? -------------------------------------------------------------------------------------------------------IMPORTING LIBRARIES
from django.urls import path
from .import views

#  -------------------------------------------------------------------------------------------------------URLs
urlpatterns = [
    path('', views.index, name="index"),
    path('customer_register', views.customer_register, name = "customer_register"),
    path('signup', views.signup, name = "signup"),
    path('login', views.login, name = "login"),
    path('logout', views.logout, name="logout"),
    path('admin_panel', views.admin_panel, name = "admin_panel"),
    path('clinic_management_system', views.clinic_management_system, name = "clinic_management_system"),
    path('doctor_register', views.doctor_register, name = "doctor_register"),
    path('edit_doctor/<int:doctor_id>/', views.edit_doctor, name = "edit_doctor"),
    path('edit_customer/<int:customer_id>/', views.edit_customer, name = "edit_customer"),
    path('delete_account/<int:user_id>/', views.delete_account, name = "delete_account"),
    path('doctor_details/<int:doctor_id>/', views.doctor_details, name = "doctor_details"),
    path('update_status/<int:appointment_id>/', views.update_status, name = "update_status"),
    path('cancel_appointment/<int:appointment_id>/', views.cancel_appointment, name = "cancel_appointment"),
    path('chats', views.chats, name = "chats"),
    path('chat_details/<int:receiver_id>', views.chat_details, name = "chat_details"),
    path('send_message/<int:receiver_id>', views.send_message, name="send_message"),
    path('make_chat/<int:doctor_id>/', views.make_chat, name="make_chat"),
    path('receive_message/<int:sender_id>/', views.receive_message, name="receive_message"),
    path('feedback/<int:doctor_id>/', views.feedback, name="feedback"),
    path('delete_review/<int:review_id>/', views.delete_review, name="delete_review"),
    path('customer_previous_appointments/', views.customer_previous_appointments, name="customer_previous_appointments"),
    path('admin_register/', views.admin_register, name="admin_register"),
    path('manage_news/', views.manage_news, name="manage_news"),
    path('delete_news/<int:news_id>/', views.delete_news, name="delete_news"),
    path('verify_doctors/', views.verify_doctors, name="verify_doctors"),
    path('verification/<int:doctor_id>/', views.verification, name="verification"),
    path('delete_message/<int:message_id>/', views.delete_message, name="delete_message"),
    path('offline_appointment/', views.offline_appointment, name="offline_appointment"),
    path('make_offer/', views.make_offer, name="make_offer"),
    path('delete_offer/', views.delete_offer, name="delete_offer"),
    path('activate/<uidb64>/<token>', views.activate, name="activate"),
    path('reset_password', views.reset_password_request, name="reset_password_request"),
    path('passwordResetConfirm/<uidb64>/<token>', views.passwordResetConfirm, name="passwordResetConfirm"),
    path('mark_notification_as_read/<int:notification_id>/', views.mark_notification_as_read, name='mark_notification_as_read'),
    
    

]
