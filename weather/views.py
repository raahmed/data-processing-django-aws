import json

from django.http import HttpResponse
from django.shortcuts import render
from weather.get_weather_data import get_weather_data


def home(request):

    return render(
        request,
        'weather/weather_data.html',
        {
            'title': 'NOAA Weather Data',
            'content': json.dumps(get_weather_data())
        }
    )
