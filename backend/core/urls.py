from django.urls import path
from . import views

urlpatterns = [
    path('', lambda r: views.redirect('/dashboard/')),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('affpartners/', views.affpartner_list, name='affpartner_list'),
    path('affpartners/create/', views.affpartner_create, name='affpartner_create'),
    path('affpartners/<int:pk>/edit/', views.affpartner_edit, name='affpartner_edit'),
    path('affpartners/<int:pk>/delete/', views.affpartner_delete, name='affpartner_delete'),
    path('referrals/', views.referral_list, name='referral_list'),
    path('referrals/create/', views.referral_create, name='referral_create'),
    path('referrals/<int:pk>/edit/', views.referral_edit, name='referral_edit'),
    path('referrals/<int:pk>/delete/', views.referral_delete, name='referral_delete'),
    path('commissions/', views.commission_list, name='commission_list'),
    path('commissions/create/', views.commission_create, name='commission_create'),
    path('commissions/<int:pk>/edit/', views.commission_edit, name='commission_edit'),
    path('commissions/<int:pk>/delete/', views.commission_delete, name='commission_delete'),
    path('settings/', views.settings_view, name='settings'),
    path('api/stats/', views.api_stats, name='api_stats'),
]
