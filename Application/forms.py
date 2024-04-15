
# ? -------------------------------------------------------------------------------------------------------IMPORTING LIBRARIES
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import SetPasswordForm, PasswordResetForm




# -----------------------------------------------------------------------------CHAT MESSAGE FORM
class ChatMessageForm(ModelForm):
    
    class Meta:
        model = ChatMessage
        fields = ["content",]

# -----------------------------------------------------------------------------NEWS FORM
class NewsForm(ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        exclude = ['date']


class SupportTeamMessageForm(ModelForm):
    class Meta:
        model = SupportTeamMessage
        fields = ['message']
        exclude = ['customer', 'date']


class MakeOfferForm(ModelForm):
    class Meta:
        model = Doctor
        fields = ['offer_percentage', 'offer_end_date']


class ForgetPasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields= ['password1', 'password2']


class ResetPasswordForm(PasswordResetForm):
    class Meta:
        model = User
        fields= ['email']