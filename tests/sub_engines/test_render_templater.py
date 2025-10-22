import os
import tempfile
from unittest import TestCase

from py_template_engine.sub_engines.RenderTemplater import RenderTemplater


class TestRenderTemplater(TestCase):

    def setUp(self):
        """Set up test fixtures with temporary template files."""
        self.templater = RenderTemplater()

        # Create temporary directory for template files
        self.temp_dir = tempfile.mkdtemp()

        # Create a simple template with variables
        self.greeting_template = os.path.join(self.temp_dir, "greeting.html")
        with open(self.greeting_template, "w") as f:
            f.write("Hello, {{name}}! Welcome to {{site_name}}.")

        # Create a template with function calls
        self.time_template = os.path.join(self.temp_dir, "time.html")
        with open(self.time_template, "w") as f:
            f.write("Current time: {{get_time()}}")

        # Create a template with conditionals
        self.conditional_template = os.path.join(self.temp_dir, "conditional.html")
        with open(self.conditional_template, "w") as f:
            f.write(
                "{{#IF logged_in}}Welcome back, {{username}}!{{#ELSE}}Please log in{{/IF}}"
            )

        # Create a template with loops
        self.list_template = os.path.join(self.temp_dir, "list.html")
        with open(self.list_template, "w") as f:
            f.write("<ul>{{#EACH items AS item}}<li>{{item}}</li>{{/EACH}}</ul>")

        # Create a complex nested template
        self.complex_template = os.path.join(self.temp_dir, "complex.html")
        with open(self.complex_template, "w") as f:
            f.write(
                """
            <div class="user-info">
                {{#IF user}}
                    <h2>{{user.name}}</h2>
                    <p>Email: {{user.email}}</p>
                    {{#EACH user.hobbies AS hobby}}
                        <span class="hobby">{{hobby}}</span>
                    {{/EACH}}
                {{#ELSE}}
                    <p>No user data available</p>
                {{/IF}}
            </div>
            """.strip()
            )

        # Create an empty template
        self.empty_template = os.path.join(self.temp_dir, "empty.html")
        with open(self.empty_template, "w") as f:
            f.write("")

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_basic_render_with_variables(self):
        """Test basic template rendering with variables."""
        template = f"{{{{#RENDER {self.greeting_template}}}}}"
        result = self.templater.render(template, name="Alice", site_name="My Website")
        self.assertEqual(result, "Hello, Alice! Welcome to My Website.")

    def test_render_with_function_calls(self):
        """Test rendering template with function calls."""
        template = f"{{{{#RENDER {self.time_template}}}}}"
        result = self.templater.render(template, get_time=lambda: "12:30 PM")
        self.assertEqual(result, "Current time: 12:30 PM")

    def test_render_with_conditionals(self):
        """Test rendering template with IF/ELSE conditions."""
        template = f"{{{{#RENDER {self.conditional_template}}}}}"

        # Test when logged in
        result_logged_in = self.templater.render(
            template, logged_in=True, username="Bob"
        )
        self.assertEqual(result_logged_in, "Welcome back, Bob!")

        # Test when not logged in
        result_not_logged_in = self.templater.render(template, logged_in=False)
        self.assertEqual(result_not_logged_in, "Please log in")

    def test_render_with_loops(self):
        """Test rendering template with EACH loops."""
        template = f"{{{{#RENDER {self.list_template}}}}}"
        result = self.templater.render(template, items=["Apple", "Banana", "Cherry"])
        expected = "<ul><li>Apple</li><li>Banana</li><li>Cherry</li></ul>"
        self.assertEqual(result, expected)

    def test_complex_template_rendering(self):
        """Test rendering complex template with multiple features."""
        template = f"{{{{#RENDER {self.complex_template}}}}}"

        user_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "hobbies": ["Reading", "Gaming", "Coding"],
        }

        result = self.templater.render(template, user=user_data)

        # Check all parts are rendered correctly
        self.assertIn("John Doe", result)
        self.assertIn("john@example.com", result)
        self.assertIn("Reading", result)
        self.assertIn("Gaming", result)
        self.assertIn("Coding", result)

    def test_multiple_renders_in_template(self):
        """Test template with multiple RENDER directives."""
        template = f"""
        <header>{{{{#RENDER {self.greeting_template}}}}}</header>
        <main>{{{{#RENDER {self.list_template}}}}}</main>
        <footer>{{{{#RENDER {self.time_template}}}}}</footer>
        """.strip()

        result = self.templater.render(
            template,
            name="Sarah",
            site_name="Blog",
            items=["Post 1", "Post 2"],
            get_time=lambda: "3:45 PM",
        )

        self.assertIn("Hello, Sarah! Welcome to Blog.", result)
        self.assertIn("<li>Post 1</li><li>Post 2</li>", result)
        self.assertIn("Current time: 3:45 PM", result)

    def test_nested_template_context(self):
        """Test that context variables are properly passed to rendered templates."""
        template = f"User: {{{{#RENDER {self.greeting_template}}}}} | Time: {{{{#RENDER {self.time_template}}}}}"

        result = self.templater.render(
            template, name="Mike", site_name="Forum", get_time=lambda: "Morning"
        )

        expected = "User: Hello, Mike! Welcome to Forum. | Time: Current time: Morning"
        self.assertEqual(result, expected)

    def test_render_empty_template(self):
        """Test rendering an empty template file."""
        template = f"Before{{{{#RENDER {self.empty_template}}}}}After"
        result = self.templater.render(template)
        self.assertEqual(result, "BeforeAfter")

    def test_template_with_no_renders(self):
        """Test template without any RENDER directives."""
        template = "<p>This template has no render directives</p>"
        result = self.templater.render(template)
        self.assertEqual(result, template)

    def test_render_with_whitespace_in_path(self):
        """Test RENDER directive with whitespace around the path."""
        template = f"{{{{#RENDER    {self.greeting_template}    }}}}"
        result = self.templater.render(template, name="Tom", site_name="App")
        # The .strip() in RenderTemplater should handle whitespace
        self.assertEqual(result, "Hello, Tom! Welcome to App.")

    def test_file_not_found_error(self):
        """Test behavior when rendered template file doesn't exist."""
        nonexistent_file = os.path.join(self.temp_dir, "nonexistent.html")
        template = f"{{{{#RENDER {nonexistent_file}}}}}"

        with self.assertRaises(FileNotFoundError):
            self.templater.render(template)

    def test_render_same_template_multiple_times(self):
        """Test rendering the same template file multiple times."""
        template = f"""
        {{{{#RENDER {self.greeting_template}}}}}
        <hr>
        {{{{#RENDER {self.greeting_template}}}}}
        """.strip()

        result = self.templater.render(template, name="Lisa", site_name="Shop")

        greeting_text = "Hello, Lisa! Welcome to Shop."
        self.assertEqual(result.count(greeting_text), 2)

    def test_render_with_missing_variables(self):
        """Test rendering when template requires variables that aren't provided."""
        template = f"{{{{#RENDER {self.greeting_template}}}}}"

        # Should not fail, variables will just be empty/missing
        # This depends on how VariableTemplater handles missing variables
        try:
            result = self.templater.render(template, name="Alex")  # Missing site_name
            # If it doesn't raise an error, that's also valid behavior
            self.assertIn("Alex", result)
        except KeyError:
            # If it raises KeyError for missing variables, that's expected
            pass


if __name__ == "__main__":
    import unittest

    unittest.main()
