import yaml
from jinja2 import Environment, FileSystemLoader
import os

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def format_date(date_dict):
    if not date_dict:
        return ""
    if 'start' in date_dict and 'end' in date_dict:
        return f"{date_dict['start']} - {date_dict['end']}"
    elif 'year' in date_dict:
        return f"{date_dict['year']}"
    return ""

def render_html(data, template_path):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    # Subtitle as a multiline string
    subtitle = "<br>".join(data.get('subtitle', []))

    # Process experiences
    experiences = []
    for exp in data.get('experiences', []):
        exp = exp.copy()
        exp['date'] = exp.get('date', {})
        exp['details'] = exp.get('details', [])
        exp['place'] = exp.get('place', '')
        exp['place_url'] = exp.get('place_url', '')
        exp['title'] = exp.get('title', '')
        experiences.append(exp)

    # Process other sections (projects, education, etc.)
    projects = data.get('projects', [])
    education = data.get('education', [])
    contact = data.get('contact', {})
    skills = data.get('skills', {})

    return template.render(
        name=data.get('name', ''),
        subtitle=subtitle,
        sumary=data.get('summary', ''),
        experiences=experiences,
        projects=projects,
        education=education,
        contact=contact,
        skills=skills,
        pdf_url=data.get('pdf_url', ''),
        cv_url=data.get('cv_url', ''),
    )

def save_html(output_path, html_content):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def main():
    yaml_file = 'data/resume.yaml'
    template_file = 'src/template/resume_template.html'
    output_file = 'index.html'

    data = load_yaml(yaml_file)
    html_content = render_html(data, template_file)
    save_html(output_file, html_content)

if __name__ == '__main__':
    main()