from unittest import TestCase

from py_template_engine.sub_engines.IfTemplater import IfTemplater


class TestIfTemplater(TestCase):

    def test_if_templating_true(self):
        """Test basic IF condition when true."""
        template = "{{#IF condition}}Hello!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, condition=True)
        self.assertEqual(result, "Hello!")

    def test_if_templating_false(self):
        """Test basic IF condition when false."""
        template = "{{#IF condition}}Hello!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, condition=False)
        self.assertEqual(result, "")

    def test_if_templating_nested_object_true(self):
        """Test IF condition with nested object property when true."""
        template = "{{#IF user.condition}}Hello!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, user={"condition": True})
        self.assertEqual(result, "Hello!")

    def test_if_templating_nested_false(self):
        """Test IF condition with nested object property when false."""
        template = "{{#IF user.condition}}Hello!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, user={"condition": False})
        self.assertEqual(result, "")

    def test_if_templating_else_true(self):
        """Test IF-ELSE condition when IF condition is true."""
        template = "{{#IF condition}}Hello!{{#ELSE}}Goodbye!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, condition=True)
        self.assertEqual(result, "Hello!")

    def test_if_templating_else_false(self):
        """Test IF-ELSE condition when IF condition is false."""
        template = "{{#IF condition}}Hello!{{#ELSE}}Goodbye!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, condition=False)
        self.assertEqual(result, "Goodbye!")

    def test_if_templating_nested_else_true(self):
        """Test IF-ELSE with nested object property when true."""
        template = "{{#IF user.condition}}Hello!{{#ELSE}}Goodbye!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, user={"condition": True})
        self.assertEqual(result, "Hello!")

    def test_if_templating_nested_else_false(self):
        """Test IF-ELSE with nested object property when false."""
        template = "{{#IF user.condition}}Hello!{{#ELSE}}Goodbye!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, user={"condition": False})
        self.assertEqual(result, "Goodbye!")

    def test_if_templating_with_text_around(self):
        """Test IF condition with text before and after."""
        template = "Start {{#IF condition}}middle{{/IF}} end"
        engine = IfTemplater()

        result_true = engine.render(template, condition=True)
        self.assertEqual(result_true, "Start middle end")

        result_false = engine.render(template, condition=False)
        self.assertEqual(result_false, "Start  end")

    def test_if_templating_multiple_separate_ifs(self):
        """Test multiple separate IF conditions in one template."""
        template = "{{#IF first}}A{{/IF}} {{#IF second}}B{{#ELSE}}C{{/IF}}"
        engine = IfTemplater()

        # Both true
        result1 = engine.render(template, first=True, second=True)
        self.assertEqual(result1, "A B")

        # First true, second false
        result2 = engine.render(template, first=True, second=False)
        self.assertEqual(result2, "A C")

        # Both false
        result3 = engine.render(template, first=False, second=False)
        self.assertEqual(result3, " C")

    def test_if_templating_whitespace_handling(self):
        """Test IF condition with various whitespace patterns."""
        template = "{{#IF   condition   }}Hello!{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, condition=True)
        self.assertEqual(result, "Hello!")

    def test_if_templating_empty_content(self):
        """Test IF condition with empty content blocks."""
        template = "{{#IF condition}}{{#ELSE}}Empty else{{/IF}}"
        engine = IfTemplater()

        result_true = engine.render(template, condition=True)
        self.assertEqual(result_true, "")

        result_false = engine.render(template, condition=False)
        self.assertEqual(result_false, "Empty else")

    def test_if_templating_double_nested_true(self):
        """Test nested IF conditions when both conditions are true."""
        template = "{{#IF foo}}{{#IF bar}}Hello!{{/IF}}{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, foo=True, bar=True)
        self.assertEqual(result, "Hello!")

    def test_if_templating_double_nested_inner_false(self):
        """Test nested IF conditions when outer is true but inner is false."""
        template = "{{#IF foo}}{{#IF bar}}Hello!{{/IF}}{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, foo=True, bar=False)
        self.assertEqual(result, "")

    def test_if_templating_double_nested_outer_false(self):
        """Test nested IF conditions when outer condition is false."""
        template = "{{#IF foo}}{{#IF bar}}Hello!{{/IF}}{{/IF}}"
        engine = IfTemplater()
        result = engine.render(template, foo=False, bar=True)
        self.assertEqual(result, "")

    def test_if_templating_complex_nested_with_else(self):
        """Test complex nested IF with ELSE blocks."""
        template = "{{#IF user}}{{#IF user.active}}Active User{{#ELSE}}Inactive User{{/IF}}{{#ELSE}}No User{{/IF}}"
        engine = IfTemplater()

        # Test active user
        result1 = engine.render(template, user={"active": True})
        self.assertEqual(result1, "Active User")

        # Test inactive user
        result2 = engine.render(template, user={"active": False})
        self.assertEqual(result2, "Inactive User")

        # Test no user
        result3 = engine.render(template, user=None)
        self.assertEqual(result3, "No User")

    def test_if_templating_triple_nested(self):
        """Test deeply nested IF conditions."""
        template = "{{#IF a}}{{#IF b}}{{#IF c}}Deep!{{/IF}}{{/IF}}{{/IF}}"
        engine = IfTemplater()

        # All true
        result1 = engine.render(template, a=True, b=True, c=True)
        self.assertEqual(result1, "Deep!")

        # One false
        result2 = engine.render(template, a=True, b=True, c=False)
        self.assertEqual(result2, "")


if __name__ == "__main__":
    import unittest

    unittest.main()
