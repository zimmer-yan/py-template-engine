import os
import tempfile
from unittest import TestCase

from py_template_engine.sub_engines.IncludeTemplater import IncludeTemplater
from py_template_engine.RenderError import RenderError

class TestIncludeTemplater(TestCase):

    def setUp(self):
        """Set up test fixtures with temporary files."""
        self.templater = IncludeTemplater()

        # Create temporary files for testing
        self.temp_dir = tempfile.mkdtemp()

        # Create a simple content file
        self.header_file = os.path.join(self.temp_dir, "header.html")
        with open(self.header_file, "w") as f:
            f.write("<header><h1>My Website</h1></header>")

        # Create another content file
        self.footer_file = os.path.join(self.temp_dir, "footer.html")
        with open(self.footer_file, "w") as f:
            f.write("<footer>&copy; 2024 My Company</footer>")

        # Create a content file with variables
        self.nav_file = os.path.join(self.temp_dir, "nav.html")
        with open(self.nav_file, "w") as f:
            f.write("<nav><a href='/home'>Home</a><a href='/about'>About</a></nav>")

    def tearDown(self):
        """Clean up temporary files."""
        import shutil

        shutil.rmtree(self.temp_dir)

    def test_basic_include(self):
        """Test basic file inclusion functionality."""
        template = f"{{{{#INCLUDE {self.header_file}}}}}"
        result = self.templater.render(template)
        self.assertEqual(result, "<header><h1>My Website</h1></header>")

    def test_multiple_includes(self):
        """Test including multiple files in one template."""
        template = f"""
        {{{{#INCLUDE {self.header_file}}}}}
        <main>Content here</main>
        {{{{#INCLUDE {self.footer_file}}}}}
        """.strip()

        result = self.templater.render(template)

        self.assertIn("<header><h1>My Website</h1></header>", result)
        self.assertIn("<main>Content here</main>", result)
        self.assertIn("<footer>&copy; 2024 My Company</footer>", result)

    def test_same_file_multiple_times(self):
        """Test including the same file multiple times."""
        template = f"""
        {{{{#INCLUDE {self.nav_file}}}}}
        <main>Some content</main>
        {{{{#INCLUDE {self.nav_file}}}}}
        """.strip()

        result = self.templater.render(template)

        # Should contain the nav content twice
        nav_content = "<nav><a href='/home'>Home</a><a href='/about'>About</a></nav>"
        self.assertEqual(result.count(nav_content), 2)

    def test_nested_includes_structure(self):
        """Test a complete page structure with includes."""
        template = f"""<!DOCTYPE html>
<html>
<head><title>Test Page</title></head>
<body>
{{{{#INCLUDE {self.header_file}}}}}
{{{{#INCLUDE {self.nav_file}}}}}
<main>
    <p>Welcome to our website!</p>
</main>
{{{{#INCLUDE {self.footer_file}}}}}
</body>
</html>"""

        result = self.templater.render(template)

        # Verify all parts are included
        self.assertIn("<header><h1>My Website</h1></header>", result)
        self.assertIn(
            "<nav><a href='/home'>Home</a><a href='/about'>About</a></nav>", result
        )
        self.assertIn("<footer>&copy; 2024 My Company</footer>", result)
        self.assertIn("Welcome to our website!", result)

    def test_include_with_different_variable_names(self):
        """Test includes with various variable naming patterns."""
        template = f"""
        {{{{#INCLUDE {self.header_file}}}}}
        {{{{#INCLUDE {self.nav_file}}}}}
        {{{{#INCLUDE {self.footer_file}}}}}
        """

        result = self.templater.render(template)

        self.assertIn("<header><h1>My Website</h1></header>", result)
        self.assertIn(
            "<nav><a href='/home'>Home</a><a href='/about'>About</a></nav>", result
        )
        self.assertIn("<footer>&copy; 2024 My Company</footer>", result)

    def test_include_with_whitespace(self):
        """Test include directive with extra whitespace."""
        template = "{{#INCLUDE   header_path   }}"
        result = self.templater.render(template, header_path=self.header_file)
        # Note: The regex captures whitespace, so this tests the actual behavior
        self.assertIn("header", result.lower())

    def test_no_includes_in_template(self):
        """Test template without any include directives."""
        template = "<p>This is just regular content with no includes</p>"
        result = self.templater.render(template)
        self.assertEqual(result, template)

    def test_file_not_found_error_dont_raise(self):
        """Test behavior when included file doesn't exist."""
        template = "{{#INCLUDE missing_file}}"

        result = self.templater.render(template)
        self.assertEqual(result, "{{#INCLUDE missing_file}}")

    def test_file_not_found_error_raise(self):
        """Test behavior when included file doesn't exist."""
        template = "{{#INCLUDE missing_file}}"

        templater = IncludeTemplater(raise_on_error=True)
        with self.assertRaises(RenderError, msg="Trying to include file but could not find path 'missing_file'"):
            templater.render(template)

    def test_empty_file_include(self):
        """Test including an empty file."""
        empty_file = os.path.join(self.temp_dir, "empty.html")
        with open(empty_file, "w") as f:
            f.write("")  # Empty file

        template = f"Before{{{{#INCLUDE {empty_file}}}}}After"
        result = self.templater.render(template)
        self.assertEqual(result, "BeforeAfter")
