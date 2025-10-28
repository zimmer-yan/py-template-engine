from unittest import TestCase

from py_template_engine.sub_engines.VariableTemplater import VariableTemplater
from py_template_engine.RenderError import RenderError

class TestVariableTemplater(TestCase):

    def test_variable_templating(self):
        """Test basic variable substitution."""
        template = "Hello {{name}}!"
        engine = VariableTemplater()
        result = engine.render(template, name="World")
        self.assertEqual(result, "Hello World!")

    def test_variable_templating_nested(self):
        """Test basic variable substitution."""
        template = "Hello {{user.name}}!"
        engine = VariableTemplater()
        result = engine.render(template, user={"name": "World"})
        self.assertEqual(result, "Hello World!")

    def test_variable_templating_whitespace(self):
        """Test basic variable substitution."""
        template = "Hello {{ name }}!"
        engine = VariableTemplater()
        result = engine.render(template, name="World")
        self.assertEqual(result, "Hello World!")

    def test_variable_templating_variable_not_set_raise(self):
        """Test variable not set."""
        template = "Hello {{name}}!"
        engine = VariableTemplater(raise_on_error=True)
        with self.assertRaises(RenderError, msg="Trying to insert variable name but could not find 'name'"):
            engine.render(template)

    def test_variable_templating_variable_not_set_nested_raise(self):
        """Test variable not set."""
        template = "Hello {{user.name}}!"
        engine = VariableTemplater(raise_on_error=True)
        with self.assertRaises(RenderError, msg="Trying to insert variable user.name but could not find 'user'"):
            engine.render(template)

    def test_variable_templating_variable_not_set_nested_value_raise(self):
        """Test variable not set."""
        template = "Hello {{user.name}}!"
        engine = VariableTemplater(raise_on_error=True)
        with self.assertRaises(RenderError, msg="Trying to insert variable user.name but could not find 'name'"):
            engine.render(template, user={})

    def test_variable_templating_variable_not_set_dont_raise(self):
        """Test variable not set."""
        template = "Hello {{name}}!"
        engine = VariableTemplater()
        result = engine.render(template)
        self.assertEqual(result, "Hello {{name}}!")

    def test_variable_templating_variable_not_set_nested_dont_raise(self):
        """Test variable not set."""
        template = "Hello {{user.name}}!"
        engine = VariableTemplater()
        result = engine.render(template, user={})
        self.assertEqual(result, "Hello {{user.name}}!")
