from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path('', views.IndexView, name='index'),
    path('<int:note_id>/', views.DetailView, name='detail'),
]