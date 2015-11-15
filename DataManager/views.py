from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from DataManager.dto import AnalyzeResult
from DataManager.models import Airline, Country, City
from DataManager.serializers import CountrySerializer, AirlineSerializer, AnalyzeRequestSerializer, \
    AnalyzeResultSerializer, CitySerializer
from DataManager.textmatcher.DescriptionAnalyzer import DescriptionAnalyzer
from DataManager.textmatcher.TextMatcher import TextMatcher

# Create your views here.
description_analyzer = DescriptionAnalyzer()
word_matcher = TextMatcher()

@api_view(['POST'])
def analyze(request):
    request_serializer = AnalyzeRequestSerializer(data=request.data)
    if request_serializer.is_valid():
        analyze_request = request_serializer.save()
        cities, countries, airlines = description_analyzer.analyze(analyze_request.content)

        analyze_result = AnalyzeResult(cities, countries, airlines)
        response_serializer = AnalyzeResultSerializer(analyze_result)
        return Response(response_serializer.data)

    return Response(status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def countries(request, format=None):
    if request.method == 'GET':
        countries = Country.objects.all()
        serializer = CountrySerializer(countries, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def country(request, pk):
    try:
        result = Country.objects.get(pk=pk)
    except Country.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CountrySerializer(result)
    return Response(serializer.data)

# Airlines

@api_view(['GET'])
def airlines(request, format=None):
    if request.method == 'GET':
        entities = Airline.objects.all()
        serializer = AirlineSerializer(entities, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def airline(request, pk):
    try:
        result = Airline.objects.get(pk=pk)
    except Airline.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = AirlineSerializer(result)
    return Response(serializer.data)

# Cities

@api_view(['GET'])
def cities(request, format=None):
    if request.method == 'GET':
        entities = City.objects.all()
        serializer = CitySerializer(entities, many=True, context={'request': request})
        return Response(serializer.data)


@api_view(['GET'])
def city(request, pk):
    try:
        result = City.objects.get(pk=pk)
    except City.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = CitySerializer(result, context={'request': request})
    return Response(serializer.data)