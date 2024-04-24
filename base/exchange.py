from django.shortcuts import render
import requests

api_key = 'b7ff85d0b03d4e070f723655'
url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/USD'

def get_exchange_rate(request):
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
       
