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



BUTTON1_VEBINAR = 'С вебинара'
BUTTON2_SITE = 'С сайта'
BUTTON3_YES = 'Все отправил'

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
            KeyboardButton(BUTTON1_VEBINAR),
            KeyboardButton(BUTTON2_SITE)
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



@log_errors
def do_site(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Хорошо, надеюсь тебе понравился наш сайт)'
    )

@log_errors
def do_vebinar(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Хорошо, надеюсь тебе понравился наш вебинар)'
    )


@log_errors
def do_start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id = update.effective_chat.id,
        text = 'Привет, Откуда ты пришёл?',
        reply_markup= get_base_reply_keyboard(),
    )
    # bot.send_message(chat_id=chat_id,
    #                  text="Привет, откуда ты пришёл?",
    #                  reply_markup=get_base_inline_keyboard(),
    #                  )

@log_errors
def questions(update: Update, context: CallbackContext):
    profile = Profile.objects.get(external_id = update.message.chat_id)
    if profile.numquestion == Question.objects.count():
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Поздравляем, вы полностью заполнили форму! \nВ данный момент она находится на рассмотрении. \nСчетчик ваших вопросов обнулён, и вы можете заполнить новую форму!!!')
        profile.numquestion = 0
        profile.save()
        do_start(update=update, context=context)
    else:
        numQuestionProfile = profile.numquestion

        context.bot.send_message(
            chat_id=profile.external_id,
            text= f'Пожалуйста, ответь на следующий вопрос, желательно следуя требованиям типа ответа:'
                  f'\n{(numQuestionProfile) + 1}) {Question.objects.get(generalNumQuestion = numQuestionProfile).textQuestion}'
                  f'\nТип ответа: {Question.objects.get(generalNumQuestion = numQuestionProfile).typeOfAnswer}',
            reply_markup=ReplyKeyboardRemove(get_base_reply_keyboard()),
        )

    print(profile.numquestion)
    print(Question.objects.count())


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

    if text == 'С вебинара':
        profile.typeOfQuestion = 'Вебинар'
        profile.save()
        return questions(update=update, context=context)
    elif text == 'С сайта':
        profile.typeOfQuestion = 'Сайт'
        profile.save()
        return questions(update=update, context=context)
    elif text == 'Все отправил':
        profile.numquestion += 1
        profile.save()
        context.bot.send_message(chat_id=chat_id,
                                 text = 'Хорошо, сохранил ваш ответ',
                                 reply_markup=ReplyKeyboardRemove(get_base_check_keyboard()))
        return questions(update=update, context=context)

    elif profile.typeOfQuestion == 'Не выбрал':
        return do_start(update=update, context=context)

    elif profile.numquestion >= 0:
        Answer.objects.create(respondentId=profile.external_id,
                                  numAnswer=profile.numquestion,
                                  textAnswer=text,
                                  typeOfAnswer=Question.objects.get(generalNumQuestion=profile.numquestion).typeOfAnswer
                                  ).save()
        profile.numquestion += 1
        profile.save()
        context.bot.send_message(chat_id=chat_id,
                                     text='Хорошо, сохранили ваш ответ',
                                     )
        questions(update=update, context=context)
        # print(textAnswer1)
        # context.bot.send_message(chat_id = chat_id,
        #                          text= f'"{text}" - является ответом на {profile.numquestion} вопрос?',
        #                          reply_markup=get_base_check_save_keyboard())



def do_photo(update: Update, context: CallbackContext):
        chat_id = update.message.chat_id
        profile = Profile.objects.get(external_id=chat_id)
        photoFile = context.bot.get_file(update.message.photo[0].file_id)
        path = f'./photos/profile_{chat_id}_answer_{profile.numquestion}_{profile.numOfFiles}.jpg'
        context.bot.send_message(chat_id = chat_id,
                                 text = 'Сохраняем ваше фото...',
                                 reply_markup=get_base_check_keyboard(),)
        photoFile.download(path)
        profile.numOfFiles += 1
        profile.save()

        Answer.objects.create(respondentId=profile.external_id,
                              numAnswer=profile.numquestion,
                              textAnswer=path,
                              typeOfAnswer=Question.objects.get(generalNumQuestion=profile.numquestion).typeOfAnswer
                              ).save()


def do_document(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    profile = Profile.objects.get(external_id=chat_id)
    docFile = context.bot.get_file(update.message.document.file_id)
    path = f'./documents/profile_{chat_id}_answer_{profile.numquestion}_{profile.numOfFiles}_{update.message.document.file_name}'
    context.bot.send_message(chat_id=chat_id,
                             text='Сохраняем ваш документ...',
                             reply_markup=get_base_check_keyboard(), )
    docFile.download(path)
    profile.numOfFiles += 1
    profile.save()

    Answer.objects.create(respondentId=profile.external_id,
                          numAnswer=profile.numquestion-1,
                          textAnswer=path,
                          typeOfAnswer=Question.objects.get(generalNumQuestion=profile.numquestion).typeOfAnswer
                          ).save()




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
        photo_handler = MessageHandler(Filters.photo, do_photo)
        document_handler = MessageHandler(Filters.document, do_document)
        updater.dispatcher.add_handler(start_handler)
        updater.dispatcher.add_handler(message_handler)
        updater.dispatcher.add_handler(photo_handler)
        updater.dispatcher.add_handler(document_handler)

        updater.start_polling()
        updater.idle()