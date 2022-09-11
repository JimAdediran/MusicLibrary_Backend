from django.http import Http404

import songs
from .models import Song
from .serializers import SongSerializer
from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status

from songs import serializers

# Create your views here.
class SongList(APIView):

    def get(self, request):
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SongSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class SongDetail(APIView):

    def get_object(self, pk):
        try:
            return Song.objects.get(pk=pk)
        except Song.DoesNotExist:
            raise Http404
    
    def get(self, request, pk):
        song = self.get_object(pk)
        serializer = SongSerializer(song)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        song = self.get_object(pk)
        custom_response = {
            "Song Deleted": song.title
        }
        song.delete()
        return Response(custom_response, status=status.HTTP_200_OK)