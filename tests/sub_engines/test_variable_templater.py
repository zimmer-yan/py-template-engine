from unittest import TestCase

from py_template_engine.sub_engines.VariableTemplater import VariableTemplater


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
