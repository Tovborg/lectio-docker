from django.urls import path, include
from lectio.views import *

namespace = 'lectio'

urlpatterns = [
    path('api/first_lecture_status/', check_first_lecture_status,
         name='first_lecture_status'),
    path('api/get_schedule/', get_schedule, name='get_schedule'),
    path('api/get_todays_schedule/', get_todays_schedule,
         name='get_todays_schedule'),
    path('', home, name='home'),
]