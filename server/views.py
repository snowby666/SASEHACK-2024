import numpy as np
import dlib
import cv2
import base64
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.exceptions import StopConsumer
from scipy.spatial import distance as dist
from imutils import face_utils
import datetime
from datetime import datetime
# import re
from django.shortcuts import get_object_or_404, render, redirect
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.db.models import Count, F, Q, Value
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from StressAPI.settings import EMAIL_HOST_USER
# from django.core.mail import send_mail
# from django.core.mail import EmailMultiAlternatives
from . import models
from django.utils import timezone
from django.http import HttpResponse, StreamingHttpResponse, JsonResponse
import os
import csv
from . import forms
import pickle
from .musicplayer import getmusic
from .futurepred import futurepred
import random
import time
from asgiref.sync import sync_to_async
import asyncio
# import poe
# from .poe2 import poe
from poe_api_wrapper import PoeApi


DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#importing frontal facial landmark detector     
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(DIR+'/server/models/shape_predictor_68_face_landmarks.dat')
#loading the trained model
emotion_classifier = load_model(DIR+'/server/models/_mini_XCEPTION.102-0.66.hdf5', compile=False)
scope_user = {}
HOTLINE_PROMPT = [
    'hotline','tổng đài','đường dây nóng','đường dây tư vấn','liên hệ tư vấn','số điện thoại tư vấn','nói chuyện với người','trò chuyện với người','nói với người','gọi điện tư vấn','tư vấn với người',
    'switchboard', 'counseling', 'consulting', 'talk to a person', 'chat with a person', 'speak with a person', 'call for counseling', 'counsel with a person'
]

class ChatBot():
    def __init__(self, lang):
        self.lang = lang
        self.b_token = models.Token.objects.get(lang=self.lang).b_token
        self.lat_token = models.Token.objects.get(lang=self.lang).lat_token
        try:
            self.cf_bm = models.Token.objects.get(lang=self.lang).cf_bm
            self.cf_clearance = models.Token.objects.get(lang=self.lang).cf_clearance
        except:
            self.cf_bm = None
            self.cf_clearance = None
        self.chat_code = models.Token.objects.get(lang=self.lang).chat_code
        try:
            self.server = PoeApi(tokens={'p-b': self.b_token, 'p-lat': self.lat_token})
            models.Token.objects.filter(lang=self.lang).update(status=True)
        except:
            self.server = ''
            models.Token.objects.filter(lang=self.lang).update(status=False)

    def reconnect(self):
        self.b_token = models.Token.objects.get(lang=self.lang).b_token
        self.lat_token = models.Token.objects.get(lang=self.lang).lat_token
        try:
            self.cf_bm = models.Token.objects.get(lang=self.lang).cf_bm
            self.cf_clearance = models.Token.objects.get(lang=self.lang).cf_clearance
        except:
            self.cf_bm = None
            self.cf_clearance = None
        self.chat_code = models.Token.objects.get(lang=self.lang).chat_code
        try:
            self.server = PoeApi(tokens={'p-b': self.b_token, 'p-lat': self.lat_token})
            models.Token.objects.filter(lang=self.lang).update(status=True)
        except:
            self.server = ''
            models.Token.objects.filter(lang=self.lang).update(status=False)
        
    def response(self, message):
        for i in HOTLINE_PROMPT:
            if i in message.lower():
                return ['Bạn có thể gọi đến các đường dây nóng sau để được tư vấn tâm lý miễn phí 24 trên 7 nhé:','- National Suicide Prevention Lifeline: 1 800 273 8255','- Crisis center: 813 964 1964','- Mental Health America: 703 684 7722']
        if models.Token.objects.get(lang=self.lang).status == True:   
            for chunk in self.server.send_message('codestressvn', message + ' (tiếp tục chỉ trả lời bằng tiếng Việt với giọng nói tự nhiên và gần gũi nhất có thể)', chatCode=self.chat_code):
                pass
            return chunk['text']
        else:
            viebot.reconnect()
            return 'Chatbot đang được bảo trì, vui lòng quay lại sau'
        
    def flush(self):
        if models.Token.objects.get(lang=self.lang).status == True:   
            try:
                self.server.purge_conversation("codestressvn", chatCode=self.chat_code)  
            except:
                pass 
    def clear(self):
        if models.Token.objects.get(lang=self.lang).status == True:
            try:
                self.server.chat_break("codestressvn", chatCode=self.chat_code)
            except:
                pass
        
    def enresponse(self, message):
        for i in HOTLINE_PROMPT:
            if i in message.lower():
                return ['If you live in Vietnam and are seeking mental health support, these hotlines may help:','- National Suicide Prevention Lifeline: 1 800 273 8255','- Crisis center: 813 964 1964','- Mental Health America: 703 684 7722']
        if models.Token.objects.get(lang=self.lang).status == True: 
            for chunk in self.server.send_message('codestressen', message + ' (keep only answering in English with the most natural and intimate voice)', chatCode=self.chat_code):
                pass
            return chunk['text']
        else:
            engbot.reconnect()
            return 'Chatbot is under maintenance, please come back later'
    def enflush(self):
        if models.Token.objects.get(lang=self.lang).status == True: 
            try:
                self.server.purge_conversation("codestressen", chatCode=self.chat_code)  
            except:
                pass 
    def enclear(self):
        if models.Token.objects.get(lang=self.lang).status == True: 
            try:
                self.server.chat_break("codestressen", chatCode=self.chat_code) 
            except:
                pass

