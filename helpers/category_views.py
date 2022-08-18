from django.http import Http404, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.
from store.models import Category
from store.serializers import CategorySerializer
from rest_framework import viewsets
from rest_framework.parsers import JSONParser
from django.contrib.auth.decorators import login_required


@login_required
@api_view(['GET','POST'])
def category_views(request):
    """
    LIST ALL CATEGORIES, OR CREATE A NEW CATEGORY
    """

    if request.method == 'GET':

        generic = Category.objects.all()

        serializer = CategorySerializer(generic, many=True)
        return Response(serializer.data)


    elif request.method == 'POST':
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET', 'PUT', 'PATCH', 'POST','DELETE'])
def category_view(request, pk):
    """
    UPDATE, GET OR DELETE A CATEGORY
    """
    try:
        generic = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':

        serializer = CategorySerializer(generic)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = CategorySerializer(generic, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)


    # using this to edit because JQUARY refuses to use PUT request to update

    elif request.method == 'POST' and pk:
        serializer = CategorySerializer(generic, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        if serializer.errors:
            print(serializer.errors)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'POST':
        serializer = CategorySerializer(generic, data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    
    
    elif request.method == 'PATCH':
        serializer = CategorySerializer(generic,
                                        data=request.data,
                                        partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        generic.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
