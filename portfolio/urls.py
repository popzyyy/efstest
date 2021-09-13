from django.conf.urls import url
from . import views
from django.urls import path
from django.conf.urls import url
from . import views
from django.urls import path, re_path
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from django.conf.urls import url
from . import views
from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
admin.autodiscover()

app_name = 'portfolio'
urlpatterns = [
    path('', views.home, name='home'),
    re_path(r'^home/$', views.home, name='home'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    path('investment/create/', views.investment_new, name='investment_new'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customer/create/', views.customer_new, name='customer_new'),
    path('fund_list/', views.fund_list, name='fund_list'),
    path('fund/<int:pk>/edit/', views.fund_edit, name='fund_edit'),
    path('fund/<int:pk>/delete/', views.fund_delete, name='fund_delete'),
    path('fund/create/', views.fund_new, name='fund_new'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='portfolio/reset_password.html'), name='reset_password'),
    path('reset_password/done/', auth_views.PasswordResetDoneView.as_view(template_name='portfolio/password_reset_sent.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='portfolio/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='portfolio/password_reset_complete.html'), name='password_reset_complete'),

]



