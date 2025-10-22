from py_template_engine.TemplateEngine import TemplateEngine

with open("./if.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(condition=True))
print("=======")
print(templater.render(condition=False))
