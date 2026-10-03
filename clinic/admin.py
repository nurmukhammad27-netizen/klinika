from django.contrib import admin
from django.apps import apps

# Clinic ilovasidagi barcha mavjud modellarni dinamik ravishda olamiz
app_config = apps.get_app_config('clinic')

for model in app_config.get_models():
    try:
        # Har bir modelni Django admin panelga registratsiya qilamiz
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass