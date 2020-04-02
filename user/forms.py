from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Column, HTML, Layout, Reset, Row, Submit


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(label="Password", widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField(label="Username")
    first_name = forms.CharField(label="First Name")
    last_name = forms.CharField(label="Last Name")
    email = forms.EmailField(label="Email", widget=forms.EmailInput)
    password = forms.CharField(
        max_length=20, label="Password", widget=forms.PasswordInput)
    confirm = forms.CharField(
        max_length=20, label="Confirm Password", widget=forms.PasswordInput)

    def clean(self):
        errors = dict()
        password = self.cleaned_data['password']
        confirm = self.cleaned_data['confirm']
        username = self.cleaned_data['username']
        try:
            email = self.cleaned_data['email'].lower()
        except KeyError:
            raise forms.ValidationError(errors)
        if User.objects.filter(email=email):
            errors['email'] = f"{email} is used."
        
        if User.objects.filter(username=username):
            errors['username'] = f"{username} is used."        

        if len(password) < 8:
            errors['password'] = 'Your password must contain at least 8 characters.'
            errors['confirm'] = 'Your password must contain at least 8 characters.'
        if password != confirm:
            errors['confirm'] = 'The two password fields didn’t match.'
        if errors:
            raise forms.ValidationError(errors)

    def clean_username(self):
        data = self.cleaned_data['username']
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        return data.title()

    def clean_last_name(self):
        data = self.cleaned_data["last_name"]
        return data.upper()

    def clean_email(self):
        data = self.cleaned_data["email"]
        return data.lower()

    def clean_password(self):
        data = self.cleaned_data["password"]
        return data


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]

        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
        }

        widget = {
            'email': forms.EmailInput,
        }

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True

        self.fields['username'].widget.attrs['readonly'] = True
        self.fields['username'].help_text = 'Your username cannot change.'

        self.helper = FormHelper(self)
        self.helper.form_method = 'POST'

        self.helper.layout = Layout(
            Row(
                Column('username', css_class='form-group col-sm mb-0'),
            ),
            Row(
                Column('email', css_class='form-group col mb-0'),
            ),
            Row(
                Column('first_name', css_class='form-group col-sm mb-0'),
                Column('last_name', css_class='form-group col-sm mb-0'),
            ),
        )
        self.helper.layout.append(
            Submit('submit', 'Update',
                   css_class='btn btn-block btn-lg btn-success')
        )
        self.helper.layout.append(
            HTML(
                """
                <div class="text-center">
                      <p>
                        <small class="text-danger">
                        Please make sure you have entered all the information correctly to complete your registration.                        </small>
                      </p>
                    </div>
                """
            )
        )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("Email already exists")
        return email


