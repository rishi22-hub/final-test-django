

from django.shortcuts import render,redirect
from .forms import LoginForm,ChangePasswordForm,ForgotPasswordForm,ResetPasswordForm,SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes,force_str
from django.contrib import messages
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from django.template.loader import render_to_string
from panels.models import Dealer,Customer
from django.contrib.auth.models import Permission
User = get_user_model()

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        password = request.POST.get('password')
        email = request.POST.get('email')
        user = authenticate(request,email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')  
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


def home(request):
    if not request.user.is_authenticated:
        return redirect("login")
    else:
        return redirect('dashboard')  


 
def forgot_password(request):
    form =ForgotPasswordForm(request.POST or None)
    if form.is_valid():
        email= request.POST.get('email')
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = request.build_absolute_uri(reverse('password_reset_confirm', args=[uid, token]))
        subject = 'Reset Your Password'
        msg     =   f'Click the following link to reset your password:\n{reset_link}'
        html_message = render_to_string('email.html', {'reset_link': reset_link})
        to      = email
        print('sending mail to ', to)
        res     = send_mail(subject, msg,'rishichaitanyatiwari@gmail.com', [to],html_message=html_message)  
        if(res == 1):  
            messages.success(request,"mail sent successfully") 
        else:
            messages.error(request,"Can't send mail")  
        
    return render(request,'forgot_password.html',{'form':form})



def register(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Deactivate the user until they reset their password
           
            user.save()

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(reverse('activate_confirm', args=[uid, token]))

            subject = 'Activate Your Account and Reset Your Password'
            message = f'Click the following link to activate your account and reset your password:\n{reset_link}'
            from_email = 'rishichaitanyatiwari@gmail.com'  # Replace with your email
            recipient_list = [user.email]
            html_message = render_to_string('email.html', {'reset_link': reset_link})
            print('sending mail to ', recipient_list)
            res     = send_mail(subject, message,'rishichaitanyatiwari@gmail.com', recipient_list,html_message=html_message)
            messages.success(request,"mail sent successfully kindly activate your account through it !!")
            return redirect('register')  # Redirect to a success page
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})




def activate_page_in_email(request,uidb64,token):    
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None     
    if user and default_token_generator.check_token(user, token):
        user.is_active=True
        if user.role=="dealer":
            dealer = Dealer.objects.create(
                user=user,
                name=user.first_name+user.last_name,
                email=user.email
            )
            dealer.user_id = user.id
            dealer.save()
           
        else:
            customer = Customer.objects.create(
                user=user,
                name=user.first_name+user.last_name,
                email=user.email
            )
            customer.user_id = user.id
            customer.save()
            

        user.save()
        messages.success(request,"Account Activated successfully!!")
        return redirect('login')
    
    return render(request, 'password_change_page.html')


def password_page_in_email(request,uidb64,token):
    form=ResetPasswordForm(request.POST or None)
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
     
    if user and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_new_password')
            print(new_password,confirm_password)
            if new_password == confirm_password:
                user.set_password(new_password)
                user.save()
                messages.success(request,"password Reset successfully!!")
                return redirect('login')
    
    return render(request, 'password_change_page.html',{'form':form})




def change_password(request,id):    
    try:
        user = User.objects.get(pk=id)
    except User.DoesNotExist:
        messages.error(request,"User does not exist!!")
        return redirect('dashboard')

    if request.method == 'POST':
        form = ChangePasswordForm(request.POST, request=request)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            confirm_new_password = form.cleaned_data['confirm_new_password']

            if new_password == confirm_new_password:
                user.set_password(new_password)
                user.save()
                return redirect('dashboard')
            
    else:
        form = ChangePasswordForm(request=request)

    return render(request, 'password_change_page.html', {'form': form})
