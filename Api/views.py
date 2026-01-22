from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from datetime import datetime
from Api.models import ErrorReport
from .serializers import StatusSerializer
from .serializers import ErrorSerializer
from rest_framework import status




@api_view(['GET'])
def get_server_status(request):
    return Response(StatusSerializer({
        'status': 'running',
        'date': datetime.now()
    }).data)
    
@api_view(['GET'])
def get_errors(request):
    errors = ErrorReport.objects.all()
    return Response(ErrorSerializer(errors, many=True).data)

@api_view(['GET'])
def get_error_from_code(request, code):
    error = ErrorReport.objects.get(code=code)
    return Response(ErrorSerializer(error).data)


@api_view(['POST'])
def create_error(request):
    serialized_error = ErrorSerializer(data=request.data)
    if serialized_error.is_valid():
        serialized_error.save()
        return Response(serialized_error.data, status=status.HTTP_201_CREATED)
    return Response(serialized_error.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT', 'DELETE'])
def object_update(request, id):
    try:
        obj = ErrorReport.objects.get(id=id)
    except ErrorReport.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = ErrorSerializer(obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)