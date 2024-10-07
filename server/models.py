from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # fullname = models.CharField(max_length=100, unique=False, null = True)
    date_of_birth = models.DateField(default=timezone.now)
    def age(self):
            dob = self.date_of_birth
            tod = datetime.date.today()
            my_age = (tod.year - dob.year) - int((tod.month, tod.day) < (dob.month, dob.day))
            return my_age
    gender = models.CharField(max_length=10, null=True,
        choices=[
            ('Male','Male'),
            ('Female', 'Female')
        ])
    # image = models.ImageField(upload_to = "server/static/server/users/", default = "server/static/server/users/defaultuser.gif", null =True)
    hassurvey = models.IntegerField(default=0)
    
    def __str__(self):
        return self.user.username
    
class UserUrl(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    url = models.CharField(max_length=500, null = True)
    frequency = models.FloatField(default=0)
    robustness = models.FloatField(default=0)
    timestamp = models.DateField(default=timezone.now)
    def __str__(self):
        return self.user.username
    
class UserMusic(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    market = models.CharField(max_length=100)
    genre = models.CharField(max_length=1000)
    singer = models.CharField(max_length=1000)
    def __str__(self):
        return self.user.username
    
class Feedback(models.Model):
    user = models.CharField(max_length=100, null=True, blank=True)
    exp = models.CharField(max_length=300, null=True)
    suggestion = models.CharField(max_length=300, null=True)
    timestamp =  models.DateField(default=timezone.now)
    def __str__(self):
        return self.user

class Token(models.Model):
    lang = models.CharField(max_length=10, null=True, 
                            choices=[('vi','vi'),('en','en')])
    b_token = models.CharField(max_length=100, null=True)
    lat_token = models.CharField(max_length=100, null=True)
    cf_bm = models.CharField(max_length=100, null=True)
    cf_clearance = models.CharField(max_length=100, null=True)
    chat_code = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return self.lang
    