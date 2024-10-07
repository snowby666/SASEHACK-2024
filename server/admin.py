from django.contrib import admin
from datetime import datetime
from server.models import *
from django.db.models import F, Count
from . import models
from import_export.admin import ImportExportMixin
from django.utils import timezone

class UserPlugin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user', 'date_of_birth', 'gender')
    
class UserUrlPlugin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user','timestamp','url')
    list_filter = ('user', 'timestamp', )
    
class TokenPlugin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('lang','b_token','lat_token','chat_code','status')
    
class FeedbackPlugin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user','timestamp')
    
class UserMusicPlugin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('user','market','genre','singer')
    
admin.site.register(UserProfileInfo, UserPlugin)
admin.site.register(UserUrl, UserUrlPlugin)
admin.site.register(UserMusic, UserMusicPlugin)
admin.site.register(Feedback, FeedbackPlugin)
admin.site.register(Token, TokenPlugin)

admin.site.site_header = 'coDestress Admin'