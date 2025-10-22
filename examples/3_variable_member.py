from py_template_engine.TemplateEngine import TemplateEngine

with open("./variable_member.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(member={"field": {"text": "Hello, Rendered!"}}))
