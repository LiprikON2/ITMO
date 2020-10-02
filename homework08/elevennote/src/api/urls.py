from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework.routers import DefaultRouter

from .views import NoteViewSet, SearchView, share_note, SharedNoteView

app_name = 'api'

router = DefaultRouter(trailing_slash=False)
router.register(r'notes', NoteViewSet)


note_list = NoteViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
note_detail = NoteViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', include(router.urls)),
    path('jwt-auth/', obtain_jwt_token),
    path('notes/', note_list, name='note-list'),
    path('notes/<int:pk>/', note_detail, name='note-detail'),
    path('notes/search/', SearchView, name='note-search'),
    path('notes/share/<int:note_pk>', share_note, name='note-share'),
    path('notes/share/<slug:slug>', SharedNoteView, name='note-shared'),
]
