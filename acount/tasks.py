# Create your tasks here
from __future__ import absolute_import, unicode_literals

import json
from datetime import datetime, timezone
import urllib.request as urllib
import ssl
from django.db.models.functions import Now

import requests
from celery.task import periodic_task
from celery.schedules import crontab

from CRM import celery
from acount.models import Planning


from celery import shared_task, app

@periodic_task(run_every=(crontab(minute='*/5')),name="send")
def send():
    p = Planning.objects.filter(update__lte=Now(), notification=True)
    for i in p:
        inline_button1 = {"text": "View customer", "url": "https://google.com/lead/" + str(i.lead.id)}
        inline_keyboard = [[inline_button1]]
        keyboard = {"inline_keyboard": inline_keyboard}
        replyMarkup = json.dumps(keyboard)
        ssl._create_default_https_context = ssl._create_unverified_context
        text = f"<b>We remind</b>%0AAbout the event «{i.type}» for the client {i.lead.full_name}"
        url = "https://api.telegram.org/bot850217832:AAHA-PAxAQHLRhyS_9XugbtZY7kTOVuBxaY/sendMessage?chat_id=" + i.manager.telegram + "&parse_mode=html&text=" + text + "&reply_markup=" + replyMarkup

        payload = {}
        headers = {}

        requests.request("GET", url, headers=headers, data=payload)
    p.update(notification=False)

