import boto3
import decimal
import json
import numpy as np

from boto3.dynamodb.conditions import Key, Attr
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    dynamo_response = get_dynamo_data()
    items = dynamo_response['Items']
    data = parse_data(items)

    return render(
        request,
        'weather/weather_data.html',
        {
            'title': 'NOAA Weather Data',
            'content': json.dumps(data)
        }
    )

# The highest and lowest temperatures recorded on Earth - needed to clean data.
def parse_data(items, lowest=-127.00, highest=134):

    data_pack = {}
    for item in items:
        locationyearmonth = str(item['LocationYearMonth'])
        arr = np.array(item['Tmps']).astype(np.float)
        filtered_arr = [ x for x in arr if lowest <= x <= highest ]
        av = np.average(filtered_arr)
        city_name, year_month = locationyearmonth.split('::')
        year, month = year_month.split("-")
        if city_name in data_pack:
            data_pack[city_name][year][month] = av
        else:
            data_pack[city_name] = { year : { month: av} }
    return data_pack

def get_dynamo_data():
    dynamodb = boto3.resource('dynamodb', region_name='us-west-2')
    table = dynamodb.Table('Weather')
    pe = 'LocationYearMonth, Tmps'
    response = table.scan(
        ProjectionExpression=pe,
        )
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=pe,
            ExclusiveStartKey=response['LastEvaluatedKey']
            )
    return response

