from django.test import TestCase

from todo_app.forms import JoinForm, LoginForm, TaskForm

class TaskFormTest(TestCase):

	def test_task_form_name_field(self):
		form = TaskForm()
		self.assertTrue(form.fields['name'].required == True and form.fields['name'] != "")