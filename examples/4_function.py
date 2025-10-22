from py_template_engine.TemplateEngine import TemplateEngine


def hello_world():
    return "Hello, World! (but from a function)"


with open("./function.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(function=hello_world))
