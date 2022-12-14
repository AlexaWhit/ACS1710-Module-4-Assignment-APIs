import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file
# from geopy.geocoders import Nominatim


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.
    
    appid = os.getenv('API_KEY')
    city = request.args.get('city')
    units = request.args.get('units')
    API_URL = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&units={units}'
    print(API_URL)

    # params = {
    #      TODO: Enter query parameters here for the 'appid' (your api key),
    #     # the city, and the units (metric or imperial).
    #     # See the documentation here: https://openweathermap.org/current
    #     'appid': appid,
    #     'city': city,
    #     'units': units,
    # }

    result_json = requests.get(API_URL).json()

    # Uncomment the line below to see the results of the API call!
    pp.pprint(result_json)


    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.

    stringDate = (datetime.now()).strftime('%A, %B, %d, %Y')
   

    context = {
        'date': stringDate,
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': datetime.fromtimestamp(result_json['sys']['sunrise']),
        'sunset': datetime.fromtimestamp(result_json['sys']['sunset']),
        'units_letter': get_letter_for_units(units),
    }

    return render_template('results.html', **context)


@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    appid = os.getenv('API_KEY')
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')
    city1_data = compare_helper(city1, units)
    city2_data = compare_helper(city2, units)

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!


    stringDate = (datetime.now()).strftime('%A, %B, %d, %Y')

    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.

    first_city = {
        'date': stringDate,
        'city': city1_data['name'],
        'temp': city1_data['main']['temp'],
        'humidity': city1_data['main']['humidity'],
        'wind_speed': city1_data['wind']['speed'],
        'sunset': datetime.fromtimestamp(city1_data['sys']['sunset']),
        'units_letter': get_letter_for_units(units),
    }

    second_city = {
        'date': stringDate,
        'city': city2_data['name'],
        'temp': city2_data['main']['temp'],
        'humidity': city2_data['main']['humidity'],
        'wind_speed': city2_data['wind']['speed'],
        'sunset': datetime.fromtimestamp(city2_data['sys']['sunset']),
        'units_letter': get_letter_for_units(units),
    }

    context = {
        'first_city': first_city,
        'second_city': second_city,
    }

    return render_template('comparison_results.html', **context)

def compare_helper(city, units):
    appid = os.getenv('API_KEY')
    API_URL = (f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={appid}&units={units}')
    response = requests.get(API_URL).json()
    return response

if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
