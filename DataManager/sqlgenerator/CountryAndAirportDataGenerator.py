__author__ = 'Magda'

import csv

AIRPORTS = []
COUNTRIES = []
CITY_NAMES = set()

INSERT_SQL = 'INSERT INTO {} VALUES({});\n'

class Country:
    def __init__(self, name, code):
        self.name = name
        self.code = code

    def print(self):
        return self.name + " " + self.code


class AirportCity:
    def __init__(self, city, country):
        self.city = city
        self.country = country

        if "'" in self.city:
            self.city = self.city.replace("'", "''")

    def __repr__(self):
        return "%s %s" % (self.city,self.country)

    def __eq__(self, other):
        return self.city, self.country == other.city, other.country

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash((self.city, self.country))

    def print(self):
        return self.city + " " + self.country #+ " " + self.iata + " "+ self.icao + " " + self.name


if __name__ == "__main__":

    # with open('../../data/countries.csv', 'r', encoding="UTF-8") as csvfile:
    #     country_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    #     for row in country_reader:
    #         print(', '.join(row))
    #         country = Country(row[2], row[1])
    #         print(country.print())
    #         COUNTRIES.append(country)


    with open('../../data/airports2.csv', 'r', encoding="UTF-8") as csvfile:
        airport_reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in airport_reader:
            print(', '.join(row))
            # airport = AirportCity(row[2], row[3], row[4], row[5], row[1])
            airport = AirportCity(row[2], row[3])
            print(airport.print())
            if airport.city not in CITY_NAMES:
                AIRPORTS.append(airport)
                CITY_NAMES.add(airport.city)

    countries = set([airport.country for airport in AIRPORTS])
    AIRPORTS = set(AIRPORTS)
    print(countries)

    with open('../../DataManager/sql/country2.sql', 'w') as f:
        with open('../../DataManager/sql/country.sql', 'r', encoding='utf-8') as country_file:
            lines = "".join(country_file.readlines())
            for country in countries:
                if country not in lines:
                    f.write(INSERT_SQL.format("DataManager_country('name', 'forms')",
                                                "'" + country + "','" + country + "'"))

        f.close()

    with open('../../DataManager/sql/city.sql', 'w', encoding='utf-8') as f:
        for airport in AIRPORTS:
            f.write(INSERT_SQL.format("DataManager_city('name', 'forms', 'country_id')",
                                      "'" + airport.city + "'," +
                                      "'" + airport.city + "'," +
                                      "(SELECT ID FROM DataManager_country where name = '" + airport.country + "')"))