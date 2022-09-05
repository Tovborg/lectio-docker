from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from lectioscraper import Lectio
# Create your views here.


@csrf_exempt
def check_first_lecture_status(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    else:
        # get data from request body
        data = json.loads(request.body)
        try:
            lecpass = data['password']
            lecuser = data['username']
            schoolid = data['schoolid']
        except KeyError:
            return JsonResponse({'error': 'Missing parameters'})

        if lecpass == '' or lecuser == '' or schoolid == '':
            return JsonResponse({'error': 'Missing parameters'})
        elif lecpass is None or lecuser is None or schoolid is None:
            return JsonResponse({'error': 'Missing parameters'})
        else:
            lectio = Lectio(lecuser, lecpass, schoolid)
            try:
                studentnum = lectio.studentId
                schedule = lectio.getTodaysSchedule(to_json=False)
                if schedule == "No schedule found for today":
                    return JsonResponse({'error': 'No schedule found for today!'})
                else:
                    # get the first key in the schedule dictionary
                    first_key = list(schedule.keys())[0]
                    # get the first value in the schedule dictionary
                    first_value = schedule[first_key]

                    if first_value['Status'] == "Aflyst!":
                        return JsonResponse({'first_lecture_status': 'Aflyst!'})
                    elif first_value['Status'] == "Normal!":
                        return JsonResponse({'first_lecture_status': 'Normal!'})
                    elif first_value['Status'] == "Aendret!":
                        return JsonResponse({'first_lecture_status': 'Aendret!'})
                    else:
                        return JsonResponse({'error': 'Unknown status'})

            except AttributeError:
                return JsonResponse({'error': 'Invalid credentials'})

            except Exception as e:
                return JsonResponse({'error': str(e)})


@csrf_exempt
def get_schedule(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    else:
        # get data from request body
        data = json.loads(request.body)
        try:
            lecpass = data['password']
            lecuser = data['username']
            schoolid = data['schoolid']
        except KeyError:
            return JsonResponse({'error': 'Missing parameters'})

        if lecpass == '' or lecuser == '' or schoolid == '':
            return JsonResponse({'error': 'Missing parameters'})
        elif lecpass is None or lecuser is None or schoolid is None:
            return JsonResponse({'error': 'Missing parameters'})
        else:
            lectio = Lectio(lecuser, lecpass, schoolid)
            try:
                studentnum = lectio.studentId
                if studentnum == "":
                    return JsonResponse({'error': 'couldn\'t find student number'})
                elif studentnum is None:
                    return JsonResponse({'error': 'Invalid credentials'})

                schedule = lectio.getSchedule(to_json=False)
                if schedule == "No schedule found for today":
                    return JsonResponse({'error': 'No schedule found for today!'})
                else:
                    # convert schedule from a list of dictionaries to a dictionary of dictionaries
                    schedule_json = {}
                    for i in schedule:
                        schedule_json[i['Id']] = i
                    return JsonResponse(schedule_json)
            except AttributeError:
                return JsonResponse({'error': 'Invalid credentials'})

            except Exception as e:
                return JsonResponse({'error': str(e)})


@csrf_exempt
def get_todays_schedule(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST requests are allowed'})
    else:
        data = json.loads(request.body)
        try:
            lecpass = data['password']
            lecuser = data['username']
            schoolid = data['schoolid']
        except KeyError:
            return JsonResponse({'error': 'Missing parameters for logon, include username, password and schoolid'})

        if lecpass == '' or lecuser == '' or schoolid == '':
            return JsonResponse({'error': 'All parameters are required and must be filled'})
        elif lecpass is None or lecuser is None or schoolid is None:
            return JsonResponse({'error': 'Missing parameters'})
        else:
            lectio = Lectio(lecuser, lecpass, schoolid)
            try:
                studentnum = lectio.studentId
                if studentnum == "":
                    return JsonResponse({'error': 'couldn\'t find student number'})
                elif studentnum is None:
                    return JsonResponse({'error': 'Invalid credentials'})

                schedule = lectio.getTodaysSchedule(to_json=False)
                if schedule == "No schedule found for today":
                    return JsonResponse({'error': 'No schedule found for today!'})
                else:
                    # convert schedule from a list of dictionaries to a dictionary of dictionaries

                    return JsonResponse(schedule)
            except AttributeError:
                return JsonResponse({'error': 'Invalid credentials'})

            except Exception as e:
                return JsonResponse({'error': str(e)})