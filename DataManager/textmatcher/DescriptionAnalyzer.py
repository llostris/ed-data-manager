# -*- coding: utf-8 -*-
import re
from DataManager.dto import AnalyzedCity, AnalyzedCountry, AnalyzedEntity
from DataManager.models import Country, City, Airline
from DataManager.textmatcher.TextMatcher import TextMatcher

__author__ = 'Magda'


CITY_KEY = 'city'
AIRLINE_KEY = 'airline'
COUNTRY_KEY = 'country'
NO_MATCH_KEY = 'none'


class DescriptionAnalyzer:

    def __init__(self):
        self.ignored_characters = r"[\.:;!?()\\/0-9\"\-\'+]"
        self.split_on = ","
        # self.names_regex = re.compile(r"((?:[A-Z][\w]+\s*){1,4})")
        self.names_regex = re.compile(r"((?:\b[A-ZŁĄĘĆŚŃŻŹ][\w]+\b\s*){1,4})")
        self.stop_words = []
        self.word_matcher = TextMatcher()


        self.cities = dict()
        self.countries = dict()
        self.airlines = dict()

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

        return None, None

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

        return None, None

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

        return None, None

    def save_result(self, form, entity_type, entity):
        if entity_type == CITY_KEY:
            self.cities[entity.name] = AnalyzedCity(entity.id, entity.country.id, entity.name, form).get_dict()
        elif entity_type == COUNTRY_KEY:
            self.countries[entity.name] = AnalyzedCountry(entity.id, entity.name, form).get_dict()
        elif entity_type == AIRLINE_KEY:
            self.airlines[entity.name] = AnalyzedEntity(entity.id, entity.name, form).get_dict()

    def analyze(self, description):
        forms = self.names_regex.findall(description)
        if 'easyJet' in description.split():
            forms.append('easyJet')
        print(forms)
        forms = map(lambda x: re.sub(self.ignored_characters, " ", x).strip(), forms)
        forms = [ ' '.join(filter(lambda x: x.lower() not in self.stop_words, form.split())) for form in forms ]
        forms = filter(lambda x: len(x) > 0, forms)
        forms = set(forms)
        print(forms)

        self.cities, self.countries, self.airlines = dict(), dict(), dict()

        for form in forms:
            found_match = False

            # self.analyze_simple(form)

            entity_key, entity = self.get_naive_match(form)
            if entity_key is not None:
                self.save_result(form, entity_key, entity)
                found_match = True

            if not found_match:
                entity_key, entity = self.get_existing_form_match(form)
                if entity_key is not None:
                    self.save_result(form, entity_key, entity)
                    found_match = True

            if not found_match:
                entity_key, entity = self.get_base_form(form)
                if entity_key is not None:
                    self.save_result(form, entity_key, entity)
                    found_match = True

        return self.cities.values(), self.countries.values(), self.airlines.values()

    def analyze_simple(self, form):
        """
        First, naive version of analyze.
        :param form:
        :return:
        """
        found_match = False

        if not found_match:
            city = self.word_matcher.get_base_form_combined(form, City.objects.all(), City.objects)
            if city is not None:
                self.cities[city.name] = AnalyzedCity(city.id, city.country.id, city.name, form).get_dict()
                found_match = True

        if not found_match:
            country = self.word_matcher.get_base_form_combined(form, Country.objects.all(), Country.objects)
            if country is not None:
                self.countries[country.name] = AnalyzedCountry(country.id, country.name, form).get_dict()
                found_match = True

        if not found_match:
            airline = self.word_matcher.get_base_form_combined(form, Airline.objects.all(), Airline.objects)
            if airline is not None:
                self.airlines[airline.name] = AnalyzedEntity(airline.id, airline.name, form).get_dict()
                found_match = True
