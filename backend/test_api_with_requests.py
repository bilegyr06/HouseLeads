import requests

data_json = {
    "email": 'ayodejioluwatt@gmail.com',
    "full_name": "Emilokan Badmos",
    "phone_number": "07085860165",
    "location_area": 'VI'
}

path_base = 'http://127.0.0.1:8000'
api_prefix = '/api/v1'
route = '/agent'
action = '/'
res = requests.post(f'{path_base}{api_prefix}{route}{action}')