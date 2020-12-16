import json

from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import View
import logging
from braces.views import CsrfExemptMixin
from amoCRM_update_lib import webhookWebinar
from .models import Registers, Parameters
from urllib.parse import unquote
import urllib.request
from django.shortcuts import render, redirect
from django.http import HttpResponse
import string
import random
import datetime
from django.views.generic import TemplateView

logger = logging.getLogger(__name__)
class ProccesHookView(CsrfExemptMixin, View):
    def post(self, request, *args, **kwargs):
        logger.info('getting hook...')
        # print(request)
        # print(request.body)
        # my_json = request.body.decode('utf8')
        # logger.info(my_json)
        # print(my_json)
        # # print(my_json)
        # # print('- ' * 20)
        # logger.info(urllib.request.urlopen(request.body.decode('utf8')))
        # logger.info(json.loads(unquote(request.body.decode('utf8'))))

        # Load the JSON to a Python list & dump it back out as formatted JSON
        data = urllib.parse.parse_qs(request.body.decode('utf-8'))
        main_data = json.dumps(data, indent=4, sort_keys=True)
        # print(main_data)
        logger.info(type(request.body.decode('utf-8')))
        logger.info(f'hook\n{main_data}')

        if 'leads[status][0][id]' in data:
            # print(data['leads[status][0][id]'])
            res = webhookWebinar(data)
            logger.info(res)

            regProfile = Registers.objects.filter(userNum = res[1], userStatus = 'Нет').first()
            if regProfile == None:
                logger.warning('mail not found, skip...')
            else:
                regProfile.userStatus = res[0]
                regProfile.save()

                logger.info('status changed, continue...')
        else:

            logger.warning('invalid hook, skip...')

        return HttpResponse()





# Create your views here.
def hello(request):
    # logger.info(f'{request}')
    print(request.COOKIES['roistat_visit'])
    parameter = Parameters.objects.all().last()
    parameter.roistat_visit = request.COOKIES['roistat_visit']
    parameter.save()

    return redirect(f'https://t.me/Testchatmessagebot?start={parameter.telegramIdLink}')

def hello1(request):
    # logger.info(f'{request}')
    def random_char(y):
        return ''.join(random.choice(string.ascii_letters) for x in range(y))
    myDict = dict(request.GET.lists())
    new_parameter = Parameters.objects.create(utm_source    = myDict['utm_source'][0],
                                              utm_medium    = myDict['utm_medium'][0],
                                              utm_campaign  = myDict['utm_campaign'][0].replace('{', '').replace('}', ''),
                                              utm_content   = myDict['utm_content'][0].replace('{', '').replace('}', ''),
                                              utm_term      = myDict['utm_term'][0].replace('{', '').replace('}', ''),
                                              telegramIdLink = random_char(5))
    new_parameter.save()
    # print(myDict['utm_source'][0])
    # print(myDict['utm_medium'][0])
    # print(myDict['utm_campaign'][0].replace('{', '').replace('}', ''))
    # print(myDict['utm_content'][0].replace('{', '').replace('}', ''))
    # print(myDict['utm_term'][0].replace('{', '').replace('}', ''))
    return render(request, 'redirect.html')



class HomePageView(TemplateView):
    template_name = 'redirect.html'

    # def get(self, request, *args, **kwargs):
    #     print(3451234513)



def test(request):

    print(35486)
    return HomePageView.as_view()
# def viewArticle(request, articleId):
#     """ A view that display an article based on his ID"""
#     text = "Displaying article Number : %s" % articleId
#     return redirect(viewArticles, year="2045", month="02")
#
#
# def viewArticles(request, year, month):
#     text = "Displaying articles of : %s/%s" % (year, month)
#     return HttpResponse(text)