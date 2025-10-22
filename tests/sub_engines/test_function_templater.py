from unittest import TestCase

from py_template_engine.sub_engines.FunctionTemplater import FunctionTemplater


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
