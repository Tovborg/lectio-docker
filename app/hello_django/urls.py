from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from lectio.views import *


urlpatterns = [
    path('api/first_lecture_status/', check_first_lecture_status,
         name='first_lecture_status'),
    path('api/get_schedule/', get_schedule, name='get_schedule'),
    path('api/get_todays_schedule/', get_todays_schedule,
         name='get_todays_schedule'),
    path('admin/', admin.site.urls),
    path('', home, name='home'),
]

if bool(settings.DEBUG):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
