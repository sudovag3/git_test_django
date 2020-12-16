from django.db import models
from django.db.models.signals import m2m_changed
from django.db.models.signals import post_save

class Videos(models.Model):
    videoTitle              = models.TextField(verbose_name='Название видео')
    videoUrl                = models.TextField(verbose_name='Ссылка на видео')
    videoDescription        = models.TextField(verbose_name='Описание видео')
    videoAdminDescription   = models.TextField(verbose_name='Системное описание видео')
    videoID                 = models.PositiveIntegerField(verbose_name='ID видео', default=0)

    def __str__(self):
        return f'#{self.videoTitle} {self.videoUrl} {self.videoDescription} {self.videoAdminDescription} {self.videoID}'

    class Meta:
        verbose_name        = 'Видео'
        verbose_name_plural = 'Видео'

class Profile(models.Model):
    external_id          = models.PositiveIntegerField(verbose_name='Id пользователя в соц сети', unique=True)
    name                 = models.TextField(verbose_name='Имя пользователя', default='Нет')
    webinarIDRegister    = models.PositiveIntegerField(verbose_name='Id выбранного вебинара', default=0)
    userQuestion         = models.PositiveIntegerField(verbose_name='Номер вопроса', default=0, blank=True)
    userStatus           = models.TextField(verbose_name='Статус пользователя', default='Посетитель')
    profileNum           = models.TextField(verbose_name='Телефон поьзователя', default=0)
    user_tg_parameteres_id = models.TextField(verbose_name='ID для Tg', blank=True)

    def __str__(self):
        return f'#{self.external_id} {self.name} {self.webinarIDRegister} {self.userQuestion} {self.userStatus} {self.profileNum} {self.user_tg_parameteres_id}'

    class Meta:
        verbose_name        = 'Профиль'
        verbose_name_plural = 'Профили'


class WebinarsDjango(models.Model):
    webinarTitle            = models.TextField(verbose_name='Название вебинара')
    webinarDescription      = models.TextField(verbose_name='Описание Вебинара', default=0)
    webinarDescription2      = models.TextField(verbose_name='Описание Вебинара2', default=0)
    webinarDescription3     = models.TextField(verbose_name='Описание Вебинара3', default=0)
    webinarID               = models.PositiveIntegerField(verbose_name='Идентификатор Вебинара')
    webinarDateTime         = models.DateTimeField(verbose_name='Дата и время вебинара')
    webinarUrl              = models.TextField(verbose_name='Ссылка на вебинар', default=0)
    webinarVideoUrl         = models.TextField(verbose_name='Ссылка на запись', default=0)


    def __str__(self):
        return f'#{self.webinarTitle} {self.webinarVideoUrl} {self.webinarDescription} {self.webinarDescription2} {self.webinarDescription3} {self.webinarID} {self.webinarDateTime}'

    class Meta:
        verbose_name        = 'Вебинар'
        verbose_name_plural = 'Вебинары'


class Parameters(models.Model):
    telegramIdLink = models.TextField(verbose_name='id для телеграмма')
    utm_source = models.TextField(verbose_name='utm_source', blank=True)
    utm_medium = models.TextField(verbose_name='utm_medium', blank=True)
    utm_campaign = models.TextField(verbose_name='utm_campaign', blank=True)
    utm_content = models.TextField(verbose_name='utm_content', blank=True)
    utm_term = models.TextField(verbose_name='utm_term', blank=True)
    roistat_visit = models.TextField(verbose_name='roistat_visit', blank=True)

    def __str__(self):
        return f'#{self.telegramIdLink} {self.utm_source} {self.utm_medium} {self.utm_campaign} {self.utm_content} {self.utm_term} {self.roistat_visit}'

    class Meta:
        verbose_name        = 'Параметр'
        verbose_name_plural = 'Параметры'


class Registers(models.Model):
    userID          = models.PositiveIntegerField(verbose_name='ID')
    userStatus      = models.TextField(verbose_name='Статус', default='Нет')
    userWebinar     = models.TextField(verbose_name='ID Вебинара')
    userName        = models.TextField(verbose_name='Имя пользователя')
    userMail        = models.TextField(verbose_name='Почта пользователя')
    userNum         = models.TextField(verbose_name='Телефон пользователя')
    numOfNotWebinar = models.IntegerField(verbose_name='Счетчик', default=0)
    userReason      = models.TextField(verbose_name='Причина', default='Нет')
    user_know_impact = models.TextField(verbose_name='Знает ли о компании?', default='Не определено')
    user_who_know_impact = models.TextField(verbose_name='Откуда знает', default='Не определено')
    user_know_investion = models.TextField(verbose_name='Знает ли о инвестициях?', default='Не определено')
    user_who_know_investion_currently = models.TextField(verbose_name='О каких именно', default='Нет')

    # typeOfAnswer = models.TextField(verbose_name='Тип ответа')

    def __str__(self):
        return f'#{self.userID} {self.userWebinar} {self.userName} {self.userMail} {self.userNum} {self.userReason} {self.user_know_impact} {self.user_who_know_impact} {self.user_know_investion} {self.user_who_know_investion_currently}'

    class Meta:
        verbose_name        = 'Регистрация'
        verbose_name_plural = 'Регистрации'

