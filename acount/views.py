from datetime import datetime, timezone
import json
import urllib
import ssl

from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models.functions import Now
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import requests

from acount.models import User, Leads, Planning


def logout_view(request):
    logout(request)
    return redirect('/login/')


@login_required(login_url='login/')
def PlanningPage(request):
    SLS = User.objects.filter(role="SLS")

    if(request.user.role == 'CLS' ):
        SLS = User.objects.filter(role="SLS",closer=request.user)

    CLS = User.objects.filter(role="CLS")
    filter = json.loads(json.dumps(request.GET))

    if (request.GET.get('page')):
        del filter['page']
    if (request.GET.get('start') and request.GET.get('end')):
        del filter['start']
        del filter['end']
        format = '%d/%m/%Y %H:%M:%S';
        s = request.GET.get('start') + " 00:01:00"
        e = request.GET.get('start') + " 23:59:00"
        start = datetime.strptime(s, format).strftime('%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(e, format).strftime('%Y-%m-%d %H:%M:%S')
        filter['update__range'] = [start, end]

    filter_url=urllib.parse.urlencode(filter)

    if (request.user.role == "SLS"):
        filter['creator'] = request.user.username
    elif (request.user.role == "CLS"):
        filter['manager'] = request.user
    filter['active'] = False
    plans = Planning.objects.filter(**filter)
    plans=plans.order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(plans, 100)
    try:
        plans = paginator.page(page)
    except PageNotAnInteger:
        plans = paginator.page(1)
    except EmptyPage:
        plans = paginator.page(paginator.num_pages)

    return render(request, 'planning.html',{
        'plans':plans,
        'filter_url':filter_url,
        'SLS':SLS,
        'CLS':CLS,
        'get':filter,
        'active': 'plan',
        'start':request.GET.get('start'),
        'end':request.GET.get('end'),
         })


@login_required(login_url='login/')
def home(request):
    # ll = int(datetime.now(tz=timezone.utc).timestamp())
    # timestamp = datetime.fromtimestamp(ll)
    # timestamp.strftime('%Y-%m-%d %H:%M:%S')
    # ssl._create_default_https_context = ssl._create_unverified_context
    # req = urllib.request.Request('https://api.telegram.org/bot850217832:AAHA-PAxAQHLRhyS_9XugbtZY7kTOVuBxaY/sendMessage?chat_id=214792065&parse_mode=html&text='+ll)
    # urllib.request.urlopen(req)

    SLS = User.objects.filter(role="SLS")
    CLS = User.objects.filter(role="CLS")
    filter= json.loads(json.dumps(request.GET))
    # get['manager']=request.user.id
    if(request.GET.get('page')):
        del filter['page']
    if(request.GET.get('start') and request.GET.get('end')):
        del filter['start']
        del filter['end']
        format= '%d/%m/%Y %H:%M:%S';
        s =request.GET.get('start')+" 00:01:00"
        e =request.GET.get('start')+" 23:59:00"
        start = datetime.strptime(s,format).strftime('%Y-%m-%d %H:%M:%S')
        end = datetime.strptime(e,format).strftime('%Y-%m-%d %H:%M:%S')
        filter['date__range']=[start, end]





    filter_url=urllib.parse.urlencode(filter)

    if(request.user.role=="ADM"):
        leads = Leads.objects.filter(**filter)
    elif(request.user.role=="SLS"):
        filter['manager']=request.user.id
        leads = Leads.objects.filter(**filter)
    elif(request.user.role=="CLS"):
        filter['manager__closer']=request.user.id

        leads = Leads.objects.filter(**filter)
    leads=leads.order_by('-id')

    page = request.GET.get('page', 1)

    paginator = Paginator(leads, 100)
    try:
        leads = paginator.page(page)
    except PageNotAnInteger:
        leads = paginator.page(1)
    except EmptyPage:
        leads = paginator.page(paginator.num_pages)

    return render(request, 'index.html',{
        'leads':leads,
        'filter_url':filter_url,
        # 'll':timestamp,
        'SLS':SLS,
        'CLS':CLS,
        'get':filter,
        'active': 'home',
        'start':request.GET.get('start'),
        'end':request.GET.get('end'),
         })

@login_required(login_url='login/')
def lead(request,id):

    lead= Leads.objects.get(id=id)
    if(request.user.role!="ADM"):
        if(lead.manager.closer!=request.user):
            if(lead.manager!=request.user):
                return redirect('/')



    if request.user.role=='ADM':
        managers= User.objects.all()
    elif request.user.role=='CLS':
        managers= User.objects.filter(closer=request.user)
    else:
        managers=''
    planning = Planning.objects.filter(lead=id).order_by('-id')

    return render(request, 'lead.html',{'lead':lead,'managers':managers,'planning':planning,'active':'home'})
@login_required(login_url='login/')
def AjaxCreateLead(request):
    if request.method == 'POST':
        if(request.POST.get('full_name') and request.POST.get('phone')):
            Leads.objects.create(full_name=request.POST.get('full_name'),phone=request.POST.get('phone'),manager=request.user)
            lastid = Leads.objects.latest().id
            return HttpResponse('/lead/' + str(lastid))
        else:
            return HttpResponse('Name and phone empty')


    return HttpResponse('Bad request')
@login_required(login_url='login/')
def AjaxCreatePlanning(request):
    if request.method == 'POST':
        planning = Planning.objects.filter(lead=request.POST.get('id'),active=False)

        if(planning):
            return HttpResponse('Finish plans')

        elif(request.POST.get('date')==''):
            return HttpResponse('Set date')

        else:
            format = '%d/%m/%Y %H:%M'

            start = datetime.strptime(request.POST.get('date'), format).strftime('%Y-%m-%d %H:%M')
            lead = Leads.objects.get(id=request.POST.get('id'))
            Planning.objects.create(lead=lead, manager=lead.manager.closer, creator=request.user.username,
                                    type=request.POST.get('type'), update=start)
            lastid = Leads.objects.latest().id

            Leads.objects.filter(id=lastid).update(update=Now())

            return HttpResponse('ok')

    return HttpResponse('Bad request')
@login_required(login_url='login/')
def AjaxUpdateLead(request):
    if request.method == 'POST':
        field_set={
            'id':request.POST.get('id'),
            'date':Leads.objects.get(id=request.POST.get('id')).date,
            'update':Now(),
            'status':request.POST.get('status'),
            'full_name':request.POST.get('full_name'),
            'phone':request.POST.get('phone'),
            'about_client':request.POST.get('about_client'),
            'source':request.POST.get('source'),
            'manager':User.objects.get(id=request.POST.get('manager')),
        }
        Leads(**field_set).save()
        return HttpResponse('ok')


    return HttpResponse('Bad request')
@login_required(login_url='login/')
def AjaxUpdatePlanning(request):
    if request.method == 'POST':
        if(request.POST.get('comment')!='' and len(request.POST.get('comment'))>=5):
            field_set={
                'finished':Now(),
                'active':True,
                'notification':False,
                'comment':request.POST.get('comment'),
            }
            object=Planning.objects.filter(id=request.POST.get('id'))

            object.update(**field_set)
            Leads.objects.filter(id=object[0].lead.id).update(update=Now())
            return HttpResponse('ok')
        else:
            return HttpResponse('Enter a comment more than 5 characters')


    return HttpResponse('Bad request')
@login_required(login_url='login/')
def test(request):
    p=Planning.objects.filter(update__lte=Now(),notification=True)
    for i in p:
        inline_button1 = {"text" : "View customer","url" : "https://google.com/lead/"+str(i.lead.id)}
        inline_keyboard = [[inline_button1]];
        keyboard = {"inline_keyboard": inline_keyboard}
        replyMarkup = json.dumps(keyboard)
        t+=i.manager.telegram
        ssl._create_default_https_context = ssl._create_unverified_context
        text= f"<b>We remind</b>%0AAbout the event «{i.type}» for the client {i.lead.full_name}"
        url = "https://api.telegram.org/bot850217832:AAHA-PAxAQHLRhyS_9XugbtZY7kTOVuBxaY/sendMessage?chat_id="+i.manager.telegram+"&parse_mode=html&text="+text+"&reply_markup="+replyMarkup

        payload = {}
        headers = {}

        requests.request("GET", url, headers=headers, data=payload)
    p.update(notification=False)

    return render(request, 'test.html', {

        'p': p,

    })