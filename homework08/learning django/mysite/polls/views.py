from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.db.models import F
from django.views import generic

from .models import *

import logging
logger = logging.getLogger(__name__)


# generic.ListView - Display a list of objects
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        queryset = []
        for question in Question.objects.order_by('-pub_date'):
            if question.was_published_recently():
                queryset.append(question)
        return queryset

# generic.DetailView - Display a detail page for a particular type of object
class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'
    

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    # Equivalent to
    #
    #   selected_choice.votes += 1
    #
    # but it aslo avoids racing conditions
    # ref: https://docs.djangoproject.com/en/3.1/ref/models/expressions/#avoiding-race-conditions-using-f
    selected_choice.votes = F('votes') + 1
    
    selected_choice.save()
    
    # After using F() variable becomes F(votes) + Value(1)
    # Refreshing makes variable accessible once again 
    selected_choice.refresh_from_db()
    
    return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))



