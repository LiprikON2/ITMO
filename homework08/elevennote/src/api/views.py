from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# from django.shortcuts import get_object_or_404
import json

from notes.models import Note
from .serializers import NoteSerializer
from notes.views import normalize_query, get_query


class NoteViewSet(viewsets.ModelViewSet):
    serializer_class = NoteSerializer
    queryset = Note.objects.all()

    def filter_queryset(self, queryset):
        queryset = Note.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(['GET'])
def SearchView(request):
    query_string = ''
    if ('q' in request.GET) and request.GET['q'].strip():
        query_string = request.GET['q']
        entry_query = get_query(query_string, ['title', 'body', 'tags__name'])
        notes = Note.objects.filter(entry_query, owner=request.user).distinct().order_by('-pub_date')
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)
