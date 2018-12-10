# encoding=utf8
import json
from urllib.parse import urlencode
from urllib.request import urlopen

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class Search:
    API_KEY = 'AIzaSyAPjFl1yYCGsN0iSOJiVSWxNj1vnSjRq_M'

    def __init__(self, place):
        self.__head = None
        self.place = place

    def append(self, place):
        if self.__head == None:
            self.__head = Node(place)
        else:
            temp = self.__head
            while temp.next is not None:
                temp = temp.next

            new_place = Node(place)
            temp.next = new_place

    def PlaceData(self, place):
        while True:
            url = urlopen('https://maps.googleapis.com/maps/api/place/textsearch/json?query=yerevan+{}&key={}'.format(place, self.API_KEY))
            data = json.load(url)
            if data['status'] == 'ZERO_RESULTS' or place == '':
                search = ''.join(input('Something went wrong, try again ').split())
            else:
                break
        return data, place

    def PlaceId(self, data):
        result = data.get('results')
        places_id = []
        for elem in result:
            place_id = elem['place_id']
            places_id.append(place_id)
        return places_id

    def PlaceDetails(self, places_id):
        details = []

        for i in range(len(places_id)):
            url = urlopen('https://maps.googleapis.com/maps/api/place/details/json?placeid={}&key={}'.format(places_id[i], self.API_KEY))
            data = json.load(url)

            result = data.get('result')
            print('The phone number of ' + result['name'] + ' is ' + result['international_phone_number'])
            print('The address of ' + result['name'] + ' is ' + result['formatted_address'])
            print()
            details.append(result['international_phone_number'])
            details.append(result['formatted_address'])
            for i in result['reviews']:
                print (i['author_name'] + "'s feedback is: " + i['text'] + " And rating is " + str(i["rating"]))
                print()
            print ('Overall rating is ' + str(result['rating']))

        return details

    def Weather(self):
        user_answer = input('Want to know weather in Yerevan? ').lower()
        if user_answer == 'yes':
            url = "https://query.yahooapis.com/v1/public/yql?"
            yql_query = "select item.condition from weather.forecast where woeid = 2214662 and u = 'Unit.CELSIUS'"
            yql_url = url + urlencode({'q': yql_query}) + "&format=json"
            result = urlopen(yql_url).read()
            data = json.loads(result)

            temp = data['query']['results']['channel']['item']['condition']['temp']
            condition =  data['query']['results']['channel']['item']['condition']['text']
            if condition == 'Showers':
                print ("Looks like it's going to rain today, the temperature is " + temp + u'°C')
            elif condition == 'Cloudy':
                print ("It's cloudy today, the temperature is " + temp + u'°C')
            elif condition == 'Scattered Thunderstorms':
                print ("Better to stay at home it's storming, the temperature is " + temp + u'°C')
            elif condition == 'Sunny':
                print ("It's sunny today, the temperature is " + temp + u'°C')
            else:
                print ("The temperature is " + temp + u'°C' + " Have a great day!")
        else:
            print ('Have a great day!')

    def search(self, search_place):
        data, place = self.PlaceData(search_place)
        places_id = self.PlaceId(data)
        details = self.PlaceDetails(places_id)
        self.Weather()

        return details

def main():
    search = ''.join(input('Please, input the name of place you want to search ').split())
    place_search = Search(search)
    details = place_search.search(place_search.place)
    place_search.append(search)
    place_search.append(details[0])
    place_search.append(details[1])
    print()

main()