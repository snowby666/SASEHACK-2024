from django import forms
from . import models
from django.core.validators import RegexValidator
GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]
class CustomDateInput(forms.widgets.DateInput):
    input_type = 'date'
class UserForm(forms.ModelForm):
    password = forms.CharField(max_length=150, label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'pattern': '(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$',
               'title': 'Tối thiểu 8 ký tự, ít nhất 1 chữ cái và 1 số', 'class': 'modal-placeholder' , 'autocomplete': 'on'}))
    confirm = forms.CharField(max_length=150, label='Confirm', widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'modal-placeholder' , 'autocomplete': 'on'}))
    username = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'placeholder': 'Username', 'pattern': '^[A-Za-z][A-Za-z0-9_]{6,12}$', 'title': 'Tối thiểu 6 ký tự, tối đa 12 ký tự và không sử dụng ký tự đặc biệt', 'class': 'modal-placeholder', 'autocomplete': 'on'}))
    
    class Meta():
        model = models.User
        fields = ('username', 'password')
        
class UserProfileInfoForm(forms.ModelForm):
    # fullname = forms.CharField(
    #     max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Fullname', 'class': 'modal-placeholder'}))
    date_of_birth = forms.DateField(widget=CustomDateInput(attrs={'placeholder': 'Date Of Birth', 'class': 'modal-placeholder'}))
    gender = forms.CharField(max_length=10, widget=forms.Select(choices=GENDER_CHOICES, attrs={'placeholder': 'Gender', 'class': 'modal-placeholder'}))
    # image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'modal-placeholder'}))

    class Meta():
        model = models.UserProfileInfo
        exclude = ('user', 'hassurvey', )
        
class FeedbackForm(forms.ModelForm):
    user = forms.CharField(required=False, max_length=100, widget=forms.TextInput(attrs={'placeholder': 'What should we call you', 'class': 'modal-placeholder', 'autocomplete': 'off'}))
    exp = forms.CharField(
        max_length=100, widget=forms.TextInput(attrs={'placeholder': "We'd love to hear more of your story", 'class': 'modal-placeholder', 'autocomplete': 'off'}))
    suggestion = forms.CharField(
        max_length=500, widget=forms.TextInput(attrs={'placeholder': 'Your suggestions are valuable to us', 'class': 'modal-placeholder', 'autocomplete': 'off'}))
    class Meta():
        model = models.Feedback
        exclude = ('timestamp', )