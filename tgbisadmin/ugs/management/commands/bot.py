from django.core.management.base import BaseCommand
from django.conf import settings
from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater
from telegram.update import Update
from telegram.ext.callbackcontext import CallbackContext
from telegram.bot import Bot
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.utils.request import Request
from ugs.models import Profile
from ugs.models import WebinarsDjango
from ugs.models import Registers
from ugs.models import Videos
import logging
import threading
from django.utils import timezone
import time
import configNames
from ugs.func import handler
from datetime import datetime, timedelta
from ugs.func import keyboards
# from apiclient.bizon365 import Webinars
import os
logger = logging.getLogger(__name__)
def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Произошла ошибка: {e}'
            print(error_message)
            logger.error(f'{e}')

            raise e
    return inner


@log_errors
def do_contact(update: Update, context: CallbackContext):
    profile = Profile.objects.get(external_id = update.message.chat_id)
    profile.profileNum = update.message.contact.phone_number
    profile.save()
    logger.info(update.message.contact.phone_number)
    do_start(update=update, context=context)


@log_errors
def WebinarCheck(update, context):
    threading.Timer(60.0, WebinarCheck, args=[update, context]).start()
    # print(1)
    timeNow = timezone.now()

    statusProfile = False
    # обращение к бизону

    for register in Registers.objects.all().filter():
        if register.userStatus == 'Не пришел на вебинар':

            context.bot.send_message(
                chat_id=register.userID,
                text='Привет! Жаль, что у Вас не получилось послушать наш вебинар.'


            )
            time.sleep(3)
            context.bot.send_message(
                chat_id=register.userID,
                text=
                     '\n\nНичего страшного. Вы сможете посмотреть запись по ссылке:'


            )
            time.sleep(2)
            context.bot.send_message(
                chat_id=register.userID,
                text=
                     f'\n{WebinarsDjango.objects.get(webinarID=register.userWebinar).webinarVideoUrl}'

            )
            register.userStatus = 'Нет'
            register.delete()

        elif register.userStatus == 'Пришел на вебинар':
            context.bot.send_message(
                chat_id=register.userID,
                text=f'Спасибо, что посетили наш вебинар!'

            )
            time.sleep(2)
            context.bot.send_message(
                chat_id=register.userID,
                text=f'Искренне надеемся, что информация была для вас полезной.'

            )
            time.sleep(3)
            context.bot.send_message(
                chat_id=register.userID,
                text=f'Мы обещали вам подарок «Регламент по оценке компаний», отправляю.'

            )

            path = os.path.dirname(__file__)
            path = os.path.join(path, 'Регламент оценки.pdf')
            f = open(path, 'rb')
            context.bot.send_document(
                chat_id=register.userID,
                document=f
            )

            register.userStatus = 'Нет'
            register.delete()

        elif register.userStatus == 'Интерес':
            context.bot.send_message(
                chat_id=register.userID,
                text=f'❤Что именно вам интересно?❤',
                reply_markup=keyboards.get_base_intresting_keyboard(),

            )
            register.userStatus = 'опрос'
            register.userReason = 'Отвечает'
            register.save()
            pass

    for webinar in WebinarsDjango.objects.all().filter():
        timeToGo = (divmod((webinar.webinarDateTime - timeNow).days * 86400 + (webinar.webinarDateTime - timeNow).seconds, 60))[0]
        print(timeToGo)
        if timeToGo == 30:
            logger.info(f'30 минут до начала вебинара{webinar.webinarID}')
            try:
                for person in Registers.objects.all().filter(userWebinar = webinar.webinarID):
                    context.bot.send_message(
                            chat_id=person.userID,
                            text=f'Добрый вечер! Напоминаю, что вы записывались на вебинар «{webinar.webinarTitle}».'

                        )
                    time.sleep(3)
                    context.bot.send_message(
                        chat_id=person.userID,
                        text=f'Он пройдёт сегодня в {webinar.webinarDateTime.time()}'

                    )
                    time.sleep(2)
                    context.bot.send_message(
                        chat_id=person.userID,
                        text=f'Вот ссылка:'

                    )
                    time.sleep(2)
                    context.bot.send_message(
                        chat_id=person.userID,
                        text=f'{webinar.webinarUrl}'

                    )
            except Registers.DoesNotExist:
                logger.info('Не найдено ни одного зрителя...')
        # elif timeToGo == 15:
        #     logger.info(f'15 минут до начала вебинара{webinar.webinarID}')
        #     # print(1)
        #     try:
        #         for person in Registers.objects.all().filter(userWebinar = webinar.webinarID):
        #             context.bot.send_message(
        #                     chat_id=person.userID,
        #                     text=f'{person.userName}.\nДо начала вебинара 💥{webinar.webinarTitle}💥 остается 15 минут, ловите ссылку!\n\n👉🏻👉🏻{webinar.webinarUrl}👈🏻👈🏻\n\nПриятного просмотра!'
        #
        #                 )
        #     except Registers.DoesNotExist:
        #         logger.info('Не найдено ни одного зрителя...')
        elif timeToGo == 0:
            pass
        elif timeToGo == -120:
            pass
    pass


