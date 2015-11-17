from rest_framework import serializers
from DataManager.dto import AnalyzeResult, AnalyzeRequest, AnalyzedEntity, AnalyzedCountry
from DataManager.models import Country, Airline, City

__author__ = 'Magda'


class CountrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Country
        fields = ('name', 'forms')


class AirlineSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Airline
        fields = ('name', 'forms')


class CitySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = City
        fields = ('name', 'forms')
        country = serializers.HyperlinkedIdentityField(view_name = 'country')


# --- NON-MODEL SERIALIZERS ---


class AnalyzeRequestSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=1000, required=True)

    def update(self, instance, validated_data):
        instance.content = validated_data.get('content', instance.content)
        return instance

    def create(self, validated_data):
        return AnalyzeRequest(**validated_data)


# class AnalyzeEntitySerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=True)
#     base_form = serializers.CharField(max_length=100, required=True)
#     provided_form = serializers.CharField(max_length=100, required=True)
#
#     def update(self, instance, validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.base_form = validated_data.get('base_form', instance.base_form)
#         instance.provided_form = validated_data.get('provided_form', instance.provided_form)
#         return instance
#
#     def create(self, validated_data):
#         return AnalyzedEntity(**validated_data)
#
#
# class AnalyzeCountrySerializer(serializers.Serializer):
#     id = serializers.IntegerField(required=True)
#     country = serializers.IntegerField(required=True)
#     base_form = serializers.CharField(max_length=100, required=True)
#     provided_form = serializers.CharField(max_length=100, required=True)
#
#     def update(self, instance, validated_data):
#         instance.id = validated_data.get('id', instance.id)
#         instance.country = validated_data.get('country', instance.country)
#         instance.base_form = validated_data.get('base_form', instance.base_form)
#         instance.provided_form = validated_data.get('provided_form', instance.provided_form)
#         return instance
#
#     def create(self, validated_data):
#         return AnalyzedCountry(**validated_data)


class AnalyzeResultSerializer(serializers.Serializer):
    cities = serializers.ListField(required=True)
    countries = serializers.ListField(required=True)
    airlines = serializers.ListField(required=True)

    def update(self, instance, validated_data):
        instance.cities = validated_data.get('cities', instance.cities)
        instance.countries = validated_data.get('countries', instance.countries)
        instance.airlines = validated_data.get('airlines', instance.airlines)
        return instance

    def create(self, validated_data):
        return AnalyzeResult(**validated_data)

