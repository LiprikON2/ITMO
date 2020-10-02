from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
import json
# For sharing notes
import hashlib
from django.http import JsonResponse


from notes.models import Note, Permalink
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


@api_view(['POST'])
def share_note(request, note_pk):
    note = get_object_or_404(Note, owner=request.user, pk=note_pk)
    share_key = hashlib.md5(note.title.encode('utf-8')).hexdigest()[:8]
    permalink = Permalink(key=share_key, refersTo=note)
    permalink.save()
    response = {
        'share_key': share_key,
    }
    return JsonResponse(response)


@api_view(['GET'])
def SharedNoteView(request, slug):
    note = get_object_or_404(Permalink, key=slug).refersTo
    serializer = NoteSerializer(note)
    return Response(serializer.data)
