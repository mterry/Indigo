from django.utils import unittest
from indigo import forms

class FormsTestCase(unittest.TestCase):
  def test_create_project_1(self):
    data = {
      "name": "Test name",
      "description": "Blah",
      "task_point_timescale": 2
    }

    form = forms.CreateProjectForm(data)
    self.assertTrue(form.is_valid())
    self.assertEquals(form["name"].errors, [])
    pass

  def test_create_project_2(self):
    data = {
      "name": "23r532tgfkes9jtbso4eitjouvse89mbut8oser9uhtb80ugveshmrb0hr9b0r,89ndubr9xut08xnr,-bds9mrth08rb,esg8tyrs0ehts name",
      "description": "Bla",
      "task_point_timescale": 2
    }

    form = forms.CreateProjectForm(data)
    self.assertFalse(form.is_valid())
    self.assertEquals(form["name"].errors, [u'Ensure this value has at most 50 characters (it has 112).'])
    pass

  def test_create_project_3(self):
    data = {
      "description": "Blah",
      "task_point_timescale": 2
    }

    form = forms.CreateProjectForm(data)
    self.assertFalse(form.is_valid())
    self.assertEquals(form["name"].errors, [u'This field is required.'])
    pass

  def test_create_iteration(self):
    pass

  def test_create_task(self):
    pass

  def test_modify_task(self):
    pass
