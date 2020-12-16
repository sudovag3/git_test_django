from django.contrib import admin

from .forms import ProfileForm

from .models import Profile, Parameters
from .models import WebinarsDjango
from .models import Registers
from .models import Videos

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('name', 'external_id', 'user_tg_parameteres_id', 'webinarIDRegister', 'userQuestion', 'userStatus', 'profileNum')
    form = ProfileForm




@admin.register(Parameters)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('telegramIdLink', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'roistat_visit')

@admin.register(Videos)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('videoTitle', 'videoUrl', 'videoDescription', 'videoAdminDescription', 'videoID')

@admin.register(WebinarsDjango)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('webinarTitle', 'webinarDescription', 'webinarDescription2', 'webinarDescription3', 'webinarID', 'webinarDateTime')

@admin.register(Registers)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('userID', 'userWebinar', 'userName', 'userMail', 'userNum')

