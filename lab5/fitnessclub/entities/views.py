import calendar
import datetime
from functools import reduce
import io
import os
import random
from matplotlib import pyplot as plt
import requests
import re
from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.generic import DetailView

from fitnessclub.settings import BASE_DIR
from .models import Article, Card, CompanyInfo, Coupon, Faq, Group, Instructor, Review, Service, Hall, Projectile, Client, Vacancy
from .forms import ClientForm, FilterForm, InstructorForm, LoginForm, RegisterForm, ReviewForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group as group, User

from venv import logger

import logging
logging.basicConfig(level=logging.INFO, filename="py_log.log",filemode="w")

# Create your views here.
def home_page(request):
    
    logging.info('Rederecting to home page')
    current_datetime = datetime.datetime.now()
    user_timezone = timezone.localtime(timezone.now())
    text_calendar = calendar.TextCalendar().formatmonth(current_datetime.year, current_datetime.month).split('\n')
    width = len(text_calendar[1])
    text_calendar[0] += ' '*(width-len(text_calendar[0]))
    text_calendar[-2] += ' '*(width-len(text_calendar[-2]))
    text_calendar = '\n' + reduce(lambda x, y: x + '\n' + y, text_calendar)
    ctz = timezone.get_current_timezone_name()
    context = {
        'dt' : current_datetime,
        'tz' : user_timezone,
        'tc' : text_calendar,
        'ctz' : ctz,
    }
    return render(request, 'Home.html', context)

def our_instructors_page(request):
    instructors = Instructor.objects.all()
    return render(request, "OurInstructorsPage.html", {'instructors': instructors})

class InstructorDetailsView(DetailView):
    model = Instructor
    template_name = 'InstructorDetailsPage.html'
    context_object_name = 'instructor'

def services_page(request):
    logging.debug("Fetching all services")
    if request.method == 'POST':
        form = FilterForm(request.POST)
        if form.is_valid():
            logger.debug("Service page form is valid")
            category = form.cleaned_data.get('typeOfservice')
            max_price = form.cleaned_data.get('max_price')
            if max_price == None:
                max_price = 2147483648
            services = Service.objects.filter(price__lte=max_price, typeOfservice__in=category)
            return render(request, "ServicesPage.html", {'form': form, 'services': services})
    else:
        form = FilterForm()
        services = Service.objects.all()
    logging.info("Rendering services list")    
    return render(request, "ServicesPage.html", {'form': form, 'services': services})

def halls_page(request):
    logging.info("Fetching halls list")
    halls = Hall.objects.all()
    projectiles = []
    for hall in halls:
        prjs = []
        prjtmp = hall.projectiles.all()
        for proj in prjtmp:
            prjs.append(proj)
        class tmp:
            h_name = ''
            prj = []    

        t = tmp()
        t.h_name = hall.hall_name
        t.prj = prjs
        projectiles.append(t)        
    return render(request, "HallsPage.html", {'halls': halls, 'projectiles':projectiles})

