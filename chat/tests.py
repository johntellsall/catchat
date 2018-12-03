import datetime
import os

import pytest
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def database_missing():
    return hasattr(os.environ, "CI")  # TODO make CI have database & run tests


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


@pytest.mark.skipif(database_missing(), reason='requires database')
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)


@pytest.mark.skipif(database_missing(), reason='requires database')
class QuestionIndexViewTests(TestCase):
    @pytest.mark.skip("ignore for now")
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No chat are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], ["<Question: Past question.>"]
        )

    @pytest.mark.skip("ignore for now")
    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("index"))
        self.assertContains(response, "No chat are available.")
        self.assertQuerysetEqual(response.context["latest_question_list"], [])

    @pytest.mark.skip("ignore for now")
    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"], ["<Question: Past question.>"]
        )

    @pytest.mark.skip("ignore for now")
    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("index"))
        self.assertQuerysetEqual(
            response.context["latest_question_list"],
            ["<Question: Past question 2.>", "<Question: Past question 1.>"],
        )
