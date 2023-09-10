"""
URL configuration for inventory_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from. import views

urlpatterns = [
     path('admin/activate-reset-confirm/<uidb64>/<token>/',views.activate_page_in_email,name='activate_confirm'),
     path('admin/password-reset-confirm/<uidb64>/<token>/',views.password_page_in_email,name='password_reset_confirm'),
    path('admin/login/', views.login_view, name='login'),
    path('admin/logout/', views.logout_view, name='logout'),
    path('admin/forgot_password/',views.forgot_password, name='forgot_password'),
    path('admin/change_password/<int:id>',views.change_password,name='change_password'),
    path('admin/register/',views.register, name='register'),
    path("",views.home,name='home'),
    path("panels/",include('panels.urls')),
    path('admin/', admin.site.urls),
    

]
