import re

from django.core.validators import ValidationError
from django import forms
from django.core.validators import RegexValidator
from datetime import date

class RegisterForm(forms.Form):
    first_name = forms.CharField(min_length=1, max_length=50, label="Your first name")
    last_name = forms.CharField(min_length=1, max_length=50, label='Your last name')
    #was age
    age = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label='Your Birthday',
        required=True
    )
    phone_number = forms.CharField(min_length=15, max_length=30, label="Your phone number")
    login = forms.CharField(min_length=1, max_length=30, label="Login")
    password1 = forms.CharField(label="Password")
    password2 = forms.CharField(min_length=3, max_length=30, label="Password", help_text="again password")
    def clean(self):
        date = self.cleaned_data.get('date')
        if date:
            today = date.today()
            age = today.year - age.year - ((today.month, today.day) < (age.month, age.day))
            if age <= 18:
                self.add_error("you should be 18 years old at leat")




class LoginForm(forms.Form):
    login = forms.CharField(min_length=1, max_length=30, label="Enter login")
    password = forms.CharField(min_length=3, max_length=30, label="Enter password")


class FilterForm(forms.Form):
    typeOfservice = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices={"Run": "Running", "Gym": "Gym", "Gachi": "Gachi", "Youga":"Youga", "Aerobics":"Aerobics"},
    )
    max_price = forms.IntegerField(min_value=1, required=False)


class InstructorForm(forms.Form):

    phone_regex = RegexValidator(
        regex=r'\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="+375 (29) XXX-XX-XX;"
    )
     
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    phone_number = forms.CharField(max_length=30, validators=[phone_regex])
    bio = forms.CharField()
    photo = forms.ImageField(required=False)
    
    
    old_password = forms.CharField(required=False, label="Enter old password",
                                   help_text="this is neccessary field")
    login = forms.CharField()
    password1 = forms.CharField(required=False, label="New password")
    password2 = forms.CharField(required=False, label="repeat new password")


class ClientForm(forms.Form):

    phone_regex = RegexValidator(
        regex=r'\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$',
        message="+375 (29) XXX-XX-XX;"
    )

    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    age = forms.IntegerField(min_value=18, max_value=120)
    phone_number = forms.CharField(max_length=30, validators=[phone_regex])

    old_password = forms.CharField(required=False, label="Enter old password",
                                   help_text="this is neccessary field")
    login = forms.CharField()
    password1 = forms.CharField(required=False, label="New password")
    password2 = forms.CharField(required=False, label="repeat new password")

    def clean(self):
        old_password = self.cleaned_data.get('old_password')
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if old_password:
            if not password1:
                self.add_error('password1', "Enter new password")
            if password1 != password2:
                self.add_error('password2', "Password don't match!")

from django.core.validators import MinValueValidator, MaxValueValidator

class ReviewForm(forms.Form):
    grade = forms.IntegerField(label='Rating', validators=[MinValueValidator(1), MaxValueValidator(5)])
    text = forms.CharField(label='Review', widget=forms.Textarea)                