@log_errors
def sendVideo(update: Update, context: CallbackContext, videoTitle):
    chat_id = update.message.chat_id
    video = Videos.objects.get(videoTitle = videoTitle)
    context.bot.send_message(
                chat_id     = chat_id,
                text        = f'❕ ``{video.videoTitle}``'
                              f'❕ ``\n{video.videoDescription}``'
                              f'\n{video.videoUrl}',
        parse_mode          = 'Markdown',
            )

@log_errors
def Register(update: Update, context: CallbackContext):

    chat_id      = update.message.chat_id
    profile      = Profile.objects.get(external_id=chat_id)
    Registers.objects.get_or_create(userID = chat_id, userWebinar = profile.webinarIDRegister)
    registerUser = Registers.objects.get(userID = chat_id, userWebinar = profile.webinarIDRegister)
    if update.message.text != 'Да, хочу зарегистрироваться':

            registerUser.userName = profile.name
            registerUser.userNum = profile.profileNum
            registerUser.userMail = update.message.text
            registerUser.save()
            profile.userQuestion = 0
            profile.webinarIDRegister = 0
            profile.save()

            context.bot.send_message(
                chat_id     = update.effective_chat.id,
                text        = 'Благодарю.'
                )
            time.sleep(0.5)
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='️⭐️⭐️Вы успешно зарегистрировались на вебинар!️⭐️⭐️',
            )
            time.sleep(2)

            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Вы слышали о компании IMPACT Capital?',
                reply_markup=keyboards.get_base_check_impact_info_keyboard(),
            )

            # context.bot.send_message(
            #     chat_id=update.effective_chat.id,
            #     text='А пока вы его ждёте, уточните, какой вопрос вам наиболее интересен:',
            #     reply_markup=keyboards.get_base_waiting_videos_keyboard(),
            # )

            # sendVideo(videoTitle = 'Видео1', update=update, context=context)
            logger.info(f'Зарегистрирован пользователь {chat_id} на вебинар {registerUser.userWebinar}')

    else:

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Укажите вашу почту куда отправить ссылку:',
        )


@log_errors
def do_start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    name = update.message.from_user.username
    if update.message.text != None and '/start ' in update.message.text:
        try:
            profile = Profile.objects.get(external_id=chat_id)

        except Profile.DoesNotExist:
            tg_unicode = update.message.text.replace('/start ', '')
            p, _ = Profile.objects.get_or_create(
                external_id=chat_id,
                user_tg_parameteres_id = tg_unicode

            )
    profile = Profile.objects.get(external_id=chat_id)
    profile.webinarIDRegister = 0
    profile.userQuestion = 0
    profile.save()

    if profile.profileNum == '0':
        context.bot.send_message(chat_id=chat_id,
                                 text=
                                      f'Привет, я чат-бот IMPACT-Bot!',
                                 )

        context.bot.send_message(chat_id=chat_id,
                                 text=
                                 f'Для регистрации на вебинар, оставьте Ваши контактные данные.',
                                 reply_markup=keyboards.get_contact_keyboard())
    elif profile.name == 'Нет':
        context.bot.send_message(chat_id=chat_id,
                                 text=
                                 f'Хорошо. Как вас зовут?',
                                 )

    else:
        context.bot.send_message(chat_id=chat_id,
                                 text=
                                 f'Мы очень рады, что ты к нам заглянул!'
                                 f'\nВпереди у нас много интересных вебинаров, выбирай!',
                                 reply_markup=keyboards.get_base_menu_keyboard())

    # bot.send_message(chat_id=chat_id,
    #                  text="Привет, откуда ты пришёл?",
    #                  C=get_base_inline_keyboard(),
    #                  )

@log_errors
def questions(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=' Для начала, нажмите "Начать".',
        reply_markup=keyboards.get_base_reply_keyboard(),
    )
    # print(profile.numquestion)
    # print(Question.objects.count())


