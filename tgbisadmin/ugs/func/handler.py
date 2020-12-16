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
from ugs.models import Parameters
import logging
import threading
from django.utils import timezone
import time
import configNames
from ugs.func import keyboards
from amoCRM_update_lib import create_deal
from amoCRM_update_lib import link
from datetime import datetime, timedelta


def send_keyborad_webinar(update: Update, context: CallbackContext):
    listWithKeyboards    = []
    timeNow              = timezone.now()

    for i in WebinarsDjango.objects.all():
        timeToGo = (
            divmod((i.webinarDateTime - timeNow).days * 86400 + (i.webinarDateTime - timeNow).seconds,
                   60))[0]
        if timeToGo > 0:
            listWithKeyboards.append([InlineKeyboardButton(i.webinarTitle, callback_data=i.webinarID)])
    keyboard = InlineKeyboardMarkup(listWithKeyboards)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='*Вот какие вебинары мы можем вам предложить⬇⬇⬇*',
        reply_markup=keyboard,
        parse_mode="Markdown",
    )

def save_reason(update: Update, context: CallbackContext, reason):
    reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='опрос').first()
    reg.userStatus = 'Не пришёл, причину определил'
    reg.userReason = reason
    reg.save()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Спасибо за обратную связь, будем рады вашему участию на других наших вебинарах',
        reply_markup=keyboards.get_base_menu_keyboard(),
    )

def save_interesting(update: Update, context: CallbackContext, interes):
    regist = Registers.objects.get(userID=update.effective_chat.id, userStatus='опрос')
    regist.userReason = interes
    context.bot.send_message(

        chat_id=update.effective_chat.id,
        text='Cпасибо, скоро с вами свяжутся, будем рады видеть вас на наших вебинарах',
        reply_markup=keyboards.get_base_menu_keyboard()
    )

def get_check_investion_currently(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Уточните, пожалуйста, какой сектор для вас предпочтительнее:',
        reply_markup=keyboards.get_base_investion_impact_info_currently_keyboard())

def get_check_investion(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Уточните, пожалуйста, есть ли у вас опыт прямых инвестиций?',
        reply_markup=keyboards.get_base_investion_impact_info_keyboard())

def get_save_investion(update: Update, context: CallbackContext):
    context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f'Спасибо за ответы, будем рады видеть вас на нашем вебинаре!',

            )
    reg = Registers.objects.filter(userID=update.effective_chat.id, userStatus='Нет').first()
    profile = Profile.objects.get(external_id=update.effective_chat.id)
    par = Parameters.objects.get(telegramIdLink = profile.user_tg_parameteres_id)

    prInfo =[{

        "custom_fields_values": [
            {
                "field_id": 133839,
                "values": [
                    {
                        "value": reg.userNum
                    }
                ]
            },
            {
                "field_id": 133841,
                "values": [
                    {
                        "value": reg.userMail
                    }
                ]
            },
            {
                "field_id": 685213,
                "values": [
                    {
                        "value": reg.userName
                    }
                ]
            },
            {
                "field_id": 667977,
                "values": [
                    {
                        "value": reg.user_know_investion
                    }
                ]
            },

            {
                "field_id": 685751,
                "values": [
                    {
                        "value": reg.user_know_impact
                    }
                ]
            },
            {
                "field_id": 685753,
                "values": [
                    {
                        "value": reg.user_who_know_impact
                    }
                ]
            }
        ]
    }]

    if reg.user_know_investion != 'Нет, не знает':
        prInfo[0]["custom_fields_values"].append({
                "field_id": 675851,
                "values": [
                    {
                        "value": reg.user_who_know_investion_currently
                    }
                ]
            })

    regInfo =[{

        "pipeline_id": 3273697,
        "name": "Заявка на вебинар",
        "custom_fields_values": [
        {
            "field_id": 675711,
            "values": [
                {
                    "value": par.utm_source
                }
            ]
        },
        {
            "field_id": 676523,
            "values": [
                {
                    "value": par.utm_medium
                }
            ]
        },
        {
            "field_id": 676525,
            "values": [
                {
                    "value": par.utm_campaign
                }
            ]
        },
        {
            "field_id": 676527,
            "values": [
                {
                    "value": par.utm_term
                }
            ]
        },
        {
            "field_id": 676529,
            "values": [
                {
                    "value": par.utm_content
                }
            ]
        },
        {
            "field_id": 676297,
            "values": [
                {
                    "value": par.roistat_visit
                }
            ]
        },]

    }]
    logging.info(link(create_deal(regInfo, 'leads')["_embedded"]["leads"][0]["id"], create_deal(prInfo, 'contacts')["_embedded"]["contacts"][0]["id"]))
    # logging.info(create_deal(regInfo, 'leads'))
    # logging.info(create_deal(prInfo, 'contacts'))
    time.sleep(2)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'А пока вы его ждёте, уточните, какой вопрос вам наиболее интересен:',
        reply_markup=keyboards.get_base_waiting_videos_keyboard()
    )


