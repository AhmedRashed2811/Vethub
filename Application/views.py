
# ? -------------------------------------------------------------------------------------------------------IMPORTING LIBRARIES
import json
import re
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponseNotAllowed, JsonResponse
from django.contrib import messages
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, get_user_model, login as Login, logout as Logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.forms import formset_factory
from django.urls import reverse
from .decorators import unauthenticated_user, allowed_users
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.db.models import Avg
from datetime import datetime
from .tokens import *
from .models import *
from .forms import *

# TODO -------------------------------------------------------------------------------------------------------CONTROLLERS

#  --------------------------------------------------------------------------------------------------VIEWS

# -----------------------------------------------------------------------------HOME PAGE
def index(request):
    doctors = Doctor.objects.filter(is_verified = True)
    doctors_count = doctors.count()
    news = News.objects.all()
    feedback_exist = False
    supportTeamMessageForm = SupportTeamMessageForm(request.POST or None)
    
    # Apply filters if provided in the GET parameters
    city_filter = request.GET.get('city')
    governorate_filter = request.GET.get('governorate')
    
    if city_filter:
        doctors = doctors.filter(city=city_filter)
        
    if governorate_filter:
        doctors = doctors.filter(governorate=governorate_filter)
    
    context = {
        "doctors": doctors,
        "feedback_exists": feedback_exist,
        "news": news,
        "doctors_count":doctors_count}
    
    if request.user.is_authenticated:
        if request.method == 'POST':
            if supportTeamMessageForm.is_valid():
                SupportTeamMessage.objects.create(
                    message = supportTeamMessageForm.cleaned_data["message"],
                    customer = request.user.customer
                )
                return redirect('/')
        
        if request.user.groups.filter(name='Customers').exists():
            delayed_appointments = Appointment.objects.filter(customer = request.user.customer)
            appointments = delayed_appointments.filter(status = "Done")
            notifications = Notification.objects.filter(customer = request.user.customer)
            notifications_count = notifications.filter(is_read = False).count()
            feedbacks = []
            not_feedback_appointments = []
            
            for appointment in delayed_appointments:
                
                notification_message1 = f'Reminder! You have an appointment with dr.({appointment.doctor.user.name}) after 3 days on ({appointment.date})'
                notification_message2 = f'Reminder! You have an appointment with dr.({appointment.doctor.user.name}) Tomorrow at ({appointment.time})'
                notification_exist1 = Notification.objects.filter(customer = request.user.customer, message=notification_message1)
                notification_exist2 = Notification.objects.filter(customer = request.user.customer, message=notification_message2)
                
                if notification_exist1:
                    pass
                elif notification_exist2:
                    pass
                else:
                    if days_until_appointment(appointment.date) == 3:
                        Notification.objects.create(customer=request.user.customer, notification_type='REMINDER', message=notification_message)
                        notifications_count += 1
                    
                    if days_until_appointment(appointment.date) == 1:
                        Notification.objects.create(customer=request.user.customer, notification_type='REMINDER', message=notification_message2)
                        notifications_count += 1
                        
            temp = 0
            for appointment in appointments:
                feedback = Feedback.objects.filter(customer = request.user.customer, doctor = appointment.doctor)

                if not feedback:
                    feedbacks.append(feedback)
                    not_feedback_appointments.append(appointment)
                    temp+=1
            
            for appointment in not_feedback_appointments:
                if appointments and len(feedbacks) != 0:
                    feedback_exist = True
                    notification_message = f'Please Give Dr. {appointment.doctor.user.name} a Feedback'
                    notification_exist3 = Notification.objects.filter(customer = request.user.customer, message=notification_message)
                    if not notification_exist3:
                        Notification.objects.create(customer=request.user.customer, notification_type='APPOINTMENT_DONE', message=notification_message)
                        notifications_count += 1
            
            notifications_count = notifications_count + temp
            context = {
                "doctors": doctors,
                "not_feedback_appointments":not_feedback_appointments,
                "appointments": appointments,
                "feedback_exists": feedback_exist,
                "news": news,
                "doctors_count":doctors_count,
                "notifications": notifications,
                "notifications_count":notifications_count}
            
        elif request.user.groups.filter(name='Admins').exists():
            context = {
                "doctors": doctors,
                "news": news,
                "doctors_count":doctors_count}
            
    if request.method =="POST":
        governorate = request.POST.get("governorate")
        city = request.POST.get("city")
        urgent_examination = request.POST.get("urgent-examination")
        if urgent_examination == "Yes":
            urgent_examination = True
        elif urgent_examination == "No":
            urgent_examination = False
        if not governorate and not city and not urgent_examination:
            pass
        else:
            if governorate and city and urgent_examination:
                doctors = doctors.filter(governorate = governorate, city = city, urgent_examination = urgent_examination)
                doctors_count = doctors.count()
            if governorate and city and not urgent_examination:
                doctors = doctors.filter(governorate = governorate, city = city)
                doctors_count = doctors.count()
            if governorate and not city and not urgent_examination:
                doctors = doctors.filter(governorate = governorate)
                doctors_count = doctors.count()
            if governorate and not city and urgent_examination:
                doctors = doctors.filter(governorate = governorate, urgent_examination = urgent_examination)
                doctors_count = doctors.count()
            if not governorate and city and not urgent_examination:
                doctors = doctors.filter(city = city)
                doctors_count = doctors.count()
            if not governorate and city and urgent_examination:
                doctors = doctors.filter(city = city, urgent_examination = urgent_examination)
                doctors_count = doctors.count()
            if not governorate and not city and urgent_examination:
                doctors = doctors.filter(urgent_examination = urgent_examination)
                doctors_count = doctors.count()
                
            context["doctors"] = doctors
            context["doctors_count"] = doctors_count

    return render(request, 'index.html', context)


