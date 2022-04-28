from django.test import TestCase

from todo_app.models import ToDoList


class ToDoListModelTest(TestCase):
	def setUpTestData(cls):
		return True