try:
    viebot = ChatBot('vi')
    if models.Token.objects.get(lang='vi').status == True:
        try:
            viebot.flush() 
        except:
            pass
    engbot = ChatBot('en')
    if models.Token.objects.get(lang='en').status == True:
        try:
            engbot.flush()
        except:
            pass
except:
    print('Failed to connect to the chatbot server')

def chatbot(request):
    if request.method == "POST":
        try:
            if request.POST.get('lang') == 'vi':
                try:
                    if request.POST.get('sendform') != None:
                        message = request.POST.get('sendform')
                        response = viebot.response(message)
                        if 'As an AI language model' not in response:
                            return JsonResponse({'response':response})
                        else:
                            viebot.clear()
                            return JsonResponse({'response':'Tôi không thể trả lời câu hỏi nhạy cảm này, vui lòng thử lại'})
                    if request.POST.get('flushform') == '1':
                        # viebot.flush()
                        viebot.clear()
                        return JsonResponse({'response':'Đã làm mới cuộc trò chuyện'})
                except:
                    viebot.reconnect()
                    return JsonResponse({'response':'Lỗi kết nối, vui lòng thử lại'})
            else:
                try:
                    if request.POST.get('sendform') != None:
                        message = request.POST.get('sendform')
                        response = engbot.enresponse(message)
                        if 'As an AI language model' not in response:
                            return JsonResponse({'response':response})
                        else:
                            engbot.enclear()
                            return JsonResponse({'response':'I cannot answer this sensitive question, please try again'})
                    if request.POST.get('flushform') == '1':
                        # engbot.enflush()
                        engbot.enclear()
                        return JsonResponse({'response':'Conversation has been cleared'})
                except:
                    engbot.reconnect()
                    return JsonResponse({'response':'Connection error, please try again'})   
        except:
            if request.POST.get('lang') == 'vi':
                viebot.reconnect()
                return JsonResponse({'response':'Chatbot đang được bảo trì, vui lòng quay lại sau'})
            else:
                engbot.reconnect()
                return JsonResponse({'response':'Chatbot is under maintenance, please come back later'})

class Client:
    def __init__(self, username):
        self.username = username
        self.mode = 0
        self.points = []
        self.points_lip = []
        self.points_leye = []
        self.points_reye = []
        self.mean_value = 0
        self.std_value = 0
        self.dataset = []
        self.stress_range = []
        
        self.duration = 8000
        self.trackurl = ''
        self.artist = ''
        self.trackname = ''
        self.moodlabel = ''
        self.getemotion = ''
        self.status = False
        
        self.autoartistlist = []
        self.autogenres = []
        self.automarket = ''
        
    def music(self):
        self.duration = 8000
        self.trackurl = ''
        self.artist = ''
        self.trackname = ''
        self.moodlabel = ''
        self.getemotion = ''
        self.status = False
    
    def clearall(self):
        self.points = []
        self.points_lip = []
        self.points_leye = []
        self.points_reye = []
        self.mean_value = 0
        self.std_value = 0
        self.stress_range = []
        
    def cleardata(self):
        self.dataset = []
        
    def update(self):
        #Get User Info for automodemusic
        try:
            self.findsinger = models.UserMusic.objects.filter(user__username=self.username).values('singer')[0]['singer']
            self.splitsingers = self.findsinger[1:-1].split(',')
            self.autoartistlist = []
            for x in self.splitsingers:
                self.autoartistlist.append(x.replace("'","").strip())
            self.findgenre = models.UserMusic.objects.filter(user__username=self.username).values('genre')[0]['genre']
            self.editgenre = self.findgenre[1:-1].split(',')
            self.autogenres = []
            for y in self.editgenre:
                self.autogenres.append(y.replace("'","").strip())
            self.automarket = models.UserMusic.objects.filter(user__username=self.username).values('market')[0]['market']
        except:
            pass
    
# web service
def error_404(request, exception):
    return render(request, 'server/404.html')

def error_500(request):
    return render(request, 'server/500.html')

def error(request, exception):
    return redirect('server:index.html')

def sitemap(request):
    return render(request, 'server/sitemap.xml', content_type = 'text/xml')

def manifest(request):
    return render(request, 'server/manifest.json', content_type = 'application/json')
    
