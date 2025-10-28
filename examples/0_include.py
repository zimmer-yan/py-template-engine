from py_template_engine.TemplateEngine import TemplateEngine

with open("./include.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render())
