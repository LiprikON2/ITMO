from django.urls import path

from .views import NoteList, NoteDetail, NoteCreate, NoteUpdate, NoteDelete, NoteTagDelete, SearchView

app_name = 'notes'

urlpatterns = [
    path('', NoteList.as_view(), name='index'),
    path('<int:pk>/detail', NoteDetail.as_view(), name='detail'),
    path('<int:pk>/', NoteUpdate.as_view(), name='update'),
    path('new/', NoteCreate.as_view(), name='create'),
    path('<int:pk>/delete/', NoteDelete.as_view(), name='note_delete'),
    path('<int:note_pk>/<slug:slug>/delete-tag', NoteTagDelete, name='tag_delete'),
    path('search/', SearchView, name='search'),
]
