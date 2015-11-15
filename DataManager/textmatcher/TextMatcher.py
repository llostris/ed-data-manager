# -*- coding: utf-8 -*-
from DataManager.models import Country, Airline, City

__author__ = 'Magda'


class TextMatcher():

    def __init__(self):
        self.use_levenshtein = True
        self.base_treshold = 2
        self.treshold = 2
        self.minimum_exact_match = 3

    def levenshtein_distance(self, text1, text2) :
        tab = [ [0 for _ in range(len(text1) + 1)] for _ in range(len(text2) + 1)]
        text1 = text1.lower()
        text2 = text2.lower()

        for i in range(len(text2)) :
            tab[i][0] = i
        for i in range(len(text1)) :
            tab[0][i] = i

        # print(tab)
        for j in range(1, len(text1), 1) :
            for i in range(1, len(text2), 1) :
                if text1[j] == text2[i] :
                    cost = 0
                else :
                    cost = 1
                tab[i][j] = min(tab[i - 1][j] + 1,
                                tab[i][j - 1] + 1,
                                tab[i - 1][j - 1] + cost
                                )
        return tab[len(text2) - 1][len(text1) - 1]

    def use_database_only(self):
        self.use_levenshtein = False

    def use_calculation_mode(self):
        self.use_levenshtein = True

    def match_words(self, word1, word2):
        if self.use_levenshtein:
            distance = self.levenshtein_distance(word1, word2)
            treshold = self.treshold
            length = len(word1.split()) - 1
            treshold += 2 * length # accommodate for longer forms having more space for differences from base form
            if distance <= treshold:
                return True
        return False

    def get_naive_match(self, provided_form, objects):
        """
        Checks if object in given base form exists in database; if yes, returns this object as a match.
        """
        try:
            form = objects.get(name=provided_form)
            return form
        except (Country.DoesNotExist, City.DoesNotExist, Airline.DoesNotExist):
            pass
        return None

    def get_existing_form_match(self, provided_form, forms_to_match, objects):
        """
        Check if provided form matches any of derivative forms in objects; if yes, return corresponding object as a
        match.
        """
        for entity in forms_to_match:
            forms = [ x.strip() for x in entity.forms.split(",") ]
            if provided_form in forms:
                return entity
        return None

    def get_base_form(self, provided_form, forms_to_match, objects):
        """
        Use Levenshtein distance do match provided form to an entity.
        """
        skipped_on_first_run = []

        for entity in forms_to_match:
            base_form = None
            if not base_form:
                if self.is_possible_match(provided_form, entity.name):
                    if self.match_words(provided_form, entity.name):
                        base_form = entity.name
                        # self.update_forms(entity, provided_form)
                elif self.is_possible_match(provided_form, entity.name, secondary=True):
                        skipped_on_first_run.append(entity)

            if base_form:
                print('FOUND: ' + entity.name)
                return entity

        return self.run_secondary_matching(provided_form, skipped_on_first_run)

    def get_base_form_combined(self, provided_form, forms_to_match, objects, treshold=2):
        self.treshold = treshold

        # naively try to grab an object for provided form
        try:
            form = objects.get(name=provided_form)
            return form
        except (Country.DoesNotExist, City.DoesNotExist, Airline.DoesNotExist):
            pass

        skipped_on_first_run = []

        for entity in forms_to_match:
            forms = [ x.strip() for x in entity.forms.split(",") ]
            base_form = None

            if provided_form in forms:
                base_form = entity.name

            if not base_form:
                if self.is_possible_match(provided_form, entity.name):
                    if self.match_words(provided_form, entity.name):
                        base_form = entity.name
                        # self.update_forms(entity, provided_form)
                elif self.is_possible_match(provided_form, entity.name, secondary=True):
                        skipped_on_first_run.append(entity)

            if base_form:
                print('FOUND: ' + entity.name)
                return entity

        return self.run_secondary_matching(provided_form, skipped_on_first_run)

    def is_possible_match(self, provided_form, base_form, secondary=False):
        """
        Returns True if a word is considered a valid option for matching, i.e. it has at least 3 start characters
        the same as the base form and has the same amount of words.
        """
        minimum_for_exact_match = self.minimum_exact_match - secondary
        return provided_form[:minimum_for_exact_match] == base_form[:minimum_for_exact_match] \
            and len(provided_form.split()) == len(base_form.split())

    def run_secondary_matching(self, provided_form, skipped_entities):
        """
        Find a match among entities that were discarded on the first run (they are less likely to be a
        right match).
        """
        for entity in skipped_entities:
            if self.match_words(provided_form, entity.name):
                print('FOUND (SECONDARY): ' + entity.name)
                return entity

    def update_forms(self, entity, provided_form):
        entity.forms += ',' + provided_form
        entity.save()
