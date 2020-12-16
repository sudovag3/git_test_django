from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import Bot
from telegram import Update
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram.ext import CallbackContext
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram import ReplyKeyboardRemove
from telegram.utils.request import Request
from ugs.models import Profile
from ugs.models import Message
from ugs.models import Question
from ugs.models import Answer

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
import requests
import json
import os


BUTTON1_START = 'Начать'
# BUTTON2_SITE = 'С сайта'
BUTTON3_YES = 'Все отправил'
BUTTON3_YES_NUMBER = 'Всё верно'
BUTTON3_NO_NUMBER = 'Нет, сейчас исправлю'
#

def get_base_check_number_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON3_YES_NUMBER),
            KeyboardButton(BUTTON3_NO_NUMBER),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_base_check_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON3_YES),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(BUTTON1_START),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            # print(error_message)
            raise e
    return inner



# @log_errors
# def do_site(update: Update, context: CallbackContext):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='Хорошо, надеюсь тебе понравился наш сайт)'
#     )
#
# @log_errors
# def do_vebinar(update: Update, context: CallbackContext):
#     context.bot.send_message(
#         chat_id=update.effective_chat.id,
#         text='Хорошо, надеюсь тебе понравился наш вебинар)'
#     )


@log_errors
def do_start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    p, _ = Profile.objects.get_or_create(
        external_id=chat_id,
        defaults={'name': update.message.from_user.username,
                  }
    )



    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = ' Для начала, нажмите "Начать".',
        reply_markup= get_base_reply_keyboard(),
    )
    # bot.send_message(chat_id=chat_id,
    #                  text="Привет, откуда ты пришёл?",
    #                  C=get_base_inline_keyboard(),
    #                  )

@log_errors
def questions(update: Update, context: CallbackContext):
    profile = Profile.objects.get(external_id = update.message.chat_id)
    if profile.numquestion == Question.objects.count():
        # url = 'https://webhook.site/8b0ee74f-d5b7-40aa-8bc1-3fa3b71f0beb'
        url = 'https://dev.salesevolution.ru/pub/integrator/3/form-getter.php/impactcapital/telegram_bot'
        headers = {'Content-type': 'application/json',  # Определение типа данных
                   'Accept': 'text/plain',
                   'Content-Encoding': 'utf-8'}
        data = serialize('json', Answer.objects.all().filter(respondentId=profile.external_id),
                         cls=DjangoJSONEncoder)
        maindata = {}
        data = json.loads(data)
        for i in data:
            maindata[i['fields']['numAnswer']] = i['fields']['textAnswer'];
        strMainData = str(maindata)
        strMainData = strMainData.replace("'", '"')
        answer = requests.post(url, data=strMainData.encode('utf-8'), headers=headers)
        print(answer)
        print(strMainData)
        print(1)


        answers = Answer.objects.all().filter(respondentId=profile.external_id)
        answers.delete()


        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Поздравляем, вы полностью заполнили форму! \nВ данный момент она находится на рассмотрении. \nСчетчик ваших вопросов обнулён, и вы можете заполнить новую форму!!!\nДля этого нажмите /start')
        profile.numquestion = 0
        profile.save()
        # do_start(update=update, context=context)
    else:
        numQuestionProfile = profile.numquestion

        context.bot.send_message(
            chat_id=profile.external_id,
            text=
                  f'{Question.objects.get(generalNumQuestion = numQuestionProfile).textQuestion}'
                 ,
            reply_markup=ReplyKeyboardRemove(get_base_reply_keyboard()),
        )

    # print(profile.numquestion)
    # print(Question.objects.count())


