# -*- coding: utf-8 -*-
import re
from DataManager.dto import AnalyzedCity, AnalyzedCountry, AnalyzedEntity
from DataManager.models import Country, City, Airline
from DataManager.textmatcher.TextMatcher import TextMatcher

__author__ = 'Magda'


CITY_KEY = 'city'
AIRLINE_KEY = 'airline'
COUNTRY_KEY = 'country'


class DescriptionAnalyzer:

    def __init__(self):
        self.ignored_characters = r"[\.:;!?()\\/0-9\"\-\'+]"
        self.split_on = ","
        # self.names_regex = re.compile(r"((?:[A-Z][\w]+\s*){1,4})")
        self.names_regex = re.compile(r"((?:\b[A-ZŁĄĘĆŚŃŻŹ][\w]+\b\s*){1,4})")
        self.stop_words = []
        self.word_matcher = TextMatcher()

        with open('data/stopwords.txt', encoding='utf-8') as f:
            lines = f.readlines()
            self.stop_words = lines[0].split(', ')

        # words after would most likely contain interesting to us data (up until '.' or ';')
        self.key_words = [ "z", "do", "linii", "linie" ]


    def get_naive_match(self, form):
        city = self.word_matcher.get_naive_match(form, City.objects.all())
        if city is not None:
            return CITY_KEY, city

        country = self.word_matcher.get_naive_match(form, Country.objects.all())
        if country is not None:
            return COUNTRY_KEY, country

        airline = self.word_matcher.get_naive_match(form, Airline.objects.all())
        if airline is not None:
            return AIRLINE_KEY, airline

    def get_existing_form_match(self, form):
        city = self.word_matcher.get_base_form_combined(form, City.objects.all(), City.objects)
        if city is not None:
            return CITY_KEY, city

        country = self.word_matcher.get_base_form_combined(form, Country.objects.all(), Country.objects)
        if country is not None:
            return COUNTRY_KEY, country

        airline = self.word_matcher.get_base_form_combined(form, Airline.objects.all(), Airline.objects)
        if airline is not None:
            return AIRLINE_KEY, airline

    def get_base_form(self, form):
        city = self.word_matcher.get_base_form_combined(form, City.objects.all(), City.objects)
        if city is not None:
            return CITY_KEY, city

        country = self.word_matcher.get_base_form_combined(form, Country.objects.all(), Country.objects)
        if country is not None:
            return COUNTRY_KEY, country

        airline = self.word_matcher.get_base_form_combined(form, Airline.objects.all(), Airline.objects)
        if airline is not None:
            return AIRLINE_KEY, airline

    def create_result(self, form, entity_type, entity):
        if entity_type == CITY_KEY:
            return AnalyzedCity(entity.id, entity.country.id, entity.name, form).get_dict()
        elif entity_type == COUNTRY_KEY:
            return AnalyzedCountry(entity.id, entity.name, form).get_dict()
        elif entity_type == AIRLINE_KEY:
            return AnalyzedEntity(entity.id, entity.name, form).get_dict()

    def analyze(self, description):
        forms = self.names_regex.findall(description)
        print(forms)
        forms = map(lambda x: re.sub(self.ignored_characters, " ", x).strip(), forms)
        print(forms)
        forms = [ ' '.join(filter(lambda x: x.lower() not in self.stop_words, form.split())) for form in forms ]
        forms = filter(lambda x: len(x) > 0, forms)
        forms = set(forms)
        print(forms)

        cities, countries, airlines = dict(), dict(), dict()

        for form in forms:
            found_match = False

            if not found_match:
                city = self.word_matcher.get_base_form_combined(form, City.objects.all(), City.objects)
                if city is not None:
                    cities[city.name] = AnalyzedCity(city.id, city.country.id, city.name, form).get_dict()
                    found_match = True

            if not found_match:
                country = self.word_matcher.get_base_form_combined(form, Country.objects.all(), Country.objects)
                if country is not None:
                    countries[country.name] = AnalyzedCountry(country.id, country.name, form).get_dict()
                    found_match = True

            if not found_match:
                airline = self.word_matcher.get_base_form_combined(form, Airline.objects.all(), Airline.objects)
                if airline is not None:
                    airlines[airline.name] = AnalyzedEntity(airline.id, airline.name, form).get_dict()
                    found_match = True


        return cities.values(), countries.values(), airlines.values()
