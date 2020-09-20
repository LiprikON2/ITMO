from django.urls import path

from .views import NoteList, NoteDetail, NoteCreate, NoteUpdate, NoteDelete, SearchView, share_note, SharedNote

app_name = 'notes'

urlpatterns = [
    path('', NoteList.as_view(), name='index'),
    path('<int:pk>/detail', NoteDetail.as_view(), name='detail'),
    path('<int:pk>/', NoteUpdate.as_view(), name='update'),
    path('new/', NoteCreate.as_view(), name='create'),
    path('<int:pk>/delete/', NoteDelete.as_view(), name='delete'),
    path('search/', SearchView, name='search'),
    path('share/<int:note_pk>', share_note, name='share'),
    path('shared/<slug:slug>', SharedNote.as_view(), name='shared'),
]
