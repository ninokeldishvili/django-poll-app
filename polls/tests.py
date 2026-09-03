import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question
# Create your tests here.

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days= days)
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
        is in longer than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1)
        past_question = Question(pub_date=time)
        self.assertIs(past_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ If not questions exist, an appropriate message should be displayed. """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'], [])

    def test_past_questions(self):
        """ Questions with a pub_date in the past should be displayed. """
        question = create_question("Past question", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_future_questions(self):
        """ Questions with a pub_date in the future should be not be displayed. """
        create_question("Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available")
        self.assertQuerySetEqual(response.context['latest_question_list'],[])

    def test_future_question_and_past_question(self):
        """ Even if both past and future questions exist, only past questions
        are displayed. """
        question = create_question("Past question", days=-30)
        create_question(question_text="Future question", days=30)

        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question])

    def test_two_past_questions(self):
        """ The questions index page may display multiple questions."""
        question1 = create_question("Past question 1", days=-30)
        question2 = create_question("Past question 2", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerySetEqual(response.context['latest_question_list'], [question2, question1])




