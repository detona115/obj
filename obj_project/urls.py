
from django.contrib import admin
from django.urls import path, include
from bank.api import urls

urlpatterns = [
    path('admin/', admin.site.urls),
] + urls.urlpatterns