def login_page(request):
    logger.debug("Login page")

    if request.method == 'POST':
        username = request.POST['login']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.groups.filter(name='Client').count():
                login(request, user)
                logger.info("Client logged in successfully")

                #logger.info("INFO: User is Client")
                return HttpResponseRedirect(reverse('entities:client'))
            elif user.groups.filter(name='Instructor').count():
                login(request, user)
                #logger.info("INFO: User is Instructor")
                # return HttpResponseRedirect('/fitness/instructor/')
                return HttpResponseRedirect(reverse('entities:instructor'))
            elif user.is_superuser:
                login(request, user)
                #logger.info("INFO: User is superuser ")
                return HttpResponseRedirect(reverse('entities:superuser'))
            else:
                form = LoginForm(request.POST)
                error = 'User not found'
                #logger2.warning("WAR: User not found")
                return render(request, 'LoginPage.html', {'form': form, 'error': error})
        else:
            form = LoginForm(request.POST)
            error = 'User not found'
            #logger2.warning("WAR: User not authorized")
            return render(request, 'LoginPage.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
        return render(request, 'LoginPage.html', {'form': form})

@login_required(login_url='login/')
def instructor_page(request):
    logger.info("Instructor page")

    user = request.user
    instructor = Instructor.objects.get(user=user)

    tomorrow = datetime.datetime.today() + datetime.timedelta(days=1)
    today = datetime.datetime.today()

    tomorrow = datetime.datetime(tomorrow.year, tomorrow.month, tomorrow.day)
    today = datetime.datetime(today.year, today.month, today.day)
    services = instructor.services.filter(start_time__lte=tomorrow).filter(start_time__gte=today).order_by('start_time')
    return render(request, 'InstructorPage.html', {'instructor':instructor, 'schedule':services})


@login_required(login_url='login/')
def client_page(request):
    logger.info("Client page")
    user = request.user
    try:
        client = Client.objects.get(user=user)
    except:
        return reverse('entities:login')
    groups = client.group_set.all()
    first_name = user.first_name

    predicted_age = None
    predicted_gender = None

    if first_name:
        # Agify API request
        logger.debug("trying to get age by api")

        agify_response = requests.get(f'https://api.agify.io', params={'name': first_name})
        if agify_response.status_code == 200:
            agify_data = agify_response.json()
            predicted_age = agify_data.get('age')

        # Genderize API request
        genderize_response = requests.get(f'https://api.genderize.io', params={'name': first_name})
        if genderize_response.status_code == 200:
            genderize_data = genderize_response.json()
            predicted_gender = genderize_data.get('gender')
    
    context = {'client': client,
                'groups': groups,
                'predicted_age': predicted_age,
                'predicted_gender': predicted_gender,
                }

    return render(request, "ClientPage.html", context)


from datetime import datetime as dt
def signin_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        

        age = request.POST['age']
        age = dt.strptime(age, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - age.year - ((today.month, today.day) < (age.month, age.day))
        if age < 18:
            form = RegisterForm(request.POST)
            error = "Too yong"
            return render(request, 'SinginPage.html', {'form': form, 'error': error})

        phone_number = request.POST['phone_number']
        
        username = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1 == password2:
            form = RegisterForm(request.POST)
            error = "Password must match"
            return render(request, 'SinginPage.html', {'form': form, 'error': error})
        if not re.fullmatch(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            form = RegisterForm(request.POST)
            error = "Phone number should match this pattern: +375 (ХХ) ХХХ-ХХ-ХХ"
            #logger2.warning("WAR: User phone_number does not match with pattern ")
            return render(request, 'SinginPage.html', {'form': form, 'error': error})
        user = User.objects.create_user(username=username, password=password1)
        user.groups.add(group.objects.get(name='Client'))
        user.save()
        client = Client.objects.create(first_name=first_name,last_name=last_name, age=age, phone_number=phone_number, user=user)
        client.save()
        login(request, user)
        logger.info("User signin successful ")
        # return HttpResponseRedirect('/fitness/client/')
        return HttpResponseRedirect(reverse('entities:client'))
    else:
        form = RegisterForm()
        return render(request, 'SinginPage.html', {'form': form})


def user_page(request):
    user = request.user
    if user.groups.filter(name='Client'):
        # return HttpResponseRedirect('/fitness/client/')
        return HttpResponseRedirect(reverse('entities:client'))
    elif user.groups.filter(name='Instructor'):
        # return HttpResponseRedirect('/fitness/instructor/'))
        return HttpResponseRedirect(reverse('entities:instructor'))
    elif user.is_superuser:
        # return HttpResponseRedirect('/fitness/super_user/'))
        return HttpResponseRedirect(reverse('entities:superuser'))
    else:
        # return HttpResponseRedirect('/account/login/')
        return HttpResponseRedirect(reverse('entities:login'))

def logout_page(request):
    logout(request)
    # return HttpResponseRedirect('/fitness/')
    return HttpResponseRedirect(reverse('entities:homepage'))



@login_required(login_url='login/')
def change_instructor_page(request):
    print('here')
    if request.method == "POST":
        form = InstructorForm(request.POST)
        if not form.is_valid():
            return render(request, "ChangeInstructorPage.html", {'form': form})
        instructor = Instructor.objects.get(user=request.user)
        instructor.first_name = request.POST['first_name']
        instructor.last_name = request.POST['last_name']
        instructor.phone_number = request.POST['phone_number']
        instructor.bio = request.POST['bio']
        if request.FILES:
            if os.path.exists(str(BASE_DIR) + instructor.photo.url):
                os.remove(str(BASE_DIR) + instructor.photo.url)
            instructor.photo = request.FILES['photo']
        if request.POST['old_password']:
            error = None
            if not instructor.user.check_password(request.POST['old_password']):
                error = "Password don't match with current"
            if request.POST['password1'] != request.POST['password2']:
                error = "Passwords should match"
            if not request.POST['password1']:
                error = "Field must not be empty"
            if not request.POST['login']:
                error = "Field must not be empty"
            if error:
                form = InstructorForm(request.POST)
                return render(request, "ChangeInstructorPage.html", {'form': form, 'error': error})
            instructor.user.set_password(request.POST['password1'])
            instructor.user.username = request.POST['login']
            instructor.user.save()
        instructor.save()
        return HttpResponseRedirect(reverse('entities:user'))
    else:
        instructor = Instructor.objects.get(user=request.user)
        form = InstructorForm({'first_name': instructor.first_name,
                               'last_name': instructor.last_name,
                               'phone_number': instructor.phone_number,
                               'bio': instructor.bio,
                               'photo': instructor.photo,
                               'login': instructor.user.username
                               })
    return render(request, "ChangeInstructorPage.html", {'form': form})

@login_required(login_url='login/')
def change_client_page(request):
    print('Changing client///////////////////////////////////////////////')
    client = Client.objects.get(user=request.user)

    if request.method == "POST":
        form = ClientForm(request.POST)
        if not form.is_valid():
            return render(request, "ChangeClientPage.html", {'form': form})

        if request.POST['old_password']:
            if client.user.check_password(request.POST['old_password']):
                client.user.set_password(request.POST['password1'])
                client.user.username = request.POST['login']
                client.user.save()
            else:
                error = "Entered password do not match with current"
                return render(request, "ChangeClientPage.html", {'form': form, 'error': error})

        client.first_name = form.cleaned_data.get('first_name')
        client.last_name = form.cleaned_data.get('last_name')
        client.age = form.cleaned_data.get('age')
        client.phone_number = form.cleaned_data.get('phone_number')
        client.save()
        return HttpResponseRedirect(reverse('entities:user'))

    form = ClientForm({'first_name': client.first_name,
                       'last_name': client.last_name,
                       'age': client.age,
                       'phone_number': client.phone_number,
                       'login': client.user.username})
    return render(request, "ChangeClientPage.html", {'form': form})

@login_required(login_url='login/')
def client_group_page(request, id):
    group = Group.objects.get(id=id)
    services = group.service_set.all()
    return render(request, "GroupDetailsPage.html", {'group': group, 'services': services})

@login_required(login_url='login/')
def groups_page(request):
    client = Client.objects.get(user=request.user)
    groups = Group.objects.filter(is_open=True).exclude(id__in=client.group_set.all())
    return render(request, "GroupsPage.html", {'groups': groups})

@login_required(login_url='login/')
def group_buy_page(request, id):
    group = Group.objects.get(id=id)
    if request.method == "POST":
        client = Client.objects.get(user=request.user)
        client.group_set.add(group)
        coupon = Coupon.objects.filter(code=request.POST['coupon'])
        if coupon.count() and coupon[0].end_date > datetime.date.today():
            coupon = coupon[0].discount
        else:
            coupon = 0
        if client.card:    
            if client.card.exp_date > datetime.date.today():
                coupon += client.card.discount
        client.costs += group.all_price * (100 - coupon) / 100
        if group.max_clients <= group.clients.count():
            group.is_open = False
        client.save()
        return HttpResponseRedirect(reverse('entities:client'))
    services = group.service_set.all()
    return render(request, "GroupBuyPage.html", {'group': group, 'services': services})

@login_required(login_url='login/')
def client_club_card_page(request):
    user = request.user
    client = Client.objects.get(user=user)
    client.costs += 20
    exp_date = datetime.datetime.today() + datetime.timedelta(days=365)
    discount = random.randint(1, 20)
    if discount <= 5:
        name = 'Silver card'
    elif discount <= 10:
        name = 'Gold card'
    elif discount <= 15:
        name = 'Platinum card'
    else:
        name = 'Elit card'
    try:
        client.card = Card.objects.update(name=name, discount=discount, exp_date=exp_date, client=client)
    except:
        client.card.delete()
        client.card = Card.objects.create(name=name, discount=discount, exp_date=exp_date, client=client)
    client.save()
    return HttpResponseRedirect(reverse('entities:user'))

@login_required(login_url='login/')
def service_clients_page(request, id):
    service = Service.objects.get(id=id)
    clients = service.group.clients.all()
    return render(request, "ServiceClientsPage.html", {'clients': clients})


from django.db.models import Avg, Count, Sum
from datetime import date, timedelta
from django.db import models

@login_required(login_url='admin/')
def superuser_page(request):
    clients = Client.objects.all().order_by("first_name")

    total_costs = clients.aggregate(Sum("costs"))

    avg_costs = clients.aggregate(Avg("costs"))

    avg_age = clients.aggregate(Avg("age"))["age__avg"]

    now = datetime.datetime.now()
    one_month_ago = now - timedelta(days=30)
    
    group_services = Group.objects.annotate(
        total_services=Count("service", filter=models.Q(service__start_time__gte=one_month_ago, service__start_time__lte=now))
    )

    client_services = clients.annotate(
        total_services=Sum("group__service__price")
    )

    service_categories = Service.objects.values("typeOfservice").annotate(
        count=Count("id")
    ).order_by("-count")

    profitable_services = Service.objects.values("typeOfservice").annotate(
        total_revenue=Sum("price")
    ).order_by("-total_revenue")


    context = {
        "clients": clients,
        "total_costs": total_costs["costs__sum"],
        "avg_costs": avg_costs["costs__avg"],
        "avg_age": avg_age,
        "group_services": group_services,
        "client_services": client_services,
        "service_categories": service_categories,
        "profitable_services": profitable_services,
    }
    return render(request, 'SuperuserPage.html', context)


def about_page(request):
    try:
        latest_article = Article.objects.order_by('-date')[0]
    except IndexError:
        latest_article = None
    return render(request, 'AboutPage.html', {'article' : latest_article
                                              
                                              })


def company_info_page(request):
    info = CompanyInfo.objects.order_by("date")
    return render(request, "CompanyInfoPage.html", {'info': info})

def news_page(request):
    info = Article.objects.order_by("-date")
    return render(request, "NewsPage.html", {'news': info})

def employees_page(request):
    instructors = Instructor.objects.all()
    return render(request, "OurInstructorsPage.html", {'instructors': instructors})

def faq_page(request):
    faqs = Faq.objects.order_by('-date')
    return render(request, "FukPage.html", {'faqs': faqs})


def vacancies_page(request):
    vac = Vacancy.objects.all()
    return render(request, "VacanciesPage.html", {'vacancies': vac})


def reviews_page(request):
    reviews = Review.objects.order_by('-date')
    return render(request, "ReviewsPage.html", {'reviews': reviews})


def coupons_page(request):
    coupons = Coupon.objects.order_by('-end_date')
    return render(request, "CouponsPage.html", {'coupons': coupons})


def create_review_page(request):
    user = request.user
    try:
        client = Client.objects.get(user=user)
    except:
        return HttpResponseRedirect(reverse('entities:reviews')) 
    if client:
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            name = Client.objects.get(user=request.user).first_name
            date = datetime.datetime.now()
            text = request.POST['text']
            grade = request.POST['grade']
            Review.objects.create(name=name, date=date, text=text, grade=grade)
            return HttpResponseRedirect(reverse('entities:reviews'))
        else:
            return render(request, 'CreateReviewPage.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('entities:reviews'))    


def age_chart(request):
    age_distribution = (
        Client.objects.values("age").annotate(count=Count("id")).order_by("age")
    )
    age_labels = [item["age"] for item in age_distribution]
    age_counts = [item["count"] for item in age_distribution]
    plt.figure(figsize=(10, 6))
    plt.bar(age_labels, age_counts, color='black')
    plt.xlabel("Age")
    plt.ylabel("Client")
    plt.title("Age distribution")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='png')


def service_chart(request):

    now = datetime.datetime.now()
    one_month_ago = now - timedelta(days=30)

    group_services = Group.objects.annotate(
        total_services=Count("service", filter=models.Q(service__start_time__gte=one_month_ago))
    )

    group_names = [group.name for group in group_services]
    service_counts = [group.total_services for group in group_services]

    plt.figure(figsize=(10, 6))
    plt.bar(group_names, service_counts, color='r')
    plt.xlabel("Groups")
    plt.ylabel("Num of services by month")
    plt.title("Services by groups distribution")

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    
    buffer.seek(0)
    return HttpResponse(buffer, content_type='png')


@login_required(login_url='admin/')
def age_distrib(request):
    return render(request, 'AgeDistributionPage.html')

@login_required(login_url='admin/')
def service_distrib(request):
    return render(request, 'ServiceDistributionPage.html')

@login_required(login_url='admin/')
def chose(request):
    obj = Instructor.objects.all()
    return render(request, 'ToDelete.html', {'instructors':obj})



@login_required(login_url='admin/')
def delete_selected(request, id):
    user = Instructor.objects.get(id=id)
    user.delete()
    obj = Instructor.objects.all()
    
    return render(request, 'ToDelete.html', {'instructors':obj})

@login_required(login_url='admin/')
def crinst(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        

        age = request.POST['age']
        age = dt.strptime(age, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - age.year - ((today.month, today.day) < (age.month, age.day))
        if age < 18:
            form = RegisterForm(request.POST)
            error = "Too yong"
            return render(request, 'ToCreate.html', {'form': form, 'error': error})

        phone_number = request.POST['phone_number']
        
        username = request.POST['login']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if not password1 == password2:
            form = RegisterForm(request.POST)
            error = "Password must match"
            return render(request, 'ToCreate.html', {'form': form, 'error': error})
        if not re.fullmatch(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', phone_number):
            form = RegisterForm(request.POST)
            error = "Phone number should match this pattern: +375 (ХХ) ХХХ-ХХ-ХХ"
            #logger2.warning("WAR: User phone_number does not match with pattern ")
            return render(request, 'ToCreate.html', {'form': form, 'error': error})
        user = User.objects.create_user(username=username, password=password1, first_name = first_name, last_name=last_name, email='test@test.com')
        user.groups.add(group.objects.get(name='Instructor'))
        user.save()
        inst = Instructor.objects.create(first_name=first_name,last_name=last_name, phone_number=phone_number, user=user, bio ='Nothing here')
        inst.save()
        #login(request, user)
        logger.info("User signin successful ")
        # return HttpResponseRedirect('/fitness/client/')
        return HttpResponseRedirect(reverse('entities:superuser'))
    else:
        form = RegisterForm()
        return render(request, 'ToCreate.html', {'form': form})