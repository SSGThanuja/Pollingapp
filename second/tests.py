# -*- coding: utf-8 -*-
from __future__ import unicode_literals



# Create your tests here.

import datetime

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase

from .models import Question

class QuestionMethodTests(TestCase):

	def test_was_published_recently_old_question(self):

		"""this func returns False for questions 
		which published older than 1 day"""

		time = timezone.now() + datetime.timedelta(days=30)
		old_question = Question(pub_date=time)
		self.assertIs(old_question.was_published_recently(), False)

	def test_was_published_recently_recent_question(self):

		"""this func returns True for questions
		which published within last day"""

		time = timezone.now()- datetime.timedelta(hours=1)
		recent_question = Question(pub_date=time)
		self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):

		"""Creates a question with the given `question_text` and published the
    		given number of `days` offset to now (negative for questions published
    		in the past, positive for questions that have yet to be published)."""

	time = timezone.now() + datetime.timedelta(days=days)
		
	return Question.objects.create(question_text = question_text, pub_date = time)


class QuestionViewTests(TestCase):

	def test_index_view_with_no_questions(self):

		"""If no ques then display message"""

		response = self.client.get(reverse('second/index'))
		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "No polls are available")

self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_a_past_question(self):

		"""displaying the questions that are published
			in the past on index page"""

		create_question(question_text = "Past question", days = -30)
		response = self.client.get(reverse('second:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])	

	def test_index_view_with_a_future_question(self):

		"""not displaying the future ques in the index page"""

		create_question(question_text = "Future question", days = 30)
		response = self.client.get(reverse('second:index'))
		self.assertContains(response, "No polls are available")

self.assertQuerysetEqual(response.context['latest_question_list'], [])

	def test_index_view_with_future_and_past_question(self):

		"""if past and future questions exist, 
		then display only past ques"""

		create_question(question_text = "Past question", days= -30)
		create_question(question_text = "Future question", days = 30)
		response = self.client.get(reverse('second:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: Past question>'])

	def test_index_view_with_two_past_questions(self):

		"""displaying the multiple 
			past quetions on index page"""

		create_question(question_text = "Past question 1:", days =-30)
		create_question(question_text = "Past question 2:", days = -5)

		response = self.client.get(reverse('second:index'))
		self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question:Past question 2>'], '<Question:Past question 1>')

	
#for detailView tests

class QuestionIndexDetailTests(TestCase):

	def test_detail_view_with_a_future_question(self):

		"""returning the future ques pub date
			as 404 error"""

		future_question = create_question(question_text = "Future question", days = 5)
		url = reverse('second:details', args = (future_question.id,))
		response = self.client.get(url)
		self.assertEqual(response.status_code, 404)

	def test_detail_view_with_a_past_question(self):

		"""pub date in the past should display in the 
			question_text"""

		past_question = create_question(question_text = "Past question", days = -5)
		url = reverse('second:details', args = (past_question.id,))
		response = self.client.get(url)
		self.assertContains(response, past_question.question_text)