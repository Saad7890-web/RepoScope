from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os

def render_pdf(data: Dict[str, Any]) -> bytes:
    env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")))
    template = env.get_template("report_template.html")
    html_content = template.render(
        code_quality=data.get("code_quality", {}),
        security=data.get("security", {}),
        activity=data.get("activity", {}),
        best_practices=data.get("best_practices", {})
    )
    pdf = HTML(string=html_content).write_pdf()
    return pdf