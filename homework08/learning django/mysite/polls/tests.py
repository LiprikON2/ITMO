import datetime

from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
import datetime

from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)
        
    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)
       
       
class IndexViewTest(TestCase):
    def test_future_questions(self):
        """
        get_queryset() mustn't return questions whose date are in the future
        """
        
        create_question('Am I the past?', days=-0.6)
        create_question('Im the future... ?', days=300)
        response = self.client.get(reverse('polls:index'))
        
        now = timezone.now()
        latest_question = response.context['latest_question_list'][0]
        self.assertIs(latest_question.pub_date < now, True)
        self.assertIs(latest_question.was_published_recently(), True)
