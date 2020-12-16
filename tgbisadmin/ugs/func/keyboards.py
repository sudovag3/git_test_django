from telegram import KeyboardButton
from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from ugs.models import Videos
import configNames


def get_base_check_reason_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.REASON_NO_INTERESTING),
        ],
        [
            KeyboardButton(configNames.REASON_CHANGE_PLAN),
        ],
        [
            KeyboardButton(configNames.REASON_DONT_UNDERSTAND),
        ],
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)




def get_base_investion_impact_info_currently_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_IMPACT_INVESTION_NED),
            KeyboardButton(configNames.BUTTON_IMPACT_INVESTION_IT),
            KeyboardButton(configNames.BUTTON_IMPACT_INVESTION_RETAIL),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)



def get_base_investion_impact_info_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_YES_CHECK_IMPACT_INVESTION),
            KeyboardButton(configNames.BUTTON_NO_CHECK_IMPACT_INVESTION),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

def get_base_check_impact_info_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_YES_CHECK_IMPACT_INFO),
            KeyboardButton(configNames.BUTTON_NO_CHECK_IMPACT_INFO),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)



def get_base_check_webinar_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_YES_CHECK_WEBINAR),
            KeyboardButton(configNames.BUTTON_NO_CHECK_WEBINAR),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_base_check_number_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_YES_NUMBER),
            KeyboardButton(configNames.BUTTON_NO_NUMBER),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_base_waiting_videos_keyboard():
    keyboard =[]
    for i in Videos.objects.filter(videoAdminDescription = 'Процесс ожидания').values():
        keyboard.append([InlineKeyboardButton(i['videoTitle'], callback_data=i['videoID'])])

    return InlineKeyboardMarkup(keyboard)


def get_base_intresting_keyboard():
    keyboard =[
        [InlineKeyboardButton('Акции IMPACT Capital', callback_data='Actions')],
        [InlineKeyboardButton('Инвестиции в портфельные компании', callback_data='Invension')],
        [InlineKeyboardButton('Аудит инвестиционного портфеля', callback_data='Portfel')],
    ]

    return InlineKeyboardMarkup(keyboard)


def get_contact_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_SEND_CONTACT, request_contact=True),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_base_check_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.BUTTON_YES_SEND),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def get_base_menu_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.CHOOSE_WEBINAR),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_base_reply_keyboard():
    keyboard = [
        [
            KeyboardButton(configNames.YES_I_WANT_REGISTER),
            KeyboardButton(configNames.NO_SEE_MORE),
        ]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

