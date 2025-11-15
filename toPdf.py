import jinja2
import pdfkit

name = "Fahad Alsaif"

context = {"name": name}

templateLoader = jinja2.FileSystemLoader("./")
template_env = jinja2.Environment(loader=templateLoader)

template = template_env.get_template("template.html")
output_text = template.render(context)

config = pdfkit.configuration(wkhtmltopdf=r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe")
pdfkit.from_string(output_text, "output.pdf", configuration=config)