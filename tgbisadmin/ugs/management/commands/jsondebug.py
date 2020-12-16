# import json
# print('{'leads[il]':'324235235'}'.replace(''', '''))
# data = json.loads('{'leads[il]':'324235235'}'.replace(''', '''))
# print(data['leads[il]'])






import time

from facebook_business.adobjects.serverside.event import Event
from facebook_business.adobjects.serverside.event_request import EventRequest
from facebook_business.adobjects.serverside.user_data import UserData
from facebook_business.adobjects.serverside.custom_data import CustomData
from facebook_business.api import FacebookAdsApi

access_token = '<ACCESS_TOKEN>'
pixel_id = 'ADS_PIXEL_ID>'

FacebookAdsApi.init(access_token=access_token)

user_data = UserData(
    email='joe@eg.com',
    fbc='fb.1.1554763741205.AbCdEfGhIjKlMnOpQrStUvWxYz1234567890',
    fbp='fb.1.1558571054389.1098115397'
)

custom_data = CustomData(
    currency='usd',
    value=123.45
)

event = Event(
    event_name='Purchase',
    event_time=int(time.time()),
    user_data=user_data,
    custom_data=custom_data,
)

events = [event]

event_request = EventRequest(
    events=events,
    pixel_id=pixel_id)

event_response = event_request.execute()
print(event_response)








# {'id': 3273697, 'name': 'Вебинар', 'sort': 2, 'is_main': False, 'is_unsorted_on': True, 'is_archive': False, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697'}}, '_embedded': {'statuses': [{'id': 33058309, 'name': 'Неразобранное', 'sort': 10, 'is_editable': False, 'pipeline_id': 3273697, 'color': '#c1c1c1', 'type': 1, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/33058309'}}}, {'id': 33058312, 'name': 'Заявки на вебинар', 'sort': 20, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#deff81', 'type': 0, 'account_id': 23681254,'_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/33058312'}}}, {'id': 33098776, 'name': 'Квалификация', 'sort': 30, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#ff8f92', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/33098776'}}}, {'id': 34354525, 'name': 'Недозвон', 'sort': 40, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#99ccff', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/34354525'}}}, {'id': 33058315, 'name': 'День вебинара', 'sort': 50, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#ffff99', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/33058315'}}}, {'id': 34354528, 'name': 'Пришел на вебинар', 'sort': 60, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#99ccff', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/34354528'}}}, {'id': 35108005, 'name': 'Интерес', 'sort': 70, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#87f2c0', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/35108005'}}}, {'id': 34354531, 'name': 'Не пришел на вебинар', 'sort': 80, 'is_editable': True, 'pipeline_id': 3273697, 'color': '#ff8f92', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/34354531'}}}, {'id': 142, 'name': 'Успешно реализовано', 'sort': 10000, 'is_editable': False, 'pipeline_id': 3273697, 'color': '#CCFF66', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/142'}}}, {'id': 143, 'name': 'Закрыто и не реализовано', 'sort': 11000, 'is_editable': False, 'pipeline_id': 3273697, 'color': '#D5D8DB', 'type': 0, 'account_id': 23681254, '_links': {'self': {'href': 'https://impactcapital.amocrm.ru/api/v4/leads/pipelines/3273697/statuses/143'}}}]}}
# from tgbisadmin import amoCRM_update_lib
# p = [
#     {
#         "name": "Сделка для примера 1",
#         "created_by": 0,
#         "price": 20000,
#         "custom_fields_values": [
#             {
#                 "field_id": 294471,
#                 "values": [
#                     {
#                         "value": "Наш первый клиент"
#                     }
#                 ]
#             }
#         ]
#     },
#     {
#         "name": "Сделка для примера 2",
#         "price": 10000,
#         "_embedded": {
#             "tags": [
#                 {
#                     "id": 2719
#                 }
#             ]
#         }
#     }
# ]
# print(p)
#
# amoCRM_update_lib.link(25804001,81290535)
import string
import random
# def random_char(y):
#     return ''.join(random.choice(string.ascii_letters) for x in range(y))
#
#
# print(random_char(10))
#
# p = {'dgs': 32}
# print(p['dg'])

    # elif profile.numquestion >= 0:
    #
    #     profile.numquestion += 1
    #     profile.save()
    #     # context.bot.send_message(chat_id=chat_id,
    #     #                              text='Хорошо, сохранили ваш ответ',
    #     #                              )
    #     questions(update=update, context=context)
    #     # print(textAnswer1)
    #     # context.bot.send_message(chat_id = chat_id,
    #     #                          text= f'"{text}" - является ответом на {profile.numquestion} вопрос?',
    #     #                          reply_markup=get_base_check_save_keyboard())




# @log_errors
# def do_photo(update: Update, context: CallbackContext):
#
#         chat_id = update.message.chat_id
#         profile = Profile.objects.get(external_id=chat_id)
#         if profile.typeOfQuestion != 'Опрос':
#             return do_start(update=update, context=context)
#         else:
#             photoFile = context.bot.get_file(update.message.photo[-1].file_id)
#             path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#             path = os.path.join(path, 'photos',
#                                 f'profile_{chat_id}_answer_{profile.numquestion}_{profile.numOfFiles}.jpg')
#
#             # photoFile = context.bot.get_file(update.message.photo[0].file_id)
#             # path = f'./photos/profile_{chat_id}_answer_{profile.numquestion}_{profile.numOfFiles}.jpg'
#             context.bot.send_message(chat_id = chat_id,
#                                      text = 'Сохраняем ваше фото...',
#                                      reply_markup=get_base_check_keyboard(),)
#
#             print(photoFile)
#             print(path)
#             print(photoFile.download(path))
#             print(profile.numOfFiles)
#             photoFile.download(path)
#             profile.numOfFiles += 1
#             profile.save()
#
#             Answer.objects.create(respondentId=profile.external_id,
#                                   numAnswer=Question.objects.get(generalNumQuestion = profile.numquestion).textQuestion,
#                                   textAnswer=path,
#                                   ).save() PHOTO

# @log_errors
# def do_document(update: Update, context: CallbackContext):
#     chat_id = update.message.chat_id
#     profile = Profile.objects.get(external_id=chat_id)
#     if profile.typeOfQuestion != 'Опрос':
#         return do_start(update=update, context=context)
#     else:
#         docFile = context.bot.get_file(update.message.document.file_id)
#         path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
#         path = os.path.join(path, 'documents',
#         f'profile_{chat_id}_answer_{profile.numquestion}_{profile.numOfFiles}_{update.message.document.file_name}')
#
#         context.bot.send_message(chat_id=chat_id,
#                                  text='Сохраняем ваш документ...',
#                                  reply_markup=get_base_check_keyboard(), )
#         print(docFile)
#         print(path)
#         print(1)
#         print(docFile.download(path))
#         print(1)
#         print(profile.numOfFiles)
#         docFile.download(path)
#         profile.numOfFiles += 1
#         profile.save()
#
#         Answer.objects.create(respondentId=profile.external_id,
#                               numAnswer=Question.objects.get(generalNumQuestion = profile.numquestion).textQuestion,
#                               textAnswer=path,
#                               ).save() DOCUMENT
