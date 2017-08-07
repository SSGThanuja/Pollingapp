# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from django.template import loader
from django.views import generic
from .models import Question, Choice

# Create your views her9e.

"""def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'second/index.html', context)"""

class IndexView(generic.ListView):
	
	template_name = 'second/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):

		"""returning the last 5 published ques (not includeing
			those set in the future)
		"""
		
		return Question.objects.filter(pub_date__lte = timezone.now()).order_by('-pub_date')[:5]

"""def details(request, question_id):

	question = get_object_or_404(Question, pk = question_id)

	return render(request, 'second/detail.html', {'question' : question})"""

class  DetailView(generic.DetailView):
	model = Question

	template_name = 'second/detail.html'

	def get_queryset(self):
		#not displaying the ques that arent published yet

		return Question.objects.filter(pub_date__lte = timezone.now())


"""def results(request, question_id):

	question = get_object_or_404(Question, pk = question_id)


	return render(request, 'second/results.html', {'question': question})"""

class ResultsView(generic.DetailView):
	model = Question

	template_name = 'second/results.html'

def votes(request, question_id):

	question = get_object_or_404(Question, pk = question_id)

	try:
		select_choice = question.choice_set.get(pk = request.POST['choice'])

	except (KeyError, Choice.DoesNotExist):

		return render(request, 'second/detail.html', {
			'question' : question,
			'error_message' : "You didn't select choice. Please select a choice",
			})

	else:

		select_choice.votes += 1
		select_choice.save()

		return HttpResponseRedirect(reverse('second:results', args=(question_id,)))

	return HttpResponse("You are voting on the question %s." %question_id)