def index(request):
    global username
    username = request.session.get('username', 0)
    login_result = 0
    registered = 2
    trigger = 1
    
    if username != 0:
        for i in range(0,8):
            if (os.path.isfile(DIR+'/server/static/server/data/{}_{}.csv'.format(username, i)) == False):
                with open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, i), 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
                    f.close()
                
        if username not in scope_user:
            scope_user[username] = Client(username)
        else:
            scope_user[username].clearall()
            scope_user[username].cleardata()
            scope_user[username].music()
        scope_user[username].update()
            
        #Trigger the survey form if user hasnt done yet
        if models.UserProfileInfo.objects.filter(user=request.user).values('hassurvey')[0]['hassurvey'] == 0:
            trigger = 0  
                           
    # Save the user data
    # Checking if the user has submitted the survey. If they have, it will save the data to the database.
    # If they have not, it will redirect them to the survey page.
    if request.method == "POST" and request.POST.get("market") is not None and request.POST.get("genre") is not None and username != 0:
        formattedsinger = [i for i in request.POST.getlist("singer") if i != '']
        data = models.UserMusic(
        user = request.user, 
        market = request.POST.get("market"), 
        genre = request.POST.getlist("genre"),
        singer = formattedsinger)
        data.save()
        models.UserProfileInfo.objects.filter(user__username=username).update(hassurvey=1)
        return redirect('server:index.html')
            
    # if checkpoint == True:
    #     checkpoint = False
    #     return render(request, 'server/index.html' ,{'trigger':trigger})
    
    # User Feedback
    if request.method == "POST" and request.POST.get("feedback") == "1":
        form_feed = forms.FeedbackForm(data=request.POST)       
        if (form_feed.is_valid()):
            feed_data = form_feed.save(commit=False) 
            if username != 0:
                feed_data.user = username
            else:
                if feed_data.user == "":
                    feed_data.user = "Anonymous"
            feed_data.save() 
        return redirect('server:index.html')
    else:
        form_feed = forms.FeedbackForm()
        
    # User Signup
    if request.method == "POST" and request.POST.get("signup") == "1":
        form_user = forms.UserForm(data=request.POST)       
        form_por = forms.UserProfileInfoForm(data=request.POST) 
        if (form_user.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
            user = form_user.save()   
            user.set_password(user.password)         
            user.save()     
             
            profile = form_por.save(commit=False)
            profile.user = user
            # if 'image' in request.FILES:
            #     profile.image = request.FILES['image']
            profile.save()
             
            registered = 1
            username = request.POST.get("username")
            for i in range(0,8): 
                with open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, i), 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
                    f.close()
                if i != 0:
                    models.UserUrl.objects.get_or_create(user=user, url='/server/static/server/data/{}_{}.csv'.format(username, i), timestamp=timezone.now())
            return render(request, 'server/index.html', {'form_user': form_user, 'form_por': form_por, 'registered': registered, 'form_feed': form_feed})
             
        if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
            registered = 2
            form_user.add_error('confirm', 'Mật khẩu xác nhận khác mật khẩu')
            return render(request, 'server/index.html', {'form_user': form_user, 'form_por': form_por, 'registered': registered, 'form_feed': form_feed})
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()   
        
    # User Login
    if request.method == "POST" and request.POST.get("login") == "1":
        username = request.POST.get("username")
        password = request.POST.get("password")
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()   
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            username = request.session.get('username', 0)
            login_result = 1
            if models.UserProfileInfo.objects.filter(user__username=username).values('hassurvey')[0]['hassurvey'] == 0:
                trigger = 0
            return render(request,'server/index.html',{'form_user': form_user, 'form_por': form_por, 'login_result': login_result, 'username': username, 'trigger':trigger, 'form_feed': form_feed})
        else:
            login_result = 2
            return render(request, 'server/index.html', {'form_user': form_user, 'form_por': form_por,'login_result': login_result, 'trigger':trigger, 'form_feed': form_feed})
    
    if registered == 2 or login_result == 1:
        return render(request, 'server/index.html', {'form_user': form_user, 'form_por': form_por, 'registered': registered, 'username': username, 'trigger':trigger, 'form_feed': form_feed})
    else:
        return render(request, 'server/index.html', {'form_user': form_user, 'form_por': form_por, 'registered': registered, 'form_feed': form_feed})
    
