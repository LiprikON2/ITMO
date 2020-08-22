from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import *


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    template = loader.get_template('index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def my_own_page(request):
    return HttpResponse('<h1> HI </h1><br> im Mike')


def detail(request, question_id):
    return HttpResponse(f"""You're looking at question {question_id}.
    <h1>{Question.objects.get(pk=question_id)}
    """)


def results(request, question_id):

    print(request.headers)
    print(dir(request))

    choices = Question.objects.get(pk=question_id).choice_set.all()

    choice_html = ''
    for index, choice in enumerate(choices):
        choice_html += f'\n<h2>{index + 1}. {choice}</h2>'

    response = f"""You're looking at the results of question {question_id}.
    <h1>{Question.objects.get(pk=question_id)}<h1>
    {choice_html}
    """

    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
