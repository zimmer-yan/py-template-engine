from unittest import TestCase

from py_template_engine.sub_engines.EachTemplater import EachTemplater


class TestEachTemplater(TestCase):

    def test_each_templating(self):
        """Test basic each substitution."""
        template = "{{#EACH items AS item}}<li>{{item}}</li>{{/EACH}}"
        engine = EachTemplater()
        result = engine.render(template, items=["Hello", "World"])
        self.assertEqual(result, "<li>Hello</li><li>World</li>")

    def test_each_templating_nested(self):
        """Test basic each substitution."""
        template = "{{#EACH items AS item}}<li>{{item.text}}</li>{{/EACH}}"
        engine = EachTemplater()
        result = engine.render(template, items=[{"text": "Hello"}, {"text": "World"}])
        self.assertEqual(result, "<li>Hello</li><li>World</li>")

    def test_each_templating_member(self):
        """Test basic each substitution."""
        template = "{{#EACH member.items AS item}}<li>{{item.text}}</li>{{/EACH}}"
        engine = EachTemplater()
        result = engine.render(
            template, member={"items": [{"text": "Hello"}, {"text": "World"}]}
        )
        self.assertEqual(result, "<li>Hello</li><li>World</li>")

    def test_each_templating_member_nested(self):
        """Test basic each substitution."""
        template = "{{#EACH member.items AS item}}<li>{{item.text}}</li>{{/EACH}}"
        engine = EachTemplater()
        result = engine.render(
            template, member={"items": [{"text": "Hello"}, {"text": "World"}]}
        )
        self.assertEqual(result, "<li>Hello</li><li>World</li>")
