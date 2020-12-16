#!/usr/bin/python3.7
import requests
import json
import pygsheets
import pandas as pd
import os
from pprint import pprint
# путь к сервисному аккаунту google
script_directory = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(script_directory, 'amowebhook-68139bc2be47.json')
# путь к файлу с настройками
AmoCRM_settings = 'https://docs.google.com/spreadsheets/d/12R1TPoXmAeGnR1azyWiG_jgpOG7tXibnGCDXXpqwpT4/edit?usp=sharing'

import logging

logging.basicConfig(filename='null', format='%(asctime)s;%(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# create a file handler
handler = logging.FileHandler('webhook.log')
handler.setLevel(logging.INFO)

# create a logging format
title = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(title)

# add the handlers to the logger
logger.addHandler(handler)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# класс для работы с http запросами
class Http_Query:
    def __init__(self,type_request,url,headers={},data={},params={}):
        self.type_request = type_request
        self.url = url
        self.headers = headers
        self.data = data
        self.params = params
        self.result=''
        self.data_result=None
    def send_request(self):
        self.result=''
        try:
            if self.type_request=='GET':
                req = requests.get(self.url, params=self.params, headers=self.headers)
            if self.type_request=='POST':
                req = requests.post(self.url, json=self.data, headers=self.headers)
            if self.type_request=='PATCH':
                req = requests.patch(self.url,data=self.data,headers=self.headers)

        except requests.exceptions.RequestException as e:
            self.result = e.response.status_code
            return self.result
        except requests.HTTPError as e:
            self.result = e.response.status_code
            return self.result
        if req.status_code in [200, 203]:
            self.data_result = json.loads(req.content.decode("utf-8"))
            self.result='SUCCESS'
            return self.result
        else:
            logger.info(req.content)
            return req.status_code

# класс для работы с гугл-таблицей

class AmoCRM:
    def __init__(self,access_token,url):
        self.access_token=access_token
        self.url=url
        self.events_filter=0
        self.events_columns =[]
        pass
    # получение одной страницы данных
    def get_one_page(self,type_req='leads',num_page=1,limit=250, _with=''):
        if type_req == 'leads':
            payload = {'page': num_page, 'limit': limit, 'with': _with}
        elif type_req == 'events':
            payload = {'page': num_page, 'limit': limit, 'with': _with,'filter[type]': ['incoming_call','outgoing_call'],} #,'filter[created_at]':1600560000
            if self.events_filter:
                payload['filter[created_at]']=self.events_filter
        elif type_req == 'users':
            payload = {'page': num_page, 'limit': limit, 'with': _with} #,'filter[created_at]':1596240000
        elif type_req == 'contacts':
            payload = {'page': num_page, 'limit': limit, 'with': _with} #,'filter[created_at]':1596240000
        elif type_req =='leads/notes':
            payload = {'page': num_page, 'limit': limit, 'with': _with,} #,'filter[created_at]':1600560000
            if self.events_filter:
                payload['filter[updated_at]']=self.events_filter

        else:
            payload = {'page': num_page, 'limit': limit, 'with': _with} #,'filter[created_at]':1596240000

        headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {self.access_token}'}
        full_url = f"https://{self.url}/api/v4/{type_req}"
        req= Http_Query("GET",full_url,headers,params=payload)
        if req.send_request()=='SUCCESS':
            return req.data_result
        else:
            return False

    # получение всех страниц данных
    def get_all_page(self,type_req='leads', limit=250, _with=''):
        result_dataframe=pd.DataFrame()
        num_page: int = 1
        leads = self.get_one_page(type_req, num_page, limit, _with)
        print(type(leads))
        while type(leads) is dict:
            name_table=type_req.split('/')[-1]
            df_leads = pd.json_normalize(leads['_embedded'][name_table])
            result_dataframe = pd.concat([result_dataframe, df_leads], ignore_index=True, verify_integrity=True)
            logger.info(f'Recieved {name_table}: {len(df_leads)}')
            num_page += 1
            if len(df_leads) < limit: break

            # print(df_leads)
            leads = self.get_one_page(type_req, num_page, limit, _with)
        else:
            logger.info(f'Stop:{leads}')
        return result_dataframe
# класс экспорта из Амо в таблицу

class GSheets:

    def __init__(self,service_file,filename='',file_url=''):
        if service_file:
            gc = pygsheets.authorize(service_file=service_file)
        else:
            gc = pygsheets.authorize()
        if filename!='':
            sh = gc.open(filename)
        elif file_url!='':
            sh = gc.open_by_url(file_url)
        else:
            logger.info('name and url is empty')
            return False

        self.service_file = service_file
        self.filename = filename
        self.gc = gc
        self.sh = sh
        pass
    # сохранение данных в таблицу
    def set_df_to_sheets(self, sheetname, df):
        wks = self.sh.worksheet_by_title(sheetname)
        wks.clear()
        wks.set_dataframe(df, (1, 1),fit=True,nan='')
        logger.info(f'Save: {sheetname}')
        return df
    # получение данных и таблицы
    def get_df_to_sheets(self, sheetname):
        wks = self.sh.worksheet_by_title(sheetname)

        df= wks.get_as_df()
        logger.info(f'Load: {sheetname}')
        return df
    # добавление данных в таблицу
    def add_df_to_sheets(self, sheetname, df):
        wks = self.sh.worksheet_by_title(sheetname)
        #wks.clear()
        wks.insert_rows(1, number=len(df), values=None, inherit=False)
        wks.set_dataframe(df, (2, 1),nan='',copy_head=False)
        logger.info(f'Add: {sheetname}')
        return df

    def get_fields(self):

        df = self.get_df_to_sheets('fields')
        df = df.set_index('Вопрос из Квиза', drop=False)
        df = df[df.index.notnull()]
        logger.info('load fields')

        return df


    def get_setting(self):

        wks = self.sh.worksheet_by_title('settings')
        df = wks.get_as_df()
        df['expired'] = pd.to_datetime(df['expired'])
        #print (df['expired'])
        #df.to_json('settings.json', force_ascii=False,date_unit='ns')
        #df=pd.read_json('settings.json')
        #df['expired'] = pd.to_datetime(df['expired'])
        #print(df['expired'])
        df.set_index('URL', inplace=True, drop=False)

        logger.info('load settings')

        return df



    def set_settings(self,df):

        wks = self.sh.worksheet_by_title('settings')
        wks.set_dataframe(df, (1,1))
        logger.info('save settings')

        return df



def first_start(client_id, client_secret, code, redirect_uri,url,filename):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri
    }
    headers = {'Content-Type': 'application/json'}
    test = requests.post(f"https://{url}/oauth2/access_token", data=data)
    print(test.content)
    if test.status_code in [200,201]:
        d = json.loads(test.content.decode("utf-8"))
        with open(filename, 'w') as outfile:
            json.dump(d, outfile,ensure_ascii=False)
        return d

