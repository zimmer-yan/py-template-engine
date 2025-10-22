from py_template_engine.TemplateEngine import TemplateEngine

with open("./each.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(items=["Hello", "World"]))