@log_errors
def do_check(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id
    text = update.message.text

    p, _ =Profile.objects.get_or_create(
        external_id = chat_id,
        defaults= {'name': update.message.from_user.username,
                   }
    )

    Message(profile=p,
            text=text).save()
    profile = Profile.objects.get(external_id = chat_id)

    # if text == 'С вебинара':
    #     profile.typeOfQuestion = 'Вебинар'
    #     profile.save()
    #     return questions(update=update, context=context)
    # elif text == 'С сайта':
    #     profile.typeOfQuestion = 'Сайт'
    #     profile.save()
    #     return questions(update=update, context=context)

    if text == 'Все отправил':
        profile.numquestion += 1
        profile.save()
        context.bot.send_message(chat_id=chat_id,
                                 text = 'Хорошо, сохранил ваш ответ',
                                 reply_markup=ReplyKeyboardRemove(get_base_check_keyboard()))
        return questions(update=update, context=context)

    elif text == 'Начать':
         context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Ответьте на вопросы. Время заполнения в среднем занимает 40 минут. \nКоличество: 56 вопросов. \nЕсли на вопрос вы затрудняетесь ответить, или ответа нет, то просто пишите "нет".\nВам понадобиться загружать фото и видео файлы, будьте к этому готовы. Также, имейте при себе бумагу и карандаш/ручку',
         )
         answers = Answer.objects.all().filter(respondentId=profile.external_id)
         answers.delete()
         profile.typeOfQuestion = 'Опрос'
         profile.save()
         profile.numquestion = 0
         profile.save()
         return questions(update=update, context=context)

    elif profile.typeOfQuestion != 'Опрос':
        return do_start(update=update, context=context)

    elif profile.numquestion == 6:
        if text == 'Нет, сейчас исправлю':
            # print(1)
            # print(Answer.objects.get(respondentId=profile.external_id,
            #                    numAnswer=Question.objects.get(generalNumQuestion=6).textQuestion))
            answers = Answer.objects.all().filter(respondentId=profile.external_id, numAnswer=Question.objects.get(generalNumQuestion=6).textQuestion)
            answers.delete()
            context.bot.send_message(chat_id=chat_id,
                                     text='Пожалуйста введите исправленный номер',
                                     reply_markup=ReplyKeyboardRemove(get_base_check_number_keyboard()))

        elif text == 'Всё верно':
            context.bot.send_message(chat_id=chat_id,
                                     text='Хоршо, номер сохранён',
                                     reply_markup=ReplyKeyboardRemove(get_base_check_number_keyboard()))

            profile.numquestion += 1
            profile.save()
            questions(update=update, context=context)
        else:
            Answer.objects.create(respondentId=profile.external_id,
                                  numAnswer=Question.objects.get(generalNumQuestion=6).textQuestion,
                                  textAnswer=text,
                                  ).save()
            context.bot.send_message(chat_id=chat_id,
                                     text=f'Проверьте правильность написания номера: {text}',
                                     reply_markup=get_base_check_number_keyboard())

    elif profile.numquestion >= 0:
        Answer.objects.create(respondentId=profile.external_id,
                                  numAnswer=Question.objects.get(generalNumQuestion = profile.numquestion).textQuestion,
                                  textAnswer=text,
                                  ).save()
        profile.numquestion += 1
        profile.save()
        # context.bot.send_message(chat_id=chat_id,
        #                              text='Хорошо, сохранили ваш ответ',
        #                              )
        questions(update=update, context=context)
        # print(textAnswer1)
        # context.bot.send_message(chat_id = chat_id,
        #                          text= f'"{text}" - является ответом на {profile.numquestion} вопрос?',
        #                          reply_markup=get_base_check_save_keyboard())




class Command(BaseCommand):
    help = 'Телеграм - бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=0.5,
            read_timeout=1.0,
        )
        bot = Bot(request=request,
                  token=settings.TOKEN)
        print(bot.get_me())

        updater = Updater(bot = bot,
                          use_context=True)
        start_handler = CommandHandler('start', do_start)
        message_handler = MessageHandler(Filters.text, do_check)
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(message_handler)
        updater.start_polling()
        updater.idle()
