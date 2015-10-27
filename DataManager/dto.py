__author__ = 'Magda'


class AnalyzeRequest:

    def __init__(self, content):
        self.content = content


class AnalyzeResult:

    def __init__(self, cities, countries, airlines):
        self.cities = cities
        self.countries = countries
        self.airlines = airlines


class AnalyzedEntity:

    def __init__(self, id, base_form, provided_form):
        self.id = id
        self.base_form = base_form
        self.provided_form = provided_form

    def get_dict(self):
        return {
            "id" : self.id,
            "base_form" : self.base_form,
            "provided_form" : self.provided_form
        }


class AnalyzedCity(AnalyzedEntity):

    def __init__(self, id, country_id, base_form, provided_form) :
        super().__init__(id, base_form, provided_form)
        self.country_id = country_id

    def get_dict(self):
        dictionary = super().get_dict()
        dictionary["country_id"] = self.country_id
        return dictionary


class AnalyzedCountry(AnalyzedEntity):

    def __init__(self, id, base_form, provided_form):
        super().__init__(id, base_form, provided_form)



