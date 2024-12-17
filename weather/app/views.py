from django.shortcuts import render
import requests
import datetime

def home(request):
    if 'city' in request.POST:
        city = request.POST['city']
    else:
        city = 'islambad'

    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=71d4c0146a588e83312d5b78d3382739'
    param = {"units": "metric"}  # Corrected parameter

    data = requests.get(url, params=param).json()
    
    # if data.get('cod') != 200:  # Check for error
    #     return render(request, 'error.html', {'message': 'Error fetching weather data'})
    des = data.get('weather', [{}])[0].get('description', 'No description available')
    icon = data.get('weather', [{}])[0].get('icon', 'No icon available')
    temp = data.get('main', {}).get('temp', 'No temperature data')
    rain = data.get('rain', 'No rain data')
    day = datetime.date.today()

    detail = {
        'Description': des,
        'icon': icon,
        'Temp': temp,
        'Day': day,
        'City':city,
        'Rain':rain
    }
    return render(request, "index.html", detail)
