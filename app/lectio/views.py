from logging import exception
from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from lectioscraper import Lectio
# Create your views here.
def check_login(data):
    try:
        lecpass = data['password']
        lecuser = data['username']
        schoolid = data['schoolid']
    except KeyError:
        return False
    except Exception as e:
        return False
    if lecpass == '' or lecuser == '' or schoolid == '':
        return False
    lectio = Lectio(lecuser, lecpass, schoolid)
    studentnum = lectio.studentId
    if studentnum is not None:
        return lectio
    return False

def home(request):
    return JsonResponse({"hello": "world 2!!!"})


@csrf_exempt
def check_first_lecture_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    data = json.loads(request.body)
    lecclient = check_login(data)
    if lecclient is False:
        return JsonResponse({'error': 'Invalid credentials'})
    schedule = lecclient.getTodaysSchedule(to_json=False)
    if schedule == "No schedule found for today":
        return JsonResponse({'error': 'No schedule found for today!'})
    first_key = list(schedule.keys())[0]
    first_value = schedule[first_key]
    if first_value['Status'] == "Aflyst!":
        return JsonResponse({'first_lecture_status': 'Aflyst!'})
    elif first_value['Status'] == "Normal!":
        return JsonResponse({'first_lecture_status': 'Normal!'})
    elif first_value['Status'] == "Aendret!":
        return JsonResponse({'first_lecture_status': 'Aendret!'})
    else:
        return JsonResponse({'error': 'Unknown status'})
        

@csrf_exempt
def get_schedule(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    data = json.loads(request.body)
    lecclient = check_login(data)
    if lecclient is False:
        return JsonResponse({'error': 'Invalid credentials'})
    schedule = lecclient.getSchedule(to_json=False)
    # convert schedule from a list of dictionaries to a dictionary of dictionaries
    schedule_json = {}
    for i in schedule:
        schedule_json[i['Id']] = i
    return JsonResponse(schedule_json)

# git pull test

@csrf_exempt
def get_todays_schedule(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    data = json.loads(request.body)
    lecclient = check_login(data)
    if lecclient is False:
        return JsonResponse({'error': 'Invalid credentials'})
    schedule = lecclient.getTodaysSchedule(to_json=False)
    if schedule == "No schedule found for today":
        return JsonResponse({'error': 'No schedule found for today!'})
    return JsonResponse(schedule)