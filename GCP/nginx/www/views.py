import decimal
import json
import numpy as np
import os
from google.cloud import datastore
from django.http import HttpResponse
from django.shortcuts import render

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/www/credentials.json"

def home(request):
    return HttpResponse("Hello, Django!")

# The highest and lowest temperatures recorded on Earth - needed to clean data.
def parse_data(items, lowest=-127.00, highest=134):
    data_pack = {}
    for item in items:
        arr = item["Temperature_List"]
        #arr = np.array(item['Temperate_List']).astype(np.int)
        filtered_arr = [ int(x) for x in arr if lowest <= int(x) <= highest ]
        av = np.average(filtered_arr)
        city_name = item["city"] + "_" + item["country"]
        year = item["Year"]
        month = item["Month"]
        if city_name in data_pack:
            data_pack[city_name][year][month] = av
        else:
            data_pack[city_name] = { year : { month: av} }
    return data_pack

def get_datastore_data():
    client = datastore.Client()
    query = client.query(kind='msft-compete')
    results = list(query.fetch())
    return results

def weather(request):
    datastore_data = get_datastore_data()
    data = parse_data(datastore_data)
    return render(
        request,
        'weather/weather_data.html',
        {
            'title': 'NOAA Weather Data',
            'content': json.dumps(data)
        }
    )