def get_info_impact(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Компания IMPACT Capital')
    time.sleep(2)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Расскажу в нескольких предложениях… ',)
    time.sleep(2)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Мы специализируется на покупке долей в перспективных компаниях на Раунде-А')
    time.sleep(3.5)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Когда проект прошёл точку безубыточности, но не стал еще прибыльным')
    time.sleep(3)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Это позволяет приобретать доли по наилучшей оценке')
    time.sleep(2.5)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'И в дальнейшем приумножать вложенные средства нам и нашим партнёрам')
    time.sleep(3)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'У нас в портфеле такие компании как:')
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'⚽Футбольная Академия Егора Титова')
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'🍕Dodo Pizza')
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'🦾Technored')
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'🍬YogurtShop')
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'🏵VananaPark')
    time.sleep(1)
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            f'Но и на фондовом рынке у нас есть чем гордиться 😊')
    time.sleep(2)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Например, в период пандемии мы сделали 105% годовых')
    time.sleep(2)
    return get_check_investion(update=update, context=context)




def get_info_webinar(update: Update, context: CallbackContext):
    chat_id = update.effective_message.chat_id
    profile = Profile.objects.get(external_id=chat_id)
    webinarSelected = WebinarsDjango.objects.get(webinarID=profile.webinarIDRegister)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'Отлично',
        parse_mode="Markdown")
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'❗`На этом вебинаре вы узнаете:`',
        parse_mode="Markdown")
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'✅{webinarSelected.webinarDescription}', )
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'✅{webinarSelected.webinarDescription2}', )
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=
        f'✅{webinarSelected.webinarDescription3}', )
    time.sleep(1)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f'\n\n🚨`Желаете Зарегистрироваться?`🚨',
        reply_markup=keyboards.get_base_reply_keyboard(),
        parse_mode="Markdown")

def get_webinar(update: Update, context: CallbackContext, data):
    webinarSelected = WebinarsDjango.objects.get(webinarID=data)
    chat_id = update.effective_message.chat_id
    profile = Profile.objects.get(external_id=chat_id)
    profile.webinarIDRegister = data
    profile.save()


    if profile.userStatus != 'Админ':
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f'💻 Выбранный `Вебинар:` {webinarSelected.webinarTitle}',
            parse_mode="Markdown")
        time.sleep(0.3)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
            f'Вебинар пройдёт {webinarSelected.webinarDateTime.day} {configNames.MONTH_LIST[webinarSelected.webinarDateTime.month + 1]}'
            f'\nСовет: Добавьте себе напоминание в календарь, чтобы не забыть.',
            parse_mode="Markdown")
        time.sleep(1)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=
                 'Рассказать, что будет на вебинаре?',
            reply_markup=keyboards.get_base_check_webinar_keyboard())

        # context.bot.send_message(
        #
        #     chat_id=update.effective_chat.id,
        #     text=f'💻`Вебинар:` {webinarSelected.webinarTitle}'
        #          f'\n\n❗`Описание:` {webinarSelected.webinarDescription}'
        #          f'\n\n🕑`Дата`: {webinarSelected.webinarDateTime.date()}'
        #          f'\n🕑`Время`: {webinarSelected.webinarDateTime.time()}'
        #          f'\n\n🚨`Желаете Зарегистрироваться?`🚨',
        #     reply_markup=get_base_reply_keyboard(),
        #     parse_mode="Markdown")
    else:
        context.bot.send_message(

            chat_id=update.effective_chat.id,
            text=f'💻`Вебинар:` {webinarSelected.webinarTitle}'
                 f'\n\n❗`Описание:` {webinarSelected.webinarDescription}'
                 f'\n\n🕑`Дата`: {webinarSelected.webinarDateTime.date()}'
                 f'\n🕑`Время`: {webinarSelected.webinarDateTime.time()}'
                 f'\n\n🚨`Желаете Зарегистрироваться?`🚨',
            parse_mode="Markdown")
    # print(data)

