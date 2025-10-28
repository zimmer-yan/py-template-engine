from unittest import TestCase

from py_template_engine.sub_engines.FunctionTemplater import FunctionTemplater
from py_template_engine.RenderError import RenderError


class TestFunctionTemplater(TestCase):

    def test_function_templating(self):
        """Test basic function substitution."""
        template = "Hello, {{get_time()}}!"
        engine = FunctionTemplater()
        result = engine.render(template, get_time=lambda: "12:00 PM")
        self.assertEqual(result, "Hello, 12:00 PM!")

    def test_function_templating_nested(self):
        """Test basic function substitution."""
        template = "Hello, {{user.get_time()}}!"
        engine = FunctionTemplater()
        result = engine.render(template, user={"get_time": lambda: "12:00 PM"})
        self.assertEqual(result, "Hello, 12:00 PM!")

    def test_function_templating_missing_variable_no_raise(self):
        """Test function substitution with missing variable."""
        template = "Hello, {{get_time()}}!"
        engine = FunctionTemplater()
        result = engine.render(template)
        self.assertEqual(result, "Hello, {{get_time()}}!")

    def test_function_templating_missing_variable_raise(self):
        """Test function substitution with missing variable and raise_on_error=True."""
        template = "Hello, {{get_time()}}!"
        engine = FunctionTemplater(raise_on_error=True)
        with self.assertRaises(RenderError, msg="Trying to insert function get_time but could not find 'get_time'"):
            engine.render(template)
