from py_template_engine.TemplateEngine import TemplateEngine

with open("./if_member.html", "r") as file:
    template = file.read()

templater = TemplateEngine(template_string=template)
print(templater.render(member={"condition": True}))
print("=======")
print(templater.render(member={"condition": False}))
