from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, ListAPIView
from rest_framework.response import Response
from DataManager.dto import AnalyzeResult
from DataManager.models import Airline, Country
from DataManager.serializers import CountrySerializer, AirlineSerializer, AnalyzeRequestSerializer, \
    AnalyzeResultSerializer
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


@api_view(['GET'])
def countrym(request):
    params = request.query_params
    original_form = params['form']  # TODO: read an array from request.data

    countries = Country.objects.all()
    base_form = word_matcher.get_base_form(original_form, countries)
    data = { 'country' : base_form }

    if base_form:
        return Response(data=data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_404_NOT_FOUND)

# Airlines

class AirlineList(ListAPIView):
    model = Airline
    serializer_class = AirlineSerializer
    # permission_classes = [
    #     permissions.AllowAny
    # ]

    def get_queryset(self):
        queryset = super(AirlineList, self).get_queryset()
        return queryset.filter(author__username=self.kwargs.get('id'))


class AirlineDetail(RetrieveAPIView):
    model = Airline
    serializer_class = AirlineSerializer
    lookup_field = 'id'