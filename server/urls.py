from django.urls import include
from django.urls import path, re_path
from . import views
app_name = 'server'
urlpatterns = [
    path('', views.index, name='index.html'),
    path('log_out/', views.log_out, name='log_out'),
    path('speech/', views.speech, name = "speech"),
    path('chatbot/', views.chatbot, name="chatbot"),
    path('analysis/', views.analysis, name = "analysis"),
    path('sitemap.xml', views.sitemap, name = "sitemap.xml"),
    path('manifest.json', views.manifest, name='manifest.json'),
]