# функция обновления токена.
def refresh_expired_token(client_id, client_secret, refresh_token, url, redirect_uri):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "redirect_uri": redirect_uri
    }
    headers = {'Content-Type': 'application/json'}
    try:
        # без headers!!!!
        req = requests.post(f"https://{url}/oauth2/access_token", data=data)
    except requests.exceptions.RequestException as e:
        return e
    except requests.HTTPError as e:
        print(e.response.status_code)
        return e.response.status_code
        #if e.response.status_code == 404:
        #    return None

    print(req.status_code)
    print(req.content)
    if req.status_code in [200,203]:
        req_result = json.loads(req.content.decode("utf-8"))
        with open(f'{client_id}.refresh', 'a') as outfile:
            outfile.write("\n")
            json.dump(req_result, outfile)
        return req_result
    else:
        return req.status_code


class AmoCRM_authorize:
    def __init__(self,filename):
        script_directory = os.path.dirname(os.path.abspath(__file__))
        full_filename = os.path.join(script_directory, filename)

        self.data = json.load(open(full_filename))
        pass
    def get_data(self):
        pass
    def save_data(self):
        pass

class AmoCRM_item:
    def __init__(self,access_token,url):
        self.url=url
        self.access_token=access_token
        pass
    def get_item_by_id(self,type_req,id):
        headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {self.access_token}'}
        full_url = f"https://{self.url}/api/v4/{type_req}/{id}?with=contacts"
        req= Http_Query("GET",full_url,headers)
        # print(req.send_request())
        if req.send_request()=='SUCCESS':
            return req.data_result
        else:
            return False

    def get_lead_by_id(self,id):
        return self.get_item_by_id('leads',id)
        pass
    def update_item_by_id(self,type_req,id,data):
        headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {self.access_token}'}
        full_url = f"https://{self.url}/api/v4/{type_req}/{id}"
        logger.info(full_url)
        req= Http_Query("PATCH",full_url,headers=headers,data=data)
        if req.send_request()=='SUCCESS':
            return req.data_result
        else:
            logger.info(req.data_result)
            return False

        pass
    def create_lead(self,data, param):
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.access_token}'}
        full_url = f"https://{self.url}/api/v4/{param}"
        logger.info(full_url)
        req = Http_Query("POST", full_url, headers=headers, data=data)
        print(1)
        if req.send_request() == 'SUCCESS':
            return req.data_result
        else:
            logger.info(req.data)
            return False
        pass

    def link_lead(self,id_deal, id_contact):
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.access_token}'}
        full_url = f"https://{self.url}/api/v4/leads/{id_deal}/link"
        logger.info(full_url)
        data = [
            {
                "to_entity_id": id_contact,
                "to_entity_type": "contacts",
                "metadata": {
                    "is_main": True,
                }
            }
        ]
        req = Http_Query("POST", full_url, headers=headers, data=data)
        print(1)
        if req.send_request() == 'SUCCESS':
            return req.data_result
        else:
            logger.info(req.data)
            return False
        pass

    def create_contact(self,data):
        headers = {'Content-Type': 'application/json',
                   'Authorization': f'Bearer {self.access_token}'}
        full_url = f"https://{self.url}/api/v4/contacts"
        logger.info(full_url)
        req = Http_Query("POST", full_url, headers=headers, data=data)
        print(1)
        if req.send_request() == 'SUCCESS':
            return req.data_result
        else:
            logger.info(req.data)
            return False
        pass


