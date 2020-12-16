from datetime import datetime, timedelta, time
from django.core.management.base import BaseCommand
from django.utils import timezone
from ugs.models import Webinars

class Command(BaseCommand):
    help = 'Time'



test = [1, 2, 3, 4, 5, ]
web = Webinars.objects.get(webinarID = 1864)
dd = timezone.now()

print((divmod(( dd-web.webinarDateTime).days * 86400 + (dd-web.webinarDateTime).seconds, 60))[0])

# if (dd + dd(1)).hour == 0:
#     print(1)