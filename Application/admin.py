from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(User)
admin.site.register(Customer)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Chat)
admin.site.register(Feedback)
admin.site.register(Admin)
admin.site.register(News)
admin.site.register(SupportTeamMessage)
admin.site.register(Notification)

