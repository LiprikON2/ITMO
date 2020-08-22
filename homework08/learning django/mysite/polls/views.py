from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.template import loader

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return render(request, 'index.html', context)


def my_own_page(request):
    return HttpResponse('<h1> HI </h1><br> im Mike')


def detail(request, question_id):
    return HttpResponse(f"""You're looking at question {question_id}.
    <h1>{Question.objects.get(pk=question_id)}
    """)


def results(request, question_id):

    # try:
    #     choices = Question.objects.get(pk=question_id).choice_set.all()
    # except Question.DoesNotExist:
    #     raise Http404('Question doesn\'t exists')

    choices = get_object_or_404(Question, pk=question_id).choice_set.all()

    context = {
        'question': Question.objects.get(pk=question_id),
        'choices': choices
    }
    return render(request, 'results.html', context)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
