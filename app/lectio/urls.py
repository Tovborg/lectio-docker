from django.urls import path, include
from lectio.views import *

namespace = 'lectio'

urlpatterns = [
    path('', home, name='home'),
]