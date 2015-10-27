from DataManager.models import Country, Airline, City

__author__ = 'Magda'


class TextMatcher():

    def __init__(self):
        self.use_levenshtein = True
        self.base_treshold = 2
        self.treshold = 2

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
            if distance <= self.treshold:
                return True
        return False

    def get_base_form(self, provided_form, forms_to_match, objects, treshold=2):
        self.treshold = treshold

        try:
            form = objects.get(name=provided_form)
            return form
        except (Country.DoesNotExist, City.DoesNotExist, Airline.DoesNotExist):
            pass

        for entity in forms_to_match:
            forms = entity.forms.split(",")
            base_form = None

            if provided_form in forms:
                base_form = entity.name

            if not base_form:
                if provided_form[0] == entity.name[0] and self.match_words(provided_form, entity.name):
                    base_form = entity.name
                    self.update_forms(entity, provided_form)

            if base_form:
                print('FOUND: ' + entity.name)
                return entity

        return None

    def update_forms(self, entity, provided_form):
        entity.forms += ',' + provided_form
        entity.save()