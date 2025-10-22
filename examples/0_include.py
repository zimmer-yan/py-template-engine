from py_template_engine.TemplateEngine import TemplateEngine

to_be_included = "./hello_world.html"

with open("./include.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(to_be_included=to_be_included))
