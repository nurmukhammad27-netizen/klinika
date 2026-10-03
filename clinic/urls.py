from django.urls import path
from . import views

urlpatterns = [
    # Main Dashboard
    path('', views.dashboard_view, name='dashboard'),

    # Asosiy operatsiyalar
    path('patients/', views.patients_list, name='patients_list'),
    path('doctors/', views.doctors_list, name='doctors_list'),
    path('rooms/', views.rooms_list, name='rooms_list'),
    path('receipt/<int:appointment_id>/', views.print_receipt, name='print_receipt'),

    # Qo'shimcha bo'limlar
    path('partners/', views.partners_view, name='partners'),
    path('staff/', views.staff_view, name='staff'),
    path('expenses/', views.expenses_view, name='expenses'),
    path('cards/', views.cards_view, name='cards'),
    path('procedures/', views.procedures_view, name='procedures'),
    path('ultrasound/', views.ultrasound_view, name='ultrasound'),
    path('wards/', views.wards_view, name='wards'),
    path('lab/', views.lab_view, name='lab'),
    
    # Omborxona (Inventory)
    path('medicines/', views.medicines_view, name='medicines'),
    path('reagents/', views.reagents_view, name='reagents'),
    path('supplies/', views.supplies_view, name='supplies'),
    path('household/', views.household_view, name='household'),

    # Hisobotlar va Sozlamalar
    path('reports/financial/', views.financial_report_view, name='financial_report'),
    path('reports/doctors/', views.doctors_report_view, name='doctors_report'),
    path('settings/', views.settings_view, name='settings'),
    path('users/', views.users_view, name='users'),

    # Generic O'chirish (Delete) URL
    path('delete/<str:model_name>/<int:item_id>/', views.delete_item, name='delete_item'),
]