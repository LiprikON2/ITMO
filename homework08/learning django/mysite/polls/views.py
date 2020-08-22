from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.db.models import F

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'index.html', context)





def detail(request, question_id):

    choices = get_object_or_404(Question, pk=question_id).choice_set.all()

    context = {
        'question': Question.objects.get(pk=question_id),
    }
    return render(request, 'detail.html', context)


def vote(request, question_id):
     
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    # Equivalent to
    #
    # selected_choice.votes += 1
    #
    # but it aslo avoids racing conditions
    # ref: https://docs.djangoproject.com/en/3.1/ref/models/expressions/#avoiding-race-conditions-using-f
    selected_choice.votes = F('votes') + 1
    
    # After using F() variable becomes F(votes) + Value(1)
    # Refreshing makes variable accessible once again 
    selected_choice.refresh_from_db()
    
    selected_choice.save()
    
    return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))



def results(request, question_id):
    
    question = get_object_or_404(Question.objects, pk=question_id)
    
    context = {
        'question': question,
    }
    return render(request, 'result.html', context)
