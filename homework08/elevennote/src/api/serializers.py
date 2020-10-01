from rest_framework import serializers
from taggit_serializer.serializers import (TagListSerializerField, TaggitSerializer)

from notes.models import Note, Permalink


class NoteSerializer(TaggitSerializer, serializers.ModelSerializer):

    tags = TagListSerializerField()

    class Meta:
        model = Note
        fields = ('id', 'title', 'tags', 'body', 'pub_date')
        

class PermalinkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Permalink
        fields = ('key', 'refersTo')
