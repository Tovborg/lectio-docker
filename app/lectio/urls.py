from django.urls import path, include
from .views import *

namespace = 'lectio'

urlpatterns = [
    path('', home, name='home'),
]