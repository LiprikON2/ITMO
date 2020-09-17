from django.urls import path

from .views import NoteList, NoteDetail, NoteCreate, NoteUpdate, NoteDelete, NoteTagDelete, SearchView, share_note, SharedNote

app_name = 'notes'

urlpatterns = [
    path('', NoteList.as_view(), name='index'),
    path('<int:pk>/detail', NoteDetail.as_view(), name='detail'),
    path('<int:pk>/', NoteUpdate.as_view(), name='update'),
    path('new/', NoteCreate.as_view(), name='create'),
    path('<int:pk>/delete/', NoteDelete.as_view(), name='note_delete'),
    path('<int:note_pk>/<slug:slug>/delete-tag', NoteTagDelete, name='tag_delete'),
    path('search/', SearchView, name='search'),
    path('share-note/<int:note_pk>', share_note, name='share_note'),
    path('shared/<slug:slug>', SharedNote.as_view(), name='shared'),
    # url("/(?P<key>[a-f0-9]{8})$", "view.that.redirects.to.permalink.refersTo"),
    
]
