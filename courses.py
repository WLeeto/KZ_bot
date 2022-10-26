import requests
from pprint import pprint

# https://www.cbr-xml-daily.ru/daily.xml

def _get_courses():
    response = 'https://www.cbr-xml-daily.ru/daily_json.js'
    resp_get = requests.get(response)
    return resp_get.json()

def course_KZT():
    return 100 / _get_courses()['Valute']['KZT']['Value']

if __name__ == "__main__":

    pprint(course_KZT())