@log_errors
def do_check(update: Update, context: CallbackContext):

    chat_id = update.message.chat_id
    text    = update.message.text

    # p, _ =Profile.objects.get_or_create(
    #     external_id = chat_id,
    #     defaults= {'name': update.message.from_user.username,
    #                }
    # )
    try:
        profile = Profile.objects.get(external_id = chat_id)

    except Profile.DoesNotExist:
        do_start(update=update, context=context)

    if profile.profileNum == 0:
        do_start(update=update, context=context)
    elif text == 'AdmStart2034':
        logger.info('Запуск основного тела программы')
        WebinarCheck(update=update, context=context)
    elif profile.name == 'Нет':
        profile.name = text
        profile.save()
        return do_start(update=update, context=context)
    elif text == 'AdminImpact20204040':
        profile.userStatus = 'Админ'
        profile.save()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Вы администратор, поздравляю!', )
        logger.info(f'Добавлен админ {profile.external_id}')
    elif text == 'testAdm20':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='❤Что именно вам интересно?❤',
            reply_markup=keyboards.get_base_intresting_keyboard(),
        )

    elif text == configNames.CHOOSE_WEBINAR:
        return handler.send_keyborad_webinar(update=update, context=context)
    elif text == configNames.YES_I_WANT_REGISTER:
        return Register(update=update, context=context)
    elif text == configNames.NO_SEE_MORE:
        profile.webinarIDRegister = 0
        profile.save()
        return handler.send_keyborad_webinar(update=update, context=context)

    elif text == configNames.REASON_NO_INTERESTING:
        return handler.save_reason(update=update, context=context, reason = text)
    elif text == 'Поменялись планы':
        return handler.save_reason(update=update, context=context, reason=text)
    elif text == 'Не разобрался, как посмотреть вебинар':
        return handler.save_reason(update=update, context=context, reason=text)
    elif text == 'Да, расскажите':
        return handler.get_info_webinar(update=update, context=context)
    elif text == 'Нет. Примерно представляю':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Отлично\n\n🚨`Желаете Зарегистрироваться?`🚨',
            reply_markup=keyboards.get_base_reply_keyboard(),
            parse_mode="Markdown")
    elif text == 'Да, слышал':
        reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()

        reg.user_know_impact = text
        reg.save()

        profile.userStatus = 'Расскажите, откуда узнали о нас?'
        profile.save()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'Расскажите, откуда узнали о нас?',
            )
        pass
    elif text == 'Нет, не слышал':
        return handler.get_info_impact(update=update, context=context)
        pass
    elif text == 'Да☑':
        reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()

        reg.user_know_investion = 'Да, знает'
        reg.save()
        return handler.get_check_investion_currently(update=update, context=context)
        pass
    elif text == 'Нет✖':
        reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()

        reg.user_know_investion = 'Нет, не знает'
        reg.save()
        return handler.get_save_investion(update=update, context=context)

    elif text == 'IT':
        reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()

        reg.user_who_know_investion_currently = text
        reg.save()
        return handler.get_save_investion(update=update, context=context)
        pass
    elif text == 'Недвижимость':
        reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()

        reg.user_who_know_investion_currently = text
        reg.save()
        return handler.get_save_investion(update=update, context=context)
        pass
    elif text == 'Retail':
        reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()

        reg.user_who_know_investion_currently = text
        reg.save()
        return handler.get_save_investion(update=update, context=context)
        pass

    else:
        if profile.userStatus == 'Расскажите, откуда узнали о нас?':
            reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()
            reg.user_who_know_impact = text
            profile.userStatus = 'Нет'
            reg.save()
            profile.save()
            context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Cпасибо, ответ принят',
            )
            return handler.get_check_investion(update=update, context=context)
        reg = Registers.objects.filter(userID = update.effective_chat.id, userStatus = 'опрос').first()

        if reg == None:
            if profile.webinarIDRegister != 0:
                return Register(update=update, context=context)
            else:
                return do_start(update=update, context=context)
        else:
            if reg.userReason == 'Отвечает':
                return handler.save_reason(update=update, context=context, reason = text)

            else:
                if profile.webinarIDRegister != 0:
                    return Register(update=update, context=context)
                else:
                    return do_start(update=update, context=context)


@log_errors
def keyboard_callback_handler(update: Update, context: CallbackContext):
    query                     = update.callback_query
    data                      = query.data
    # print(data)
    try:

        if 'o' in data:
            if data == 'Actions':
                return handler.save_interesting(update=update, context=context, interes = 'Акции IMPACT Capital')
            elif data == 'Invension':
                return handler.save_interesting(update=update, context=context, interes='Инвестиции в портфельные компании')
            elif data == 'Portfel':
                return handler.save_interesting(update=update, context=context, interes='Аудит инвестиционного портфеля')

        else:
            return handler.get_webinar(update=update, context=context, data=data)
    except WebinarsDjango.DoesNotExist:

        videoSelected = Videos.objects.get(videoID=data)
        context.bot.send_message(

            chat_id=update.effective_chat.id,
            text=

            # f'`Видео:` {videoSelected.videoTitle}'
            # f'\n\n❗`Описание:` {videoSelected.videoDescription}'
            f'{videoSelected.videoUrl}',
        )


# WebinarCheck(update=Update, context=CallbackContext)
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
        contact_handler = MessageHandler(Filters.contact, do_contact)
        message_handler = MessageHandler(Filters.text, do_check)
        buttons_handler = CallbackQueryHandler(callback=keyboard_callback_handler, pass_chat_data=True)
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(buttons_handler)
        updater.dispatcher.add_handler(contact_handler)

        updater.start_polling()
        updater.idle()
