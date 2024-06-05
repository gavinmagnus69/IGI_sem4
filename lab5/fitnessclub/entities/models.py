import datetime
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

class Base(models.Model):
    create_date = models.DateTimeField(auto_now=True)
    update_date = models.DateTimeField(auto_now=True)
    
    local_create_date = models.DateTimeField(auto_now=True)
    local_update_date = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        super().save()
        
        if not self.id:
            self.local_create_date = datetime.datetime.now(timezone.timezone.utc).astimezone()
        
        self.update_date = datetime.datetime.now()
        self.local_update_date = datetime.datetime.now(timezone.timezone.utc).astimezone()

    class Meta:
        abstract = True


# Create your models here.
class Client(Base):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
   
    phone_regex = RegexValidator(
        regex=r'\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="+375 (29) XXX-XX-XX;   "
    )

    age = models.PositiveSmallIntegerField(default=0)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    date_of_birth = models.DateField(default=datetime.date.today())

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=19,
        blank=True,
        null=True
    )

    costs = models.FloatField(default=0, validators=[MinValueValidator(0)])
    def clean(self):
        super().clean()

    def __str__(self) -> str:
        return self.first_name    

class Projectile(Base):
    name = models.CharField(max_length=30, help_text="enter name of projectile(гиря тд тп)")
    def __str__(self) -> str:
        return self.name


# Залы
class Hall(Base):
    projectiles = models.ManyToManyField(Projectile, help_text='select projectiles for this hall')
    hall_name = models.CharField(max_length=20, help_text='enter hall name')
    def __str__(self) -> str:
        return self.hall_name

class Group(Base):
    name = models.CharField(max_length=50)
    all_price = models.FloatField(default=0, validators=[MinValueValidator(0)])
    max_services = models.PositiveSmallIntegerField(default=10)
    max_clients = models.PositiveSmallIntegerField(default=10)
    is_open = models.BooleanField(default=False)
    is_edit = models.BooleanField(default=True)
    clients = models.ManyToManyField(Client, blank=True)
    def __str__(self) -> str:
        return self.name

class Service(Base):

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    price = models.FloatField(default=0, validators=[MinValueValidator(0)])

    typeOfservice = models.CharField(max_length=100, default='Gym')

    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True)

    hall = models.ForeignKey(Hall, on_delete=models.SET_NULL, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.group.all_price = self.group.all_price + self.price
        self.group.save()

    def __str__(self) -> str:
        return self.typeOfservice        

class Instructor(Base):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)

    phone_regex = RegexValidator(
        regex=r'\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="+375 (29) XXX-XX-XX;   "
    )

    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=19,
        blank=True,
        null=True
    )

    bio = models.TextField(null=True, default=None)

    photo = models.ImageField(upload_to="instructors/", default='billy')

    services = models.ManyToManyField(Service, default=Service.objects.get(id=1))
    
    def clean(self):
        super().clean()
    def __str__(self) -> str:
        return self.first_name + self.last_name
        
class Schedule(Base):
    info = models.TextField()
    group = models.OneToOneField(Group, on_delete=models.CASCADE)

class Card(Base):
    client = models.OneToOneField(Client, on_delete=models.CASCADE)

    name = models.CharField(max_length=50)
    discount = models.PositiveSmallIntegerField() #%100
    exp_date = models.DateField()
    def __str__(self) -> str:
        return self.name


class CompanyInfo(Base):
    logo = models.CharField(max_length=20)
    bio = models.TextField()
    requisites = models.TextField()
    date = models.DateField()


class Article(Base):
    date = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    text = models.TextField()
    picture = models.ImageField(upload_to="articles", default='')


class Faq(Base):
    date = models.DateField()
    question = models.TextField()
    answer = models.TextField()


class Vacancy(Base):
    name = models.CharField(max_length=30)
    description = models.TextField()
    salary = models.CharField(max_length=40)



class Review(Base):
    name = models.TextField()
    grade = models.PositiveSmallIntegerField()
    text = models.TextField()
    date = models.DateTimeField()


class Coupon(Base):
    name = models.CharField(max_length=30)
    description = models.TextField()
    code = models.CharField(max_length=10)
    discount = models.PositiveSmallIntegerField(default=5, validators=[MaxValueValidator(100)])
    end_date = models.DateField()