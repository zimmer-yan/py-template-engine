from py_template_engine.TemplateEngine import TemplateEngine

with open("./each_member.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(member={"items": [{"text": "Hello"}, {"text": "World"}]}))
