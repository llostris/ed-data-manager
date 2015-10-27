import re
from DataManager.dto import AnalyzedCity, AnalyzedCountry, AnalyzedEntity
from DataManager.models import Country, City, Airline
from DataManager.textmatcher.TextMatcher import TextMatcher

__author__ = 'Magda'


class DescriptionAnalyzer:

    def __init__(self):
        self.ignored_characters = r"[\.,:;!?()\\/0-9\"\-\'+]"
        self.stop_words = []
        self.word_matcher = TextMatcher()

        with open('data/stopwords.txt', encoding='utf-8') as f:
            lines = f.readlines()
            self.stop_words = lines[0].split(', ')

        # words after would most likely contain interesting to us data (up until '.' or ';')
        self.key_words = [ "z", "do", "linii", "linie" ]

    def analyze(self, description):
        description = re.sub(self.ignored_characters, " ", description)
        words = description.split()
        words = filter(lambda x: x.lower() not in self.stop_words, words)
        words = filter(lambda x: x[0].isupper(), words)

        cities, countries, airlines = [], [], []

        for word in list(words):
            found_match = False

            if not found_match:
                country = self.word_matcher.get_base_form(word, Country.objects.all(), Country.objects)
                if country is not None:
                    countries.append(AnalyzedCountry(country.id, country.name, word).get_dict())
                    found_match = True

            if not found_match:
                airline = self.word_matcher.get_base_form(word, Airline.objects.all(), Airline.objects)
                if airline is not None:
                    airlines.append(AnalyzedEntity(airline.id, airline.name, word).get_dict())

            if not found_match:
                city = self.word_matcher.get_base_form(word, City.objects.all(), City.objects)
                if city is not None:
                    cities.append(AnalyzedCity(city.id, city.country.id, city.name, word).get_dict())


        return cities, countries, airlines
