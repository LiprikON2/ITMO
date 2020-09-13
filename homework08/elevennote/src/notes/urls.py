from django.urls import path

from .views import NoteList, NoteDetail, NoteCreate, NoteUpdate, NoteDelete, NoteTagList

app_name = 'notes'

urlpatterns = [
    path('', NoteList.as_view(), name='index'),
    path('<int:pk>/detail', NoteDetail.as_view(), name='detail'),
    path('<int:pk>/', NoteUpdate.as_view(), name='update'),
    # path('tag/<slug:slug>/', NoteTagList.as_view(), name='tags'),
    path('tag/<slug:slug>/', NoteTagList, name='tags'),
    path('new/', NoteCreate.as_view(), name='create'),
    path('<int:pk>/delete/', NoteDelete.as_view(), name='delete'),
]