@login_required(login_url='server:index.html') 
def analysis(request):
    global username
    username = request.session.get('username', 0)
    profile = models.UserProfileInfo.objects.get(user__username=username)
    slots = ['No. 1', 'No. 2', 'No. 3', 'No. 4', 'No. 5', 'No. 6', 'No. 7']
    ranks = ['Least Popular', 'Most Popular']
    url = '0'
    notify = '0'
    label = ''
    disslot = 'No. 1'
    selectedslot = 'No. 1'
    error = '0'
    
    if username != 0:
        for i in range(0,8):
            if (os.path.isfile(DIR+'/server/static/server/data/{}_{}.csv'.format(username, i)) == False):
                with open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, i), 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
                    f.close()       
        if username not in scope_user:
            scope_user[username] = Client(username)
        else:
            scope_user[username].clearall()
            scope_user[username].cleardata()
            scope_user[username].music()
        scope_user[username].update()
    
    #video controller
    if request.method == "POST":
        if request.POST.get('changemode') == '0':
            scope_user[username].mode = 0
            reset(username)
        elif request.POST.get('changemode') == '1':
            scope_user[username].mode = 1
            reset(username)
    else:
        scope_user[username].mode = 0
            
    if request.method == "POST" and request.POST.get('sender') == '-1':
        # try:
        #     classifier(mean_latest, std_latest, stress_range)
        # except Exception:
        #     pass
        if username != 0:
            reset(username)
    elif request.method == "POST" and request.POST.get('sender2') == '1':
        pass

    if request.method == "POST" and request.POST.get("slot"):
        getslot = request.POST.get('slot')
        selectedslot = getslot
        if getslot == 'No. 1':
            slot = '1'
        elif getslot == "No. 2":
            slot = '2'
        elif getslot == "No. 3":
            slot = '3'
        elif getslot == "No. 4":
            slot = '4'
        elif getslot == "No. 5":
            slot = '5'
        elif getslot == "No. 6":
            slot = '6'
        else:
            slot = '7'
        #save the data
        if request.POST.get("save") == "1":
            scope_user[username].cleardata()
            with open(DIR+'/server/static/server/data/{}_0.csv'.format(username), newline="") as csvfile:
                reader = csv.reader(csvfile)
                scope_user[username].dataset.append(next(reader))
                for row in reader:
                    scope_user[username].dataset.append(row)    
                csvfile.close()          
            with open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, slot), "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(scope_user[username].dataset)
                csvfile.close()
            
            #save the features for the future prediction
            stress_value_list = []
            with open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, slot), 'r') as f:
                f_reader = csv.reader(f, delimiter=' ')
                value_list = list(list(f_reader)[-1][-1].split(','))
                try:
                    mean = value_list[2]
                    std = value_list[3]
                except Exception:
                    mean = 0
                    std = 0         
                f.close()   
            filename = open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, slot), 'r')
            file = csv.DictReader(filename)
            for col in file:
                stress_value_list.append(float(col['Value']))
            filename.close()
            try:
            
                #check if data exists on the same date
                checkdate = datetime.now().date()
                if models.UserUrl.objects.filter(user__username=username, timestamp=checkdate):
                    models.UserUrl.objects.filter(user__username=username, timestamp=checkdate).update(frequency=0,robustness=0)     
                models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, slot)).update(timestamp=timezone.now(),
                                                                                                                                            frequency=datafeatures(mean,std,stress_value_list)[0],
                                                                                                                                            robustness=datafeatures(mean,std,stress_value_list)[1]
                                                                                                                                            )
            except Exception:
                pass
    
    #clear the current data from home
    with open(DIR+'/server/static/server/data/{}_0.csv'.format(username), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
    dismarket = models.UserMusic.objects.filter(user=request.user).values('market')[0]['market']
    if dismarket == 'CN':
        dismarket = "China"
    elif dismarket == 'JP':
        dismarket = "Japan"
    elif dismarket == 'IN':
        dismarket = "India"
    elif dismarket == 'KR':
        dismarket = "Korea"
    elif dismarket == 'VN':
        dismarket = "Vietnam"

    getsinger = models.UserMusic.objects.filter(user=request.user).values('singer')[0]['singer']
    singers = getsinger[1:-1].split(',')
    disartistlist = []
    for x in singers:
        disartistlist.append(x.replace("'","").strip())
    getgenre = models.UserMusic.objects.filter(user=request.user).values('genre')[0]['genre']
    formatgenre = getgenre[1:-1].split(',')
    disgenres = []
    for y in formatgenre:
        disgenres.append(y.replace("'","").strip())
    disgenres = disgenres[0:8]
    
    # Updating the user's music preference in the database.
    if request.method == "POST" and request.POST.get("preference") == "1" and username != 0:
        if request.POST.get("market") is not None and request.POST.get("genre") is not None:
            formattedsinger = [i for i in request.POST.getlist("singer") if i != '']
            models.UserMusic.objects.filter(user__username=username).update(
            market = request.POST.get("market"), 
            genre = request.POST.getlist("genre"),
            singer = formattedsinger)
            return redirect('server:analysis')
    
    #predict model
    # Getting the data from the database and storing it in a list.
    if request.method == "POST" and request.POST.get("regression") == "1" and username != 0:
        reg_data_x = []
        reg_data_y = []
        reg_time = []
        reg_data = []
        reg_dataset = []
        for order in range(1,8):
            getfreq = models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, order)).values('frequency')[0]['frequency']
            getrobust = models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, order)).values('robustness')[0]['robustness']
            getdate = models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, order)).values('timestamp')[0]['timestamp']
            reg_data_x.append(getfreq)
            reg_data_y.append(getrobust)
            reg_time.append(f'{getdate}')
            if getfreq != 0 or getrobust != 0:
                reg_data.append([getfreq,getrobust,f'{getdate}'])
        prediction = '0'
        getfuturepred = futurepred(reg_data)
        reg_dataset = getfuturepred[0]
        trend = getfuturepred[1]
    else:
        trend = '0'
        prediction = '1'
        reg_dataset = [['Date'],['Estimation'],['Regression']]
        
    if request.method == "POST" and request.POST.get("load") == "1" and username != 0:
        slot = request.POST.get('slot')
        loadslot = slot
        if slot == 'No. 1':
            loadfile = 1
        elif slot == "No. 2":
            loadfile = 2
        elif slot == "No. 3":
            loadfile = 3
        elif slot == "No. 4":
            loadfile = 4
        elif slot == "No. 5":
            loadfile = 5
        elif slot == "No. 6":
            loadfile = 6
        else:
            loadfile = 7
        gettimestamp = models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, str(loadfile))).values('timestamp')[0]['timestamp']
        timestamp = f'Here is your {slot} health report recorded on {gettimestamp}'
            
        filename = open(DIR+'/server/static/server/data/{}_{}.csv'.format(username, slot[-1]), 'r')
        file = csv.DictReader(filename)
        chartdata = [['Frame'],['Value'],['Mean'],['Standard Deviation']]
        for col in file:
            chartdata[0].append(int(col['Frame']))
            chartdata[1].append(float(col['Value']))
            chartdata[2].append(float(col['Mean']))     
            chartdata[3].append(float(col['Standard Deviation'])) 
        filename.close()
    else:
        chartdata = [['Frame'],['Value'],['Mean'],['Standard Deviation']]
        loadfile = 0
        timestamp = ''
        loadslot = 'No. 1'
            
   # The below code is a part of the view function in the views.py file. It is a part of the
   # recommendation system. It is a part of the code that is executed when the user clicks on the
   # "Recommend" button.
    if request.method == "POST" and request.POST.get("recommend") == "1" and username != 0:
        slot = request.POST.get('slot')
        disslot = slot
        if slot == 'No. 1':
            slot = '1'
        elif slot == "No. 2":
            slot = '2'
        elif slot == "No. 3":
            slot = '3'
        elif slot == 'No. 4':
            slot = '4'
        elif slot == "No. 5":
            slot = '5'
        elif slot == "No. 6":
            slot = '6'
        else:
            slot = '7'
            
        pop = request.POST.get('rank')
        if pop == "Most Popular":
            pop = 100
        else:
            pop = 0
    
        datafreq = models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, slot)).values('frequency')[0]['frequency']
        datarobust = models.UserUrl.objects.filter(user__username=username, url='/server/static/server/data/{}_{}.csv'.format(username, slot)).values('robustness')[0]['robustness']
           
        getsinger = models.UserMusic.objects.filter(user=request.user).values('singer')[0]['singer']
        singers = getsinger[1:-1].split(',')
        artistlist = []
        for x in singers:
            artistlist.append(x.replace("'","").strip())
        getgenre = models.UserMusic.objects.filter(user=request.user).values('genre')[0]['genre']
        formatgenre = getgenre[1:-1].split(',')
        genres = []
        for y in formatgenre:
            genres.append(y.replace("'","").strip())
        
        market = models.UserMusic.objects.filter(user=request.user).values('market')[0]['market']
        
        prediction = analysis_model(datafreq, datarobust) 
        if prediction != [1, 0.0]:
            try:
                if prediction[0] == 0:
                    if prediction[1] > 0.8:
                        emotion = "Depressed"
                        label = "You seem to be under severe stress!"
                    else:
                        emotion = "Sad"
                        label = "You seem to be under mild stress!"
                else:
                    if prediction[1] > 0.1:
                        emotion = "Happy"
                        label = "You are in a good mood!"
                    else:
                        emotion = "Energetic"  
                        label = "You are better than ever!"
                musicurl = list(getmusic(artistlist, emotion, genres, market, pop, type=0))
                if len(musicurl) > 4:
                    recommendation = random.sample(musicurl ,4)
                    # print(recommendation)
                else:
                    recommendation = musicurl
                if recommendation != []:
                    url = recommendation
                else:
                    #if cant find any songs that match music taste
                    musicurl = list(getmusic(artistlist, emotion, genres, market, pop, type=1))
                    if len(musicurl) > 4:
                        recommendation = random.sample(musicurl ,4)
                    else:
                        recommendation = musicurl  
                    notify = '1'
                    url = recommendation
                    
                if recommendation == []:
                    #if cant find any songs that match music taste and market
                    musicurl = list(getmusic(artistlist, emotion, genres, market, pop, type=2))
                    if len(musicurl) > 4:
                        recommendation = random.sample(musicurl ,4)
                    else:
                        recommendation = musicurl  
                    notify = '1'
                    url = recommendation
            except Exception:
                pass      
        else:
            error = '1'    
        return render(request, 'server/analysis.html', {'username':username,
                                                        'slots':slots,
                                                        'ranks':ranks, 
                                                        'url':url,
                                                        'notify':notify,
                                                        'label':label,
                                                        'profile':profile,
                                                        'dismarket':dismarket,
                                                        'disartistlist':disartistlist,
                                                        'disgenres':disgenres, 
                                                        'loadfile':loadfile,
                                                        'timestamp':timestamp,
                                                        'reg_dataset':reg_dataset,
                                                        'prediction':prediction,
                                                        'loadslot':loadslot,
                                                        'disslot':disslot,
                                                        'selectedslot':selectedslot,
                                                        'error': error,
                                                        'chartdata':chartdata,
                                                        'trend': trend                                                                                          
                                                        })
    if username != 0:
        return render(request, 'server/analysis.html', {'username':username,
                                                        'slots':slots,
                                                        'ranks':ranks, 
                                                        'url':url,
                                                        'notify':notify,
                                                        'label':label,
                                                        'profile':profile,
                                                        'dismarket':dismarket,
                                                        'disartistlist':disartistlist,
                                                        'disgenres':disgenres, 
                                                        'loadfile':loadfile,
                                                        'timestamp':timestamp,
                                                        'reg_dataset':reg_dataset,
                                                        'prediction':prediction,
                                                        'loadslot':loadslot,
                                                        'disslot':disslot,
                                                        'selectedslot':selectedslot,
                                                        'error': error,
                                                        'chartdata':chartdata,
                                                        'trend': trend     
                                                        })
    else: 
        return redirect('server:index.html')
    