# -----------------------------------------------------------------------------DOCTOR DETAILS & CREATE APPOINTMENT
def doctor_details(request, doctor_id):
    doctor1 = get_object_or_404(User, pk=doctor_id)
    feedbacks = Feedback.objects.filter(doctor = doctor1.doctor)
    appointments = Appointment.objects.filter(doctor = doctor1.doctor)
    rating = ""
    doctor_rating = int(round(doctor1.doctor.rating))
    remaining = 5-doctor_rating
    times = []
    time = {}
    
    for appointment in appointments:
        time["time"] = appointment.time
        time["date"] = appointment.date
        
        times.append(time)
        time = {}
        
    for i in range(0, doctor_rating):
        rating+='<i class="fa-solid fa-star checked"></i>'
    
    for i in range(0, remaining):
        rating+='<i class="fa-regular fa-star checked"></i>'
        
    doctor_rating = rating
    rating = ""
    feedback_list= []
    new_feedback = {}
    remaining = 0
    
    for feedback in reversed(feedbacks):
        rating = ""
        new_feedback["name"] = feedback.customer.user.name
        new_feedback["date"] = feedback.date
        new_feedback["comment"] = feedback.comment
        rate = int(feedback.rating)
        remaining = 5- rate
        for i in range(0, rate):
            rating+='<i class="fa-solid fa-star checked"></i>'
        
        for i in range(0, remaining):
            rating+='<i class="fa-regular fa-star checked"></i>'
        
        new_feedback["rating"] = rating
        feedback_list.append(new_feedback)
        new_feedback = {}
        
    
    location_url = doctor1.doctor.location
    pattern = r"mlat=([-+]?\d*\.\d+|\d+)&mlon=([-+]?\d*\.\d+|\d+)"
    match = re.search(pattern, location_url)

    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
    
    bbox_latitude_min = latitude - 0.015
    bbox_latitude_max = latitude + 0.015
    bbox_longitude_min = longitude - 0.015
    bbox_longitude_max = longitude + 0.015
    
    if request.method == 'POST':
        customer_id = request.POST.get('user_id')
        doctor_id = request.POST.get('doctor_id')
        doctor_price = float(request.POST.get('doctor_price'))
        offer_percentage = float(request.POST.get('offer_percentage'))
        doctor_offer_price = doctor_price - (doctor_price*offer_percentage)
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        if customer_id is None or not customer_id.isdigit():
            return redirect('/login')
        
        customer = User.objects.filter(id=customer_id).first()
        customer = Customer.objects.filter(user = customer).first()
        doctor = Doctor.objects.filter(user = doctor1).first()

        Appointment.objects.create(
            customer=customer,
            doctor=doctor,
            appointment_price=doctor_offer_price,
            date=date,
            time=time
        )
        
        customer.appointments_count += 1
        customer.save()
        
        notification_message = f'Your appointment with Dr. {doctor.user.name} has been successfully scheduled for {date} at {time}.'
        Notification.objects.create(customer=customer, notification_type='CREATED', message=notification_message)
        return redirect('/')
    
    else:    
        return render(request, 'doctor_details.html', {'doctor': doctor1, 'feedbacks_count': feedbacks.count(), 'latitude': latitude, 'longitude': longitude, 'latitude': latitude,
        'longitude': longitude,
        'bbox_latitude_min': bbox_latitude_min,
        'bbox_latitude_max': bbox_latitude_max,
        'bbox_longitude_min': bbox_longitude_min,
        'bbox_longitude_max': bbox_longitude_max,
        "feedback_list": feedback_list,
        "doctor_rating":doctor_rating,
        "appointments":times}
        )


# -----------------------------------------------------------------------------SIGN-UP
@unauthenticated_user
def signup(request):
    return render(request, "SignUp.html")


