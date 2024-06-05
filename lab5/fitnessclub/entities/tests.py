from django.test import TestCase

# Create your tests here.
import pytest
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Client, Group, Hall, Service, Instructor, Schedule, Card
from .forms import RegisterForm
from .models import CompanyInfo
from .forms import ClientForm, InstructorForm
from datetime import datetime, timedelta


class ClientModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testuser", password="testpassword")
        self.client = client = Client.objects.create(
            first_name="Roma",
            last_name="Bro",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )

    def test_create_client(self):
        self.assertEqual(self.client.first_name, "Roma")

    def test_age(self):
        self.assertEqual(self.client.age, 25)

    def test_last(self):
        self.assertEqual(self.client.last_name, "Bro")    


    # def test_invalid_phone_number(self):
    #     client = Client(
    #         first_name="Roma",
    #         last_name="Bro",
    #         age=30,
    #         phone_number="2281337",
    #         user=self.user
    #     )
    #     with self.assertRaises(ValidationError):
    #         client.clean()

    def test_negative_age(self):
        client = Client(
            first_name="Roma",
            last_name="Bro",
            age=-1,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_empty_fullname(self):
        client = Client(
            first_name="",
            last_name="",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.full_clean()

    def test_long_fullname(self):
        client = Client(
            first_name="Roma" * 50,
            last_name="Bro",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )
        with self.assertRaises(ValidationError):
            client.full_clean()
            


class GroupModelTest(TestCase):
    def setUp(self):
        self.client = Client.objects.create(
            first_name="Roma",
            last_name="Bro",
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=User.objects.create(username="anotheruser", password="password")
        )

    def test_create_group(self):
        group = Group.objects.create(name="Yoga Group", all_price=500)
        self.assertEqual(group.name, "Yoga Group")

    def test_group_with_clients(self):
        group = Group.objects.create(name="Yoga Group", all_price=500)
        group.clients.add(self.client)
        self.assertEqual(group.clients.count(), 1)

    def test_group_with_invalid_price(self):
        group = Group(name="Yoga Group", all_price=-100)
        with self.assertRaises(ValidationError):
            group.full_clean()

    # def test_duplicate_group_name(self):
    #     Group.objects.create(name="Yoga Group", all_price=500)
    #     with self.assertRaises(ValidationError):
    #         Group.objects.create(name="Yoga Group", all_price=500)


class HallModelTest(TestCase):
    def test_create_hall(self):
        hall = Hall.objects.create(hall_name="Main Hall")
        self.assertEqual(hall.hall_name, "Main Hall")

    def test_create_hall_with_empty_name(self):
        hall = Hall.objects.create(hall_name="")
        with self.assertRaises(ValidationError):
            hall.full_clean()

    # def test_duplicate_hall_name(self):
    #     Hall.objects.create(hall_name="Main Hall")
    #     with self.assertRaises(ValidationError):
    #         Hall.objects.create(hall_name="Main Hall")


class WorkoutModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Yoga Group", all_price=500)
        self.hall = Hall.objects.create(hall_name="Main Hall")

    def test_create_workout(self):
        service = Service.objects.create(
            start_time=datetime.now(),
            end_time=datetime.now() + timedelta(hours=1),
            price=100,
            typeOfservice="Yoga",
            group=self.group,
            hall=self.hall
        )
        self.assertEqual(service.typeOfservice, "Yoga")

class GroupScheduleModelTest(TestCase):
    def setUp(self):
        self.group = Group.objects.create(name="Yoga Group", all_price=500)

    def test_create_group_schedule(self):
        group_schedule = Schedule.objects.create(
            info="Yoga schedule",
            group=self.group
        )
        self.assertEqual(group_schedule.info, "Yoga schedule")

    def test_group_schedule_without_group(self):
        group_schedule = Schedule(info="Yoga schedule")
        with self.assertRaises(ValidationError):
            group_schedule.full_clean()


class ClubCardModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(username="testclient", password="testpassword")
        self.client = Client.objects.create(
            first_name="Roma",
            last_name='Bro',
            age=25,
            phone_number="+375 (29) 123-45-67",
            user=self.user
        )

    def test_create_club_card(self):
        club_card = Card.objects.create(
            name="Gold",
            exp_date=datetime.now() + timedelta(days=365),
            discount=10,
            client=self.client
        )
        self.assertEqual(club_card.name, "Gold")

    def test_club_card_with_high_discount(self):
        club_card = Card(
            name="Gold",
            exp_date=datetime.now() + timedelta(days=365),
            discount=1000,
            client=self.client
        )
        
class ChangePagesViewsTest(TestCase):

    def setUp(self):
        self.test_user = User.objects.create_user(username="testuser", password="password123")

        self.instructor = Instructor.objects.create(
            user=self.test_user,
            first_name="Test",
            last_name='Tset',
            phone_number="123-456-7890",
        )

        self.client = Client.objects.create(
            user=self.test_user,
            first_name="Roma",
            last_name='Bro',
            age=25,
            phone_number="098-765-4321",
        )

        self.auth_client = self.client
        self.client_logged_in = self.client.login(username=self.test_user.username, password="password123")

    def test_instructor_change_page_get(self):
        url = reverse("entities:change_instructor")
        response = self.client_logged_in.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context["form"], InstructorForm)
        self.assertEqual(response.context["form"]["first_name"].value(), self.instructor.first_name)