#Use knn algorithm to predict stress label
loaded_model = pickle.load(open(DIR+'/server/models/knnfacemodel.pkl', 'rb'))
def knn_model(mean, std, stress_value_list):
    try:
        spread_value = round((float(mean) + float(std)), 4)
        frequency = list(x for x in stress_value_list if x > 0)
        frequency_value = len(frequency)/len(stress_value_list)
        try:
            robust = list(i for i in stress_value_list if i > spread_value)
            robust_value = len(robust)/len(stress_value_list)
        except Exception:
            robust_value = spread_value
        data = [[frequency_value, robust_value]]
        prediction = list(loaded_model.predict(data))
        prediction.append(frequency_value)
        return prediction
    except Exception:
        pass
    
def analysis_model(datafreq, datarobust):
    try:
        data = [[datafreq, datarobust]]
        prediction = list(loaded_model.predict(data))
        prediction.append(datafreq)
        return prediction
    except Exception:
        pass

#extract 2 params from the data
def datafeatures(mean, std, stress_value_list):
    try:
        spread_value = round((float(mean) + float(std)), 4)
        frequency = list(x for x in stress_value_list if x > 0)
        frequency_value = len(frequency)/len(stress_value_list)
        try:
            robust = list(i for i in stress_value_list if i > spread_value)
            robust_value = len(robust)/len(stress_value_list)
        except Exception:
            robust_value = spread_value
        data = [frequency_value, robust_value]
        return data
    except Exception:
        pass

