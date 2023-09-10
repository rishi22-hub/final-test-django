from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
User = get_user_model()

class LoginForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email'}))
    password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your Password'}))
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')

        # Check if the username and password are valid
        if 'email' in self.cleaned_data and 'password' in self.cleaned_data:
            user = authenticate(email=email, password=password)
            users =User.objects.all()
            mail_list=[user.email for user in users]
            user=User.objects.filter(email=email).first()
            if not email in mail_list:
                raise forms.ValidationError('Mail is not registered !!')            
            elif not user.is_active:
                raise forms.ValidationError('Activate you account from mail!!')
            else:
                raise forms.ValidationError('Invalid username or password or if new account activate from mail received !!')
        return cleaned_data

        

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None or len(email) < 5:
            raise forms.ValidationError("Email must be at least 5 characters long.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if password is None or len(password) < 5:
            raise forms.ValidationError("Password must be of length 5.")
        return password
    # password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your Password'}))
    # email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'enter your email'}))


    
class ForgotPasswordForm(forms.Form):
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Enter your Email'}))
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None or len(email) < 5:
            raise forms.ValidationError("Email must be at least 5 characters long.")
        return email

    def clean(self):
        email = self.cleaned_data.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError('User with that email does not exist.')
        return email




class ChangePasswordForm(forms.Form):
    old_password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your old Password'}))
    new_password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your new Password'}))
    confirm_new_password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your new Password again'}))
    

    def _init_(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super()._init_(*args, **kwargs)
    

    

    def clean(self):
        cleaned_data = super().clean()
        old_password = cleaned_data.get('old_password')
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        print(old_password,confirm_new_password,new_password)
        if old_password and new_password and confirm_new_password:
            user = authenticate(email=self.request.user.email, password=old_password)

            if user is None:
                raise forms.ValidationError('Invalid old password.')

            if len(new_password) < 5:
                raise forms.ValidationError('New password must be at least 5 characters long.')

            if new_password != confirm_new_password:
                raise forms.ValidationError('New passwords do not match.')

            if old_password == new_password:
                raise forms.ValidationError('new password is same as old enter differnt password or click cancel')

        return cleaned_data



class ResetPasswordForm(forms.Form):
    new_password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your new Password'}))
    confirm_new_password= forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Enter your new Password again'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_new_password = cleaned_data.get('confirm_new_password')
        if new_password != confirm_new_password:
            raise forms.ValidationError('passwords do not match.')
    




class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    role = forms.ChoiceField(
        choices=(
        ('dealer', 'Dealer'),
        ('consumer', 'Consumer')
        ),
        widget=forms.Select(attrs={'class': 'form-control'}),
        
    )
    password1='Dev@1234' 

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'role', 'email']

    
    def _init_(self, *args, **kwargs):
        super(SignupForm, self)._init_(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