def extract_answer(tjson,landing_url):

    if 'leads[note][0][note][text]' in tjson:
        ans_list = tjson['leads[note][0][note][text]'].split('\n')
        if landing_url in ans_list[-1]:
            #print(ans_list[-1])
            #print(len(ans_list))
            ans_count = (len(ans_list) - 2) // 3
            #print(ans_count)
            recieved_df = pd.DataFrame(columns=['answer_value'])
            for i in range(ans_count):
                recieved_df.loc[ans_list[3 * i].rstrip()] = [ans_list[3 * i + 1].rstrip()]
            lead_id = tjson['leads[note][0][note][element_id]']
            return {'lead':lead_id,'data':recieved_df}

    return False

def extract_answer_from_export_note(ans_text,landing_url):
    if type(ans_text) is str:
        ans_list = ans_text.split('\n')
        if landing_url in ans_list[-1]:
            ans_text = ans_text.split('\n\n\n')[0]
            ans_text = ans_text.split('\nРезультат: ')[0]
            ans_list = ans_text.split('\n')
            ans_count = (len(ans_list) + 1) // 3
            recieved_df = pd.DataFrame(columns=['answer_value'])
            for i in range(ans_count):
                recieved_df.loc[ans_list[3 * i].rstrip()] = [ans_list[3 * i + 1].rstrip()]
            return [recieved_df]

    return False