@login_required(login_url='server:index.html')    
def log_out(request):
    form_user = forms.UserForm()
    form_por = forms.UserProfileInfoForm()  
    username = request.session.get('username', 0)
    if username != 0:
        try:
            del scope_user[username]
        except:
            pass
        with open(DIR+'/server/static/server/data/{}_0.csv'.format(username), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
    logout(request)
    return redirect('server:index.html')

#calculating distance of facial features in terms of the facial landmark

def ebdist(leye, reye, username):
    if leye is not None and reye is not None:
        eyedist = dist.euclidean(leye, reye)
        scope_user[username].points.append(int(eyedist))
        return eyedist
    
def lpdist(l_lower,l_upper, username):
    if l_lower is not None and l_upper is not None:
        lipdist = dist.euclidean(l_lower, l_upper)
        scope_user[username].points_lip.append(int(lipdist))
        return lipdist

def leyedist(el_lower,el_upper, username):
    if el_lower is not None and el_upper is not None:
        ledist = dist.euclidean(el_lower, el_upper)
        scope_user[username].points_leye.append(int(ledist))
        return ledist

def reyedist(rl_lower,rl_upper, username):
    if rl_lower is not None and rl_upper is not None:
        redist = dist.euclidean(rl_lower, rl_upper)
        scope_user[username].points_reye.append(int(redist))
        return redist

# def get_stress_range(stress_value, username):
#     #stress_range = [round(((np.exp(-(a+b+c+d)/4))*1000),6) for a,b,c,d in zip(points, points_lip, points_leye, points_reye)]
#     stress_range.append(round(stress_value, 3))
#     return stress_range

def get_std_value(stress_index, username):
    scope_user[username].std_value = (round(np.std(stress_index), 3))
    # for x in std_value:        
    #     std_value[std_value.index(x)] = round(np.std(stress_index), 3)
    return scope_user[username].std_value

def get_mean_value(stress_index, username):
    scope_user[username].mean_value = (round(np.mean(stress_index), 3))
    # for y in mean_value:        
    #     mean_value[mean_value.index(y)] = round(np.mean(stress_index), 3)
    return scope_user[username].mean_value

# def get_top_range(mean, std, username):
#     top_value = mean + std
#     top_range.append(round(top_value, 3))
#     # for m in top_range:        
#     #     top_range[top_range.index(m)] = round(top_value, 3)
#     return top_range

# def get_bottom_range(mean, std, username):
#     bottom_value = mean - std
#     bottom_range.append(round(bottom_value, 3))
#     # for n in bottom_range:        
#     #     bottom_range[bottom_range.index(n)] = round(bottom_value, 3)
#     return bottom_range

#Detect the emotion
EMOTIONS = ["angry", "disgust", "scared", "happy", "sad", "surprised", "neutral"]
def get_emotion(faces, frame):
    try:
        x, y, w, h = face_utils.rect_to_bb(faces)
        roi = cv2.resize(frame[y:y + h, x:x + w], (64, 64))
        roi = roi / 255.0
        roi = np.array([roi]) 

        preds = emotion_classifier.predict(roi)[0]
        # emotion_probability = np.max(preds)
        emotion = EMOTIONS[preds.argmax()]

        return emotion
    except:
        pass

#calculating stress value using the distances (min-max scaling)
def normalize_values(points, disp, points_lip, dis_lip, points_leye, ledist, points_reye, redist, label, username):
    # age = models.UserProfileInfo.objects.get(user__username=username)
    # my_age = age.age()
    max_points = np.max(points)
    min_points = np.min(points)
    max_points_lip = np.max(points_lip)
    min_points_lip = np.min(points_lip)
    max_points_leye = np.max(points_leye)
    min_points_leye = np.min(points_leye)
    max_points_reye = np.max(points_reye)
    min_points_reye = np.min(points_reye)
    
    denom_lip = abs(max_points_lip - min_points_lip)
    denom_points = abs(max_points - min_points)
    denom_leye = abs(max_points_leye - min_points_leye)
    denom_reye = abs(max_points_reye - min_points_reye)
    
    if denom_lip != 0 and denom_points != 0 and denom_leye != 0 and denom_reye != 0:
        normalize_value_lip = abs(dis_lip - min_points_lip)/denom_lip
        normalized_value_eye = abs(disp - min_points)/denom_points
        normalized_value_leye = abs(ledist - min_points_leye)/denom_leye
        normalized_value_reye = abs(redist - min_points_reye)/denom_reye
        normalized_value = (normalized_value_eye * 2 + normalize_value_lip + normalized_value_leye * 0.5 +
                            normalized_value_reye * 0.5) / 4
        stress_value = np.exp(-normalized_value)
    else:
        stress_value = 0
    if label not in ['scared', 'sad', 'angry']:
        stress_value = 0
    
    scope_user[username].stress_range.append(round(stress_value, 3))
    return stress_value
  

#classifiy the data and use it for training the model

def classifier(mean_latest, std_latest, stress_range):
    spread = mean_latest + std_latest
    frequency = list(x for x in stress_range if x > 0)
    frequency_value = len(frequency)/len(stress_range)
    try:
        robust = list(i for i in stress_range if i > spread)
        robust_value = len(robust)/len(stress_range)
    except Exception:
        robust_value = spread
    dict = {'Frequency': frequency_value, 'Robustness': robust_value}

    # with open(DIR+'/server/static/server/model/testmodel.csv', 'a', newline="") as f:
    #     dictwriter_object = DictWriter(f, fieldnames  = ["Frequency","Robustness", "Label"])
    #     dictwriter_object.writerow(dict)
    #     f.close()

def draw_dots(frame, leyebrow, reyebrow, openmouth, lefteye, righteye):
    # Convert the coordinate arrays to a single NumPy array of (x,y) tuples
    coords = np.concatenate([leyebrow, reyebrow, openmouth, lefteye, righteye]).astype(int)
    # Draw circles using cv2.circle() with the array of (x,y) tuples
    for coord in coords:
        cv2.circle(frame, tuple(coord), 1, (255, 238, 227), -1)
    pass

def fps_count():
    try:
        new = time.time()
        fps = int(1/(new-prev))
        prev = new
        return fps
    except cv2.error as e:
        raise e
    
def reset(username):
    scope_user[username].clearall()
    with open(DIR+'/server/static/server/data/{}_0.csv'.format(username), 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Frame", "Value", "Mean", "Standard Deviation"])
            f.close()        

@sync_to_async
def speech(request):
    username = request.session.get('username', 0)
    if (username != 0) and (len(scope_user[username].points) > 150) and (scope_user[username].status == False):
        try:
            automode(scope_user[username].mean_value, scope_user[username].std_value, scope_user[username].stress_range, username)
            automodemusic(scope_user[username].getemotion, username)
            scope_user[username].status = True
            return JsonResponse({
                                'result':scope_user[username].moodlabel,
                                'trackurl':scope_user[username].trackurl,
                                'duration':scope_user[username].duration,
                                'artist':scope_user[username].artist,
                                'trackname':scope_user[username].trackname
                                }) 
        except:
            return JsonResponse({'result':'','trackurl':'','duration':'','artist':'','trackname':''}) 
    else:
        return JsonResponse({'result':'','trackurl':'','duration':'','artist':'','trackname':''}) 
        
def automode(mean, std, stress_value_list, username):
    prediction = knn_model(mean, std, stress_value_list) 
    if prediction is not None:
        try:
            if prediction[0] == 0:
                if prediction[1] > 0.8:
                    scope_user[username].getemotion = "Depressed"
                    scope_user[username].moodlabel = "You seem to be under severe stress!"
                else:
                    scope_user[username].getemotion = "Sad"
                    scope_user[username].moodlabel = "You seem to be under mild stress!"
            else:
                if prediction[1] > 0.1:
                    scope_user[username].getemotion = "Happy"
                    scope_user[username].moodlabel = "You are in a good mood!"
                else:
                    scope_user[username].getemotion = "Energetic"  
                    scope_user[username].moodlabel = "You are better than ever!"
        except Exception:
            pass
        
def automodemusic(emotion, username):
    pop = random.randint(0, 100)
    musicurl = getmusic(scope_user[username].autoartistlist, emotion, scope_user[username].autogenres, scope_user[username].automarket, pop, type=0)
    if musicurl == {}:
        #if cant find any songs that match music taste
        musicurl = getmusic(scope_user[username].autoartistlist, emotion, scope_user[username].autogenres, scope_user[username].automarket, pop, type=1)
    if musicurl == {}:
        #if cant find any songs that match music taste and market
        musicurl = getmusic(scope_user[username].autoartistlist, emotion, scope_user[username].autogenres, scope_user[username].automarket, pop, type=2)
    scope_user[username].trackurl = random.choice(list(musicurl))
    scope_user[username].duration = musicurl[scope_user[username].trackurl][0]
    scope_user[username].artist = musicurl[scope_user[username].trackurl][1]
    scope_user[username].trackname = musicurl[scope_user[username].trackurl][2]
    # print(musicurl)
    # print(trackurl, duration) 
    
# Video function
# import threading

#Initial declaration
(lBegin, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eyebrow"]
(rBegin, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eyebrow"]
# getting lip points from facial landmarks
(l_lower, l_upper) = face_utils.FACIAL_LANDMARKS_IDXS["mouth"]
(i_lower, i_upper) = face_utils.FACIAL_LANDMARKS_IDXS["inner_mouth"]
(el_lower, el_upper) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(er_lower, er_upper) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]  

class VideoStreamConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        global username
        # self.prev = 0
        # self.new = 0
        self.username = username
        self.mood = 'Analyzing...'
        await self.accept()

    async def disconnect(self, close_code):
        # self.prev = 0
        # self.new = 0
        # print(f"WebSocket closed with code {close_code}.")
        scope_user[self.username].clearall()
        scope_user[self.username].cleardata()
        scope_user[self.username].music()
        self.stop = True
        raise StopConsumer()
    
    async def draw_border(self, img, pt1, pt2, color, thickness, r, d):
        x1,y1 = pt1
        x2,y2 = pt2

        # Top left
        cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

        # Top right
        cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

        # Bottom left
        cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

        # Bottom right
        cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
    
    async def receive(self, bytes_data):
        if not (bytes_data):
            await self.close()
        else:
            self.frame = cv2.imdecode(np.frombuffer(bytes_data, dtype=np.uint8), cv2.IMREAD_COLOR)
            #frame = imutils.resize(frame, width=400,height=400)
            #preprocessing the image
            self.gray = cv2.cvtColor(self.frame,cv2.COLOR_BGR2GRAY)
            self.detections = detector(self.gray,0)
            if (self.detections):             
                self.detection = self.detections[0]
                self.x, self.y, self.w, self.h = self.detection.left(), self.detection.top(), self.detection.width(), self.detection.height()  
                self.dst = 6421 / self.w
                self.dst = '%.2f' %self.dst                 
                await self.draw_border(self.frame, (self.x, self.y), (self.x + self.w, self.y + self.h), (255, 217, 102),2, 10, 3)
                self.emotion = get_emotion(self.detection, self.gray)
                self.shape = predictor(self.frame, self.detection)
                self.shape = face_utils.shape_to_np(self.shape)
                self.leyebrow = self.shape[lBegin:lEnd]
                self.reyebrow = self.shape[rBegin:rEnd]
                self.openmouth = self.shape[l_lower:l_upper]
                self.innermouth = self.shape[i_lower:i_upper]
                self.lefteye = self.shape[el_lower:el_upper]
                self.righteye = self.shape[er_lower:er_upper]
                self.reyebrowhull = cv2.convexHull(self.reyebrow)
                self.leyebrowhull = cv2.convexHull(self.leyebrow)
                self.openmouthhull = cv2.convexHull(self.openmouth)
                self.innermouthhull = cv2.convexHull(self.innermouth)
                self.leyehull = cv2.convexHull(self.lefteye)
                self.reyehull = cv2.convexHull(self.righteye)
                lipdist_async = sync_to_async(lpdist)
                self.lipdist = await lipdist_async(self.openmouthhull[-1][0], self.openmouthhull[0][0], self.username)
                ebdist_async = sync_to_async(ebdist)
                self.eyedist = await ebdist_async(self.leyebrow[-1], self.reyebrow[0], self.username)
                leyedist_async = sync_to_async(leyedist)
                self.ledist = await leyedist_async(self.leyehull[-1][0], self.leyehull[0][0], self.username)
                reyedist_async = sync_to_async(reyedist)
                self.redist = await reyedist_async(self.reyehull[-1][0], self.reyehull[0][0], self.username)
                normalize_values_async = sync_to_async(normalize_values)
                self.stress_value = await normalize_values_async(scope_user[self.username].points, self.eyedist, scope_user[self.username].points_lip, self.lipdist, scope_user[self.username].points_leye, self.ledist, scope_user[self.username].points_reye, self.redist, self.emotion, self.username)

                if self.username != 0:
                    self.stress_range = scope_user[self.username].stress_range
                    self.mean_value = get_mean_value(self.stress_range, self.username)
                    self.std_value = get_std_value(self.stress_range, self.username)
                    self.f = open(DIR+'/server/static/server/data/{}_0.csv'.format(self.username), 'a', newline='')
                    if scope_user[self.username].mode == 0:
                        # Quickscan Mode
                        self.row = {"Frame": len(scope_user[self.username].points), "Value":self.stress_range[-1], "Mean":self.mean_value, "Standard Deviation": self.std_value}
                        # with open(DIR+'/server/static/server/data/{}_0.csv'.format(username), 'w', newline='') as f:
                        #     writer = csv.writer(f)
                        #     writer.writerow(["Frame", "Value", "Mean", "Standard Deviation", "Top Spread", "Bottom Spread"])
                        #     writer.writerows(zip(range(len(points)), self.stress_range, self.mean_value, self.std_value, self.top_range, self.bottom_range))
                    
                    else:
                        # Monitor Mode
                        if (len(scope_user[self.username].points) > 150) and (scope_user[self.username].status == True):
                            scope_user[self.username].status = False
                            self.mood = scope_user[self.username].getemotion
                            # automode(self.mean_value, self.std_value, self.stress_range, self.username)
                            reset(self.username)
                        self.row = {"Frame":len(scope_user[self.username].points), "Value":self.stress_range[-1]}
                    self.writer = csv.DictWriter(self.f, fieldnames=self.row.keys())
                    self.writer.writerow(self.row)

                cv2.drawContours(self.frame, [self.reyebrowhull, self.leyebrowhull, self.openmouthhull, self.innermouthhull, self.leyehull, self.reyehull], -1, (219, 255, 99), 1)
                # draw_dots(self.frame, self.leyebrow, self.reyebrow, self.openmouth, self.lefteye, self.righteye)
                # cv2.putText(self.frame, "FPS: {}".format((self.fps)), (235,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (54, 161, 255), 1)
                cv2.putText(self.frame, "Distance: {} cm".format((self.dst)), (10,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (54, 161, 255), 1)
                cv2.putText(self.frame, "Current Mood: {}".format((self.mood)), (10,20),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (54, 161, 255), 1)
                # cv2.putText(frame, "Stress Detected?: {}".format((stress_detector)), (10,40),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (239, 112, 4), 2)
                # cv2.putText(frame,"Stress Index: {}".format(str(int(stress_value*100))),(10,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (239, 112, 4), 2)
                
                cv2.putText(self.frame,"Stress Index: {}/100".format(str(int(self.stress_value*100))),(10,60),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (239, 112, 4), 1)
                # cv2.putText(self.frame,"Stress Index: {}/100".format(str(len(scope_user[self.username].points))),(10,80),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (239, 112, 4), 1)
                # cv2.putText(self.frame,"Stress Index: {}/100".format(str(self.username)),(10,100),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (239, 112, 4), 1)
                
            self.buffer_img = cv2.imencode('.jpeg', self.frame)[1]
            self.b64_img = base64.b64encode(self.buffer_img).decode('utf-8')
            # b64_img = buffer_img.tobytes()
            # Send the base64 encoded image back to the client
            asyncio.sleep(200/1000)
            await self.send(self.b64_img)
            # await asyncio.sleep(0)