# -----------------------------------------------------------------------------CUSTOMER SIGN-UP
@unauthenticated_user
def customer_register(request):
    if request.method == 'POST':
        email = request.POST.get("Email")
        name = request.POST.get("Name")
        phone_number = request.POST.get("PhoneNumber")
        password1 = request.POST.get("Password1")
    
        if  (User.objects.filter(email=email) or User.objects.filter(phone_number=phone_number)):
            messages.info(request, "User Already Exists")
            return redirect('login')

        hashed_password = make_password(password1)
        
        user = User.objects.create(
                        email=email,
                        name=name,
                        phone_number=phone_number,
                        password = hashed_password 
                    )
        
        customer = Customer.objects.create(
            user = user,
        )
        
        custom_user_instances = []
        user.is_active = False
        user.save()
        activate_email(request, user,user.email )
        custom_user_instances.append(user)
        group = Group.objects.get(name='Customers')
        group.user_set.add(user)
        first_custom_user_instance = custom_user_instances[0] if custom_user_instances else None
        
        customer.user = first_custom_user_instance
        customer.is_verified = False
        customer.save()
        
        messages.success(request, "User Created Successfully")
        return redirect('/login')

    return render(request, 'customer_register.html')


# -----------------------------------------------------------------------------DOCTOR SIGN-UP
@unauthenticated_user
def doctor_register(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        password1 = request.POST.get("password1")
        governorate = request.POST.get("governorate")
        city = request.POST.get("city")
        profile_photo = request.FILES.get("profile_photo")
        certifications = request.FILES.get("certification")
        price = request.POST.get("price")
        urgent_examination = request.POST.get("urgent-examination")
        description = request.POST.get("Description")
        location = request.POST.get('location')
        
        if  (User.objects.filter(email=email) or User.objects.filter(phone_number=phone_number)):
            messages.info(request, "User Already Exists")
            return redirect('login')
    
        hashed_password = make_password(password1)
        
        user = User.objects.create(
                        email=email,
                        name=name,
                        phone_number=phone_number,
                        password = hashed_password 
                    )
        
        doctor = Doctor.objects.create(
            user = user,
            governorate = governorate,
            city = city,
            profile_photo = profile_photo,
            certifications = certifications,
            price = price,
            urgent_examination = urgent_examination,
            description = description,
            location = location
        )
        
        custom_user_instances = []
        user.is_active = False
        activate_email(request, user,user.email )
        user.save()
        custom_user_instances.append(user)
        group = Group.objects.get(name='Doctors')
        group.user_set.add(user)
        first_custom_user_instance = custom_user_instances[0] if custom_user_instances else None
        doctor.user = first_custom_user_instance
        doctor.save()
        messages.warning(request, "Your Certification is Being Verified Also")
        return redirect('/login')
        
    return render(request, 'doctor_register.html')


# -----------------------------------------------------------------------------LOGIN
@unauthenticated_user
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        
        if user is not None:
            try:
                if hasattr(user, 'doctor'):
                    if user.doctor.is_verified:
                        Login(request, user)
                        return redirect(get_redirect_url(request))
                    else:
                        messages.warning(request, "Not Verified Yet")
                elif hasattr(user, 'customer'):
                    if user.is_active:
                        Login(request, user)
                        return redirect(get_redirect_url(request))
                    else:
                        messages.error(request, "Verify your Email First")
                        return render(request, 'login.html')
                    
                elif hasattr(user, "admin"):
                    Login(request, user)
                    return redirect(get_redirect_url(request))
                
            except ObjectDoesNotExist:
                messages.info(request, "User has no doctor.")
        else:
            messages.error(request, "Not Correct Please Try Again")
            
    if 'HTTP_REFERER' in request.META:
        request.session['referrer'] = request.META.get('HTTP_REFERER')
            
    return render(request, 'login.html')


# -----------------------------------------------------------------------------EDIT DOCTOR
@allowed_users(allowed_roles=["Doctors", "Admins"])
@login_required(login_url='login')
def edit_doctor(request, doctor_id):
    doctor_user = get_object_or_404(User, pk=doctor_id)
    doctor = doctor_user.doctor  
    
    latitude = ""
    longitude = ""
    location_url = doctor.location
    pattern = r"mlat=([-+]?\d*\.\d+|\d+)&mlon=([-+]?\d*\.\d+|\d+)"
    match = re.search(pattern, location_url)
    if match:
        latitude = float(match.group(1))
        longitude = float(match.group(2))
    bbox_latitude_min = latitude - 0.015
    bbox_latitude_max = latitude + 0.015
    bbox_longitude_min = longitude - 0.015
    bbox_longitude_max = longitude + 0.015
    
    if request.method == 'POST':
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        governorate = request.POST.get("governorate")
        city = request.POST.get("city")
        price = request.POST.get("price")
        urgent_examination = request.POST.get("urgent-examination")
        description = request.POST.get("Description")
        image_exist = False
        try:
            profile_photo = request.FILES['profile_photo']
            image_exist = True
        except:
            pass
        location = request.POST.get('location')
        
        if not city and not governorate :
            city = doctor.city
            governorate = doctor.governorate
            
        if city and not governorate:
            governorate = doctor.governorate
            
        if not city and governorate:
            city = doctor.city
        
        if phone_number != doctor_user.phone_number:
            temp = User.objects.filter(phone_number = phone_number).count()
            if temp != 0:
                messages.error(request, "This Number is already Exists")
                temp = 0
                if request.user.groups.filter(name='Admins').exists():
                    return redirect('/admin_panel')
                
                return redirect("edit_doctor", doctor_id=request.user.id)
        
        doctor_user.name = name
        doctor_user.phone_number = phone_number
        doctor.governorate = governorate
        doctor.city = city
        doctor.price = price
        doctor.urgent_examination = urgent_examination
        doctor.description = description
        
        try:
            if (image_exist):
                os.remove(doctor.profile_photo.path)
            doctor.profile_photo = profile_photo
        except:
            pass
        
        doctor.location = location
        
        doctor_user.save()
        doctor.save()
        messages.success(request, "Updated Successfully")
        
        if request.user.groups.filter(name='Admins').exists():
            return redirect('/admin_panel')
        
        return redirect('/')
        
    return render(request, 'edit_doctor.html', {"user":doctor_user, "doctor":doctor,'latitude': latitude, 'longitude': longitude, 'latitude': latitude,
        'longitude': longitude,
        'bbox_latitude_min': bbox_latitude_min,
        'bbox_latitude_max': bbox_latitude_max,
        'bbox_longitude_min': bbox_longitude_min,
        'bbox_longitude_max': bbox_longitude_max,})


# -----------------------------------------------------------------------------EDIT CUSTOMER
@allowed_users(allowed_roles=["Customers", "Admins"])
@login_required(login_url='login')
def edit_customer(request, customer_id):
    
    customer_user = get_object_or_404(User, pk=customer_id)
    customer = customer_user.customer  
    appointments_count = customer.appointments_count
        
    if request.method == 'POST':
        name = request.POST.get("name")
        phone_number = request.POST.get("phone_number")
        
        if(phone_number == customer_user.phone_number):
            customer_user.name = name
            customer_user.save()
            if request.user.groups.filter(name='Admins').exists():
                return redirect('/admin_panel')
            
            return JsonResponse({'success': True}) 
            
        temp = User.objects.filter(phone_number = phone_number).count()
        if temp != 0:
            messages.error(request, "This Number is already Exists")
            temp = 0
            return redirect("edit_customer", customer_id=request.user.id)
        
        else:
            customer_user.name = name
            customer_user.phone_number = phone_number
            customer_user.save()
            
            if request.user.groups.filter(name='Admins').exists():
                return redirect('/admin_panel')
            
            return JsonResponse({'success': True}) 
        
    
    return render(request, 'edit_customer.html', { "appointments_count":appointments_count,"customer":customer_user})


# -----------------------------------------------------------------------------CLINIC MANAGEMENT SYSTEM
@login_required(login_url='login')
@allowed_users(allowed_roles=["Doctors"])
def clinic_management_system(request):

    doctor_user = User.objects.filter(id=request.user.id).first()
    doctor = Doctor.objects.filter(user = doctor_user).first()
        
    doctor_appointments = Appointment.objects.filter(doctor=doctor)

    context = {"doctor_appointments":doctor_appointments}
    
    return render(request, 'clinic_management_system.html', context)


# -----------------------------------------------------------------------------CHATS 
@allowed_users(allowed_roles=["Doctors","Customers"])
@login_required(login_url='login')
def chats(request):
    
    user = request.user
    if user.groups.filter(name='Customers').exists():
        customer = request.user.customer
        chats = Chat.objects.filter(customer = customer)
        context = {"user": customer, "chats": chats}
        return render(request, 'chats.html', context)
    
    if user.groups.filter(name='Doctors').exists():
        doctor = request.user.doctor
        chats = Chat.objects.filter(doctor = doctor)
        context = {"user": doctor, "chats": chats}
        return render(request, 'chats.html', context)
        
    return render(request, 'chats.html')


# -----------------------------------------------------------------------------CHAT
@allowed_users(allowed_roles=["Doctors","Customers"])
@login_required(login_url='login')
def chat_details(request, receiver_id):
    user = request.user
    
    if user.groups.filter(name='Customers').exists():
        customer = request.user.customer
        doctor = get_object_or_404(User, pk=receiver_id)
        chat = Chat.objects.filter(customer = customer, doctor = doctor.doctor).first()
        received_messages = ChatMessage.objects.filter(msg_sender = doctor, msg_receiver = user)
        messages = ChatMessage.objects.filter(chat=chat)
        form = ChatMessageForm()
        
        if request.method == 'POST':
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                chat_message = form.save(commit=False)
                chat_message.content = form.cleaned_data['content']
                chat_message.msg_sender = user
                chat_message.msg_receiver = doctor
                chat_message.chat = chat
                chat_message.save()
                return redirect(f"/chat_details/{doctor.id}", )

        context = {
            "sender": customer,
            "receiver": doctor,
            "form": form,
            "messages":messages,
            "number_of_received_messages": received_messages.count()}
        return render(request, 'chat_details.html', context)
    
    if user.groups.filter(name='Doctors').exists():
        doctor = request.user.doctor
        customer = get_object_or_404(User, pk=receiver_id)
        chat = Chat.objects.filter(customer = customer.customer, doctor = doctor).first()
        context = {"sender": doctor, "receiver": customer}
        received_messages = ChatMessage.objects.filter(msg_sender = customer, msg_receiver = user)
        messages = ChatMessage.objects.filter(chat=chat)
        form = ChatMessageForm()
        
        if request.method == 'POST':
            form = ChatMessageForm(request.POST)
            if form.is_valid():
                chat_message = form.save(commit=False)
                chat_message.content = form.cleaned_data['content']
                chat_message.msg_sender = user
                chat_message.msg_receiver = customer
                chat_message.chat = chat
                chat_message.save()
                return redirect(f"/chat_details/{customer.id}", )
            
        context = {
            "sender": doctor,
            "receiver": customer,
            "form": form,
            "messages":messages,
            "number_of_received_messages": received_messages.count()}
        return render(request, 'chat_details.html', context)
    
    return render(request, 'index.html')


# -----------------------------------------------------------------------------FEEDBACK
@allowed_users(allowed_roles=["Customers"])
@login_required(login_url='login')
def feedback(request, doctor_id):

    customer = request.user.customer
    doctor = User.objects.filter(id=doctor_id).first().doctor
    bad_word_exist = False
    
    if request.method == 'POST':
        question1 = request.POST.get("question1")
        question2 = request.POST.get("question2")
        comment = request.POST.get("comment")
        rating = request.POST.get("doctor-rating")
        
        
        bad_words = ["fuck",  "الخرا", "وسخ", "خول", "عرص", "يتمنيك" , "خرا", "متناكة", "نتن"]
        for word in bad_words:
            if word in comment.split():
                bad_word_exist = True

        if bad_word_exist:
            Feedback.objects.create(
                customer = customer,
                doctor = doctor,
                rating = rating,
                comment = comment,
                question1 = question1,
                question2 = question2,
                inappropriate = True
            )
        
        else:
            Feedback.objects.create(
                customer = customer,
                doctor = doctor,
                rating = rating,
                comment = comment,
                question1 = question1,
                question2 = question2
            )
        
        
        # Calculate the new rating
        existing_ratings = Feedback.objects.filter(doctor=doctor)
        new_rating = existing_ratings.aggregate(Avg('rating'))['rating__avg']
        if new_rating is not None:
            doctor.rating = round(new_rating, 1)
        else:
            doctor.rating = 0  # No ratings yet
        doctor.save()
        
        return redirect('/')
        
    return render(request, 'Feedback.html')


# -----------------------------------------------------------------------------CUSTOMER PREVIOUS APPOINTMENTS
@allowed_users(allowed_roles=["Customers"])
@login_required(login_url='login')
def customer_previous_appointments(request):
    customer = request.user.customer
    appointments = Appointment.objects.filter(customer = customer)
    context = {"appointments": appointments}
    feedback_exist = False
    
    feedbacks = []
    not_feedback_appointments = []
    
    for appointment in appointments:
        
        feedback = Feedback.objects.filter(customer = customer, doctor = appointment.doctor)
        if not feedback:
            feedbacks.append(feedback)
            not_feedback_appointments.append(appointment)
            
    if appointments and len(feedbacks) != 0:
        feedback_exist = True
        
    context = {"not_feedback_appointments":not_feedback_appointments, "appointments": appointments, "feedback_exists": feedback_exist}
    
    return render(request, "customer_previous_appointments.html", context)


# -----------------------------------------------------------------------------ADMIN PANEL
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def admin_panel(request):
    customers = Customer.objects.all()
    appointments = Appointment.objects.all()
    doctors = Doctor.objects.filter(is_verified = True)
    inappropriate_reviews = Feedback.objects.filter(inappropriate = True)
    supportTeamMessages = SupportTeamMessage.objects.all()

    context = {
        'customers': customers,
        'doctors': doctors,
        'appointments': appointments,
        'inappropriate_reviews':inappropriate_reviews,
        'supportTeamMessages': supportTeamMessages
        }
    
    return render(request, 'admin_panel.html', context)


# -----------------------------------------------------------------------------ADMIN REGISTER
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def admin_register(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        name = request.POST.get("name")
        phone_number = request.POST.get("phoneNumber")
        password = request.POST.get("password")
        
        if  (User.objects.filter(email=email) or User.objects.filter(phone_number=phone_number)):
            messages.info(request, "User Already Exists")
            return redirect('admin_panel')
        
        password = make_password(password)
        
        user = User.objects.create(
                        email=email,
                        name=name,
                        phone_number=phone_number,
                        password = password 
                    )
        
        admin = Admin.objects.create(
            user = user,
        )
        
        custom_user_instances = []
        user.save()
        custom_user_instances.append(user)
        group = Group.objects.get(name='Admins')
        group.user_set.add(user)
        first_custom_user_instance = custom_user_instances[0] if custom_user_instances else None
        
        admin.user = first_custom_user_instance
        admin.save()
        
        messages.success(request, "New Admin Created Successfully")
        return redirect('/admin_panel')



# -----------------------------------------------------------------------------MANAGE NEWS
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def manage_news(request):
    form = NewsForm()
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_title = form.cleaned_data['information']
            # Create a notification message for all customers
            notification_message = f'New news: {news_title}. Check it out now!'
            # Get all customers
            customers = Customer.objects.all()
            # Create a notification for each customer
            for customer in customers:
                Notification.objects.create(customer=customer, notification_type='NEWS', message=notification_message)
            form.save()
            return redirect('/admin_panel')
    
    news = News.objects.all()
    context = {"news": news, "form": form}
    return render(request, "manage_news.html", context)


# -----------------------------------------------------------------------------VERIFY DOCTOR
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def verify_doctors(request):
    doctors = Doctor.objects.filter(is_verified = False)
    return render(request, 'verify_doctors.html',{"doctors": doctors})


# ! --------------------------------------------------------------------------------------------------FUNCTIONS

# ! -----------------------------------------------------------------------------DOCTOR VERIFICATION
@allowed_users(allowed_roles=["Admins"])
def verification(request, doctor_id):
    doctor_user = get_object_or_404(User, pk=doctor_id)
    doctor = doctor_user.doctor
    if doctor:
        doctor.is_verified = True
        doctor_user.is_active = True
        os.remove(doctor.certifications.path)
        doctor_user.save()
        doctor.save()
        messages.success(request, f'{doctor.user.name} Verified Successfully')
        return redirect('verify_doctors')


# ! -----------------------------------------------------------------------------GET REDIRECT URL
def get_redirect_url(request):
    # Get the stored referrer from session, or default to '/'
    return request.session.get('referrer', '/')


# ! -----------------------------------------------------------------------------DELETE NEWS
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def delete_news(request, news_id):
    news_instance = get_object_or_404(News, pk=news_id)
    if request.method == 'POST':
        news_instance.delete()
        return redirect('manage_news')  
    return render(request, 'manage_news.html')  


# ! -----------------------------------------------------------------------------RECEIVE MESSAGE
@login_required(login_url='login')
def receive_message(request, sender_id):
    
    user = request.user

    if user.groups.filter(name='Customers').exists():
        customer = request.user.customer
        doctor = get_object_or_404(User, pk=sender_id)
        chat = Chat.objects.filter(customer = customer, doctor = doctor.doctor).first()
        
        messages = ChatMessage.objects.filter(msg_sender = doctor, msg_receiver = user, chat = chat)
        
        arr = []
        arr_time = []
        for message in messages:
            arr.append(message.content)
            arr_time.append(message.timestamp)

        context = {
        "body": arr,
        "time": arr_time
        }
        
    if user.groups.filter(name='Doctors').exists():
        doctor = request.user.doctor
        customer = get_object_or_404(User, pk=sender_id)
        chat = Chat.objects.filter(customer = customer.customer, doctor = doctor).first()
        
        messages = ChatMessage.objects.filter(msg_sender = customer, msg_receiver = user, chat = chat)
        
        arr = []
        arr_time = []
        for message in messages:
            arr.append(message.content)
            arr_time.append(message.timestamp)
        
        context = {
        "body": arr,
        "time": arr_time
        }
        
    return JsonResponse(context, safe = False)


# ! -----------------------------------------------------------------------------SEND MESSAGE
@allowed_users(allowed_roles=["Doctors","Customers"])
@login_required(login_url='login')
def send_message(request, receiver_id):
    data = json.loads(request.body)
    new_message = data["msg"]
    user = request.user
    if not new_message.strip():  # Check if the message contains only whitespace characters
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    if user.groups.filter(name='Customers').exists():
        customer = request.user.customer
        doctor = get_object_or_404(User, pk=receiver_id)
        chat = Chat.objects.filter(customer = customer, doctor = doctor.doctor).first()
        message = ChatMessage.objects.create(content = new_message, msg_sender = user, msg_receiver = doctor, chat = chat,seen = False)
    
    if user.groups.filter(name='Doctors').exists():
        doctor = request.user.doctor
        customer = get_object_or_404(User, pk=receiver_id)
        chat = Chat.objects.filter(customer = customer.customer, doctor = doctor).first()
        message = ChatMessage.objects.create(content = new_message,
                                                msg_sender = user,
                                                msg_receiver = customer,
                                                chat = chat,seen = False)

    context = {
        "body":message.content,
        "time":message.timestamp
    }

    return JsonResponse(context, safe = False)


# ! -----------------------------------------------------------------------------CREATE CHAT
@login_required(login_url='login')
@allowed_users(allowed_roles=["Doctors","Customers"])
def make_chat(request, doctor_id):

    doctor = User.objects.filter(id=doctor_id).first().doctor
    
    if request.method == 'POST':
        customer= request.user.customer
        existing_chat = Chat.objects.filter(customer=customer, doctor=doctor).exists()
        if existing_chat:
            # Redirect to some page indicating that a chat already exists
            return redirect(reverse('chat_details', args=[doctor_id]))
        
        Chat.objects.create(customer = customer, doctor=doctor)
        
        return redirect(reverse('chat_details', args=[doctor_id]))


# ! -----------------------------------------------------------------------------DELETE ACCOUNT
@login_required(login_url='login')
def delete_account(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    
    if request.user.groups.filter(name='Admins').exists():
        if request.method == 'POST':
            if hasattr(user, 'doctor'):
                os.remove(user.doctor.profile_photo.path)
            user.delete()
        return redirect('/admin_panel')
            
    if request.user.groups.filter(name='Customers').exists():
        request.user.delete()
        return redirect('/')
    
    if request.user.groups.filter(name='Doctors').exists():
        os.remove(request.user.doctor.profile_photo.path)
        request.user.delete()
        return redirect('/')
        
    return redirect('/')


# ! -----------------------------------------------------------------------------UPDATE APPOINTMENT STATUS  
@login_required(login_url='login')
@allowed_users(allowed_roles=["Doctors"])
def update_status(request, appointment_id):

    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    appointment = get_object_or_404(Appointment, id=appointment_id)
    new_status = request.POST.get('new_status')
    appointment.status = new_status
    appointment.save()
    doctor = appointment.doctor
    if new_status == 'Done':
        doctor.appointments_count += 1
        doctor.reviews+=1
        doctor.save()

    return JsonResponse({'success': True})  


# ! -----------------------------------------------------------------------------CANCEL APPOINTMENT  
@login_required(login_url='login')
@allowed_users(allowed_roles=["Doctors", "Customers"])
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)
    customer = appointment.customer
    if request.user.groups.filter(name='Customers').exists():
        # Create a notification message
        notification_message = f'Your appointment with Dr. {appointment.doctor.user.name} has been canceled.'
        # Create a notification instance for the customer
        Notification.objects.create(customer=request.user.customer, notification_type='CANCELED', message=notification_message)
    
    if request.user.groups.filter(name='Doctors').exists():
        # Create a notification message
        notification_message = f'Your appointment with Dr. {appointment.doctor.user.name} has been canceled due to some circumstances.'
        # Create a notification instance for the customer
        Notification.objects.create(customer=appointment.customer, notification_type='DOCTOR_CANCELED', message=notification_message)
    
    appointment.delete()
    customer.appointments_count -= 1
    customer.save()
    
    if request.user.groups.filter(name='Customers').exists():
        messages.error(request, 'Appointment Canceled successfully!')
        return redirect("/")
    
    messages.error(request, 'Appointment Canceled successfully!')
    return redirect('/clinic_management_system')


# ! -----------------------------------------------------------------------------LOGOUT
@login_required(login_url='login')
def logout(request):
    Logout(request)
    messages.info(request, 'You Logged Out Successfully!')
    return redirect('/')


# ! -----------------------------------------------------------------------------DELETE REVIEW
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def delete_review(request, review_id):

    review = get_object_or_404(Feedback, id=review_id)
    doctor = review.doctor
    doctor.reviews -= 1
    review.delete()
    doctor.save()
    
    return redirect('/admin_panel')


# ! -----------------------------------------------------------------------------DELETE SUPPORT TEAM MESSAGE
@allowed_users(allowed_roles=["Admins"])
@login_required(login_url='login')
def delete_message(request, message_id):
    
    message = get_object_or_404(SupportTeamMessage, id=message_id)
    if request.method == 'POST':
        message.delete()
        return redirect('admin_panel')


# ! -----------------------------------------------------------------------------OFFLINE APPOINTMENT MANAGEMENT
@allowed_users(allowed_roles=["Doctors"])
@login_required(login_url='login')
def offline_appointment(request):
    
    if request.method == 'POST':
        doctor = request.user.doctor
        doctor_price = doctor.price
        doctor_offer_percentage = doctor.offer_percentage
        doctor_offer_price = doctor_price - (doctor_price*doctor_offer_percentage)
        date = request.POST.get('date')
        time = request.POST.get('time')
        offline_customer_name = request.POST.get('offline_customer_name')
        offline_customer_phone = request.POST.get('offline_customer_phone')
    
        existing_appointments = Appointment.objects.filter(doctor=doctor, date=date, time=time)
        
        if existing_appointments.exists():
            messages.error(request, f'Doctor already has an appointment at {date} on {time}. Please choose another time.')
            return JsonResponse({'success': True})  
        else:
            Appointment.objects.create(
                doctor=doctor,
                appointment_price=doctor_offer_price,
                date=date,
                time=time,
                offline_customer_name=offline_customer_name,
                offline_customer_phone=offline_customer_phone
            )
            messages.success(request, 'Appointment created successfully!')
            return JsonResponse({'success': True})


# ! -----------------------------------------------------------------------------CREATE OFFER
@allowed_users(allowed_roles=["Doctors"])
@login_required(login_url='login')
def make_offer(request):
    if request.method == 'POST':
        
        percentage = request.POST.get('percentage')
        end_date = request.POST.get('end_date')
        doctor = request.user.doctor

        if percentage == "":
            messages.error(request, 'Enter Offer')
            return redirect('clinic_management_system')
            #return JsonResponse({'error': False})
        
        doctor.offer_percentage = percentage
        doctor.offer_end_date = end_date
        doctor.save()
        
        messages.success(request, 'Offer Created successfully!')
        return redirect('clinic_management_system')


# ! -----------------------------------------------------------------------------DELETE OFFER
@allowed_users(allowed_roles=["Doctors"])
@login_required(login_url='login')
def delete_offer(request):
    doctor = request.user.doctor
    doctor.offer_percentage = float(0.0)
    doctor.offer_end_date = None
    
    doctor.save()
    
    messages.success(request, 'Offer Deleted successfully!')
    # Return a JSON response indicating success
    return JsonResponse({'success': True})


# ! -----------------------------------------------------------------------------SENDING ACTIVATION Email
@unauthenticated_user
def activate_email(request, user, to_email):
    mail_subject = "Activate your User Account"
    message = render_to_string("activate_email.html", {
        'user': user.email,
        'domain': get_current_site(request).domain,
        'user_id': urlsafe_base64_encode(force_bytes(user.id)),
        'token': account_activation_token.make_token(user),
        'protocol': "https" if request.is_secure() else 'http'
        })
    email =EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Please go to email: {to_email} and click the link')
    else:
        messages.error(request, f'Problem sending email to {to_email}')


# ! -----------------------------------------------------------------------------ACTIVATING EMAIL
@unauthenticated_user
def activate(request, uidb64, token):
    user_id = get_user_model()
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk= user_id)
    except:
        user = None
    
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Thank your for email verification, Now you can login")
        return redirect('login')
    
    else:
        messages.warning(request, "Your Certification is Being Verified!")
        
    return redirect('/')


# ! -----------------------------------------------------------------------------FORGET PASSWORD
@unauthenticated_user
def reset_password_request(request):
    if request.method =='POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email = email)).first()
            if associated_user:
                mail_subject = "Password Reset Request"
                message = render_to_string("forget_password_email.html", {
                    'user': associated_user.email,
                    'domain': get_current_site(request).domain,
                    'user_id': urlsafe_base64_encode(force_bytes(associated_user.id)),
                    'token': account_activation_token.make_token(associated_user),
                    'protocol': "https" if request.is_secure() else 'http'
                    })
                email = EmailMessage(mail_subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request, """ Password reset Sent to Email """)
                else:
                    messages.error(request, "Email Doesn't Exist Go to SignUp")
                
            else:
                messages.error(request, "Email Doesn't Exist Go to SignUp")
                return redirect('/')
                
            
    form = ResetPasswordForm()
    return render(
        request=request,
        template_name="reset_password.html",
        context={"form":form}
    )


# ! -----------------------------------------------------------------------------PASSWORD RESET
@unauthenticated_user
def passwordResetConfirm(request, uidb64, token):
    user_id = get_user_model()
    try:
        user_id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk= user_id)
        
    except:
        user = None
        
    if user is not None and account_activation_token.check_token(user, token):
        if request.method == "POST":
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your Password is Changed Successfully!")
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
            
        form = SetPasswordForm(user)
        return render(request, 'forget_password.html', {'form': form})
    
    else:
        messages.error(request, "Link is Expired!")
    
    messages.error(request,"Something went wrong, redirecting to home page!")
    return redirect('/')


@allowed_users(allowed_roles=["Customers"])
@login_required(login_url='login')
def mark_notification_as_read(request, notification_id):
    
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    notification = get_object_or_404(Notification, id=notification_id)
    print("notification_id")
    notification.is_read = True
    notification.save()
    return JsonResponse({'success': True})  


def days_until_appointment(appointment_date_str):
    return (datetime.strptime(appointment_date_str, '%A %m/%d').date().replace(year=datetime.now().year) - datetime.now().date()).days