def webhook(request_data):
    logger.info('start')
    gsheet=GSheets(json_file,file_url=AmoCRM_settings)
    df = gsheet.get_setting()
    field_df = gsheet.get_fields()
    #print(field_df)
    #print(type(field_df['id'].iloc[0]))
    for index, row in df.iterrows():
        logger.info(f"token expired{ row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired']-pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient=AmoCRM_item(df.loc[index, 'access_token'],index)
        # element_id


        quiz_rezult=extract_answer(request_data,row['landing_url'])
        if quiz_rezult:
            #print(quiz_rezult)
            #result=amoclient.get_lead_by_id(quiz_rezult['lead'])
            #print(result)
            #result=amoclient.get_item_by_id('leads/notes','213286369')
            #print(result)
            df1 = quiz_rezult['data'].join(field_df, how='inner')
            field_json=[]
            for index,jrow in df1.iterrows():
                if jrow['id']>0:
                    field_json.append({ "field_id": jrow['id'],"values": [{"value": jrow['answer_value']}]})
            field_json=json.dumps({"custom_fields_values": field_json})
            result=amoclient.update_item_by_id('leads',quiz_rezult['lead'],field_json)
            logger.info(result)
    logger.info('end')
    return 'webhook recieved'

def webhookWebinar(request_data):
    logger.info('start')
    gsheet=GSheets(json_file,file_url=AmoCRM_settings)
    df = gsheet.get_setting()

    for index, row in df.iterrows():
        logger.info(f"token expired{ row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired']-pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient=AmoCRM_item(df.loc[index, 'access_token'],index)
        lead = amoclient.get_item_by_id('leads', request_data['leads[status][0][id]'][0])
        contact = amoclient.get_item_by_id('contacts', lead['_embedded']['contacts'][0]['id'])
        voron = amoclient.get_item_by_id(f'leads/pipelines/{lead["pipeline_id"]}/statuses', lead["status_id"])
        logger.info(voron)

    logger.info('end')
    return [voron['name'], contact['custom_fields_values'][0]['values'][0]['value']]


def create_deal(data, param):
    logger.info('start')
    gsheet = GSheets(json_file, file_url=AmoCRM_settings)
    df = gsheet.get_setting()

    for index, row in df.iterrows():
        logger.info(f"token expired{row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired'] - pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient = AmoCRM_item(df.loc[index, 'access_token'], index)
        voron = amoclient.create_lead(data=data, param=param)
        logger.info(voron)

    logger.info('end')
    return voron

def link(id_deal, id_contact):
    logger.info('start')
    gsheet = GSheets(json_file, file_url=AmoCRM_settings)
    df = gsheet.get_setting()

    for index, row in df.iterrows():
        logger.info(f"token expired{row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired'] - pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient = AmoCRM_item(df.loc[index, 'access_token'], index)
        voron = amoclient.link_lead(id_deal=id_deal, id_contact=id_contact)
        logger.info(voron)

    logger.info('end')
    return voron


def create_contact_true(data):
    logger.info('start')
    gsheet = GSheets(json_file, file_url=AmoCRM_settings)
    df = gsheet.get_setting()

    for index, row in df.iterrows():
        logger.info(f"token expired{row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired'] - pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient = AmoCRM_item(df.loc[index, 'access_token'], index)
        voron = amoclient.create_lead(data=data)
        logger.info(voron)

    logger.info('end')
    return voron

def test_long_task():
     test = {"leads[note][0][note][element_type]": "2", "leads[note][0][note][element_id]": "22060555", "leads[note][0][note][note_type]": "4", "leads[note][0][note][text]": 'Количество этажей будет в вашем будущем доме?\nДва\n\nУкажите предпочтительную площадь будущего дома в м²\n149\n\nКогда вы планируете начать строительство?\nв течение 1-3 месяцев\n\nГде находится ваш земельный участок?\nот 20км до 50км от МКАД\n\nКакой способ связи для вас удобнее?\nTelegram\n\nРезультат: https://bot.flatoutlet.ru/telegram/pmFo\n\nUTM-метки:\ncampaign: look-a-like_ new quiz\ncontent: 23846024248070263\nmedium: domagency\nsource: ig\ncampaign: look-a-like_ new quiz\n\nСтраница: https://mrqz.me/5f2ac962b03fc800440a755c?utm_source=ig&amp;utm_medium=domagency&amp;utm_campaign=look-a-like_+new+quiz&amp;utm_content=23846024248070263&amp;fbclid=PAAaZZApzkvvtxUtbH7jBHWX0DYpkIsVfigWIxl2NqmbuzBrpxkZVUdMmix4g', "leads[note][0][note][account_id]": "15109720", "leads[note][0][note][date_create]": "2020-09-28 00:26:51", "leads[note][0][note][timestamp_x]": "2020-09-28 00:26:51", "leads[note][0][note][created_by]": "1608151", "leads[note][0][note][modified_by]": "1608151", "leads[note][0][note][main_user_id]": "1608151", "leads[note][0][note][group_id]": "258124", "leads[note][0][note][id]": "213313359", "leads[note][0][note][created_at]": "1601242011", "leads[note][0][note][updated_at]": "1601242011", "account[subdomain]": "makeprofit", "account[id]": "15109720", "account[_links][self]": "https://makeprofit.amocrm.ru"}
     webhook(test)

def send_request(data):
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    test = requests.post(f"http://makeprofitteam.pythonanywhere.com/amo_webhook_long/", data=data, headers=headers)

def update_notes_day(day_count:str):
    logger.info('get notes from amo')
    gsheet=GSheets(json_file,file_url=AmoCRM_settings)
    df = gsheet.get_setting()
    field_df = gsheet.get_fields()

    for index, row in df.iterrows():
        logger.info(f"token expired{ row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired']-pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient=AmoCRM(df.loc[index, 'access_token'],index)
        amoclient_item=AmoCRM_item(df.loc[index, 'access_token'],index)

        amoclient.events_filter=(pd.Timestamp.now()-pd.Timestamp("1970-01-01")-pd.Timedelta(day_count)) // pd.Timedelta('1s')
        print(amoclient.events_filter)
        df=amoclient.get_all_page('leads/notes')

        df['updated_at']=pd.to_datetime(df['updated_at'], unit='s')
        df['created_at'] = pd.to_datetime(df['created_at'], unit='s')
        df.to_csv('notes.csv',encoding='UTF-8')

        for index,row in df.iterrows():
            pprint(row['params.text'])
            quiz_rezult = extract_answer_from_export_note(row['params.text'],'Страница: http')
            if quiz_rezult:
                df1 = quiz_rezult[0].join(field_df, how='inner')
                field_json=[]
                for index,jrow in df1.iterrows():
                    if jrow['id']>0:
                        field_json.append({ "field_id": jrow['id'],"values": [{"value": jrow['answer_value']}]})
                field_json=json.dumps({"custom_fields_values": field_json})
                result = amoclient_item.update_item_by_id('leads', row['entity_id'], field_json)
                print('leads',row['entity_id'],field_json)
                print(result)
            pass




def update_custom_fields():
    logger.info('update_custom fields')
    gsheet=GSheets(json_file,file_url=AmoCRM_settings)
    df = gsheet.get_setting()
    field_df = gsheet.get_fields()
    for index, row in df.iterrows():
        logger.info(f"token expired{ row['expired']}")
        # проверка на еxpires и обновление токена
        if row['expired']-pd.Timedelta(seconds=3600) < pd.Timestamp.now():
            req_result = refresh_expired_token(row['client_id'], row['client_secret'], f"{row['refresh_token']}", index,
                                               row['redirect_uri'])
            if type(req_result) is dict:
                df.loc[index, 'refresh_token'] = req_result['refresh_token']
                df.loc[index, 'access_token'] = req_result['access_token']
                df.loc[index, 'expired'] = pd.Timestamp.now() + pd.Timedelta(seconds=req_result['expires_in'])
                gsheet.set_settings(df)

        amoclient=AmoCRM(df.loc[index, 'access_token'],index)
        df=amoclient.get_all_page('leads/custom_fields')
        gsheet.set_df_to_sheets('custom_fields',df)

if __name__=='__main__':
    pass
    #test_long_task()
    #update_notes_day('4h')
   # webhookWebinar({'leads[status][0][id]': '25431551', 'leads[status][0][status_id]': '34354531', 'leads[status][0][pipeline_id]': '3273697', 'leads[status][0][old_status_id]': '35108005', 'leads[status][0][old_pipeline_id]': '3273697', 'account[id]': '23681254', 'account[subdomain]': 'impactcapital'})