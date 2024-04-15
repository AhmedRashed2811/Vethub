
# ? -------------------------------------------------------------------------------------------------------IMPORTING LIBRARIES
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator,MaxValueValidator, MinValueValidator
from django.contrib.auth.models import  AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.core.files.storage import default_storage
from django.utils.deconstruct import deconstructible
import os
from uuid import uuid4 
from django_resized import ResizedImageField


@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.path = sub_path

    def __call__(self, instance, filename):
        upload_to = self.path
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(upload_to, filename)

def delete_file(path):
    if default_storage.exists(path):
        default_storage.delete(path)


#  -------------------------------------------------------------------------------------------------------MODELS

# -----------------------------------------------------------------------------USER
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    # Add custom fields
    username = None
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=100, null=False, default="")
    phone_number = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^01[0-9]{9}$',
                message="Phone number must be entered in the format: '01*******'"
            )
        ],
        null =False, 
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def has_module_perms(self, app_label):
        return self.is_staff


# -----------------------------------------------------------------------------CUSTOMER
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    chats = models.ManyToManyField('Chat', related_name="customer_chats", null=True, blank=True)
    appointments_count = models.IntegerField(null=True,blank=True, default=0)
    
    def __str__(self):
        return self.user.email


# -----------------------------------------------------------------------------DOCTORS
class Doctor(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)
    profile_photo = ResizedImageField(quality=80, upload_to=PathAndRename('Profile_Photos'), null=False, blank=False)
    certifications = ResizedImageField(size=[800, 600], quality=80, upload_to=PathAndRename('Certifications'), null=False, blank=False)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2)
    urgent_examination = models.BooleanField(default = False, null = False)
    city = models.CharField(max_length=100)
    location = models.CharField(max_length=1000, null=True,blank=True)
    governorate = models.CharField(max_length=50)
    offer_percentage = models.DecimalField(max_digits=2, decimal_places=2,default = 0.0, null=True,blank=True) 
    offer_end_date = models.DateField(null=True,blank=True)
    reviews = models.IntegerField(null=True,blank=True, default=0)
    rating = models.DecimalField(
                            null=True,blank=True,
                            default=0,
                            max_digits=2,
                            decimal_places=1,
                            validators=[
                                MaxValueValidator(5),
                                MinValueValidator(0)
                        ])
    chats = models.ManyToManyField('Chat', related_name="doctor_chats",null=True,blank=True)
    is_verified = models.BooleanField(default = False, null = False)
    appointments_count = models.IntegerField(null=True,blank=True, default=0)
    
    def __str__(self):
        return self.user.email
    
    def displayed_price(self):
        return self.price - (self.price * self.offer_percentage)
    
    # def save(self, *args, **kwargs):
    #     # Check if this instance has a primary key (already saved in the database)
    #     if self.pk:
    #         try:
    #             # Retrieve the current instance from the database
    #             current_instance = Doctor.objects.get(pk=self.pk)
    #             # If the profile_photo has changed, delete the previous photo
    #             if current_instance.profile_photo and current_instance.profile_photo != self.profile_photo:
    #                 delete_file(current_instance.profile_photo.path)
    #         except Doctor.DoesNotExist:
    #             pass
        
    #     # Call the parent class's save() method to save the instance
    #     super().save(*args, **kwargs)


# -----------------------------------------------------------------------------APPOINTMENTS
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('On-Going', 'On-Going'),
        ('Done', 'Done'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_price = models.DecimalField(max_digits=5, decimal_places=2)
    date = models.TextField( null=False, blank=False)
    time = models.TextField( null=False, blank=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    offline_customer_name = models.CharField(max_length=100, null=True, blank=True, default="")
    offline_customer_phone = models.CharField(
        max_length=15,
        validators=[
            RegexValidator(
                regex=r'^01[0-9]{9}$',
                message="Phone number must be entered in the format: '01*******'"
            )
        ],
        null =True,
        blank =True, 
    )

    def __str__(self):
        if self.offline_customer_name:
            return f"Appointment: {self.offline_customer_name} with {self.doctor.user.name} on {self.date} at {self.time}"
        
        return f"Appointment: {self.customer.user.name} with {self.doctor.user.name} on {self.date} at {self.time}"


# -----------------------------------------------------------------------------CHATS
class Chat(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.customer.user.name} with dr. {self.doctor.user.name}"


# -----------------------------------------------------------------------------MESSAGES
class ChatMessage(models.Model):
    
    content = models.TextField()
    msg_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_sender")
    msg_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="msg_receiver")
    seen = models.BooleanField(default = False)
    timestamp = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.content


# -----------------------------------------------------------------------------FEEDBACK
class Feedback(models.Model):
    QUESTION_CHOICES = [
        ('Excellent', 'Excellent'),
        ('Good', 'Good'),
        ('Poor', 'Poor'),
    ]
    date = models.DateTimeField(auto_now_add=True)
    inappropriate = models.BooleanField(default = False)
    comment = models.TextField()
    rating = models.DecimalField(
        max_digits=2,
        decimal_places=1,
        validators=[
            MaxValueValidator(5),
            MinValueValidator(0)
        ]
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    question1 = models.CharField(max_length=10, choices=QUESTION_CHOICES, default='Good')
    question2 = models.CharField(max_length=10, choices=QUESTION_CHOICES, default='Good')
    
    def __str__(self):
        return f"{self.customer.user.name} with dr. {self.doctor.user.name}"


# -----------------------------------------------------------------------------ADMIN
class Admin(models.Model):
    user = models.OneToOneField(User, null=True, on_delete = models.CASCADE)

    def __str__(self):
        return self.user.email


# -----------------------------------------------------------------------------NEWS
class News(models.Model):
    information = models.TextField()
    image = models.ImageField( null=False, blank=False)
    date = models.DateField(default=timezone.now)
    
    def __str__(self):
        return self.information


# -----------------------------------------------------------------------------SUPPORT TEAM MESSAGE
class SupportTeamMessage(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Message from ({self.customer})'


# -----------------------------------------------------------------------------NOTIFICATION
class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('CREATED', 'Appointment created'),
        ('CANCELED', 'Appointment canceled'),
        ('APPOINTMENT_DONE', 'Appointment done'),
        ('DOCTOR_CANCELED', 'Doctor canceled appointment'),
        ('REMINDER', 'Appointment reminder'),
        ('NEWS' , 'News added')
    )

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_date = models.DateField(auto_now_add=True)
    created_time = models.TimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.customer.user.name} - {self.notification_type}'

    class Meta:
        ordering = ['-created_date', '-created_time']

