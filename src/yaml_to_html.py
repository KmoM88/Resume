import yaml
from jinja2 import Environment, FileSystemLoader
import os

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return yaml.safe_load(file)

def merge_dicts(a, b):
    # Recursively merge two dicts (b overrides a)
    result = a.copy()
    for k, v in b.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = merge_dicts(result[k], v)
        else:
            result[k] = v
    return result

def render_html(data, template_path):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))

    subtitle = "<br>".join(data.get('subtitle', []))
    experiences = []
    for exp in data.get('experiences', []):
        exp = exp.copy()
        exp['date'] = exp.get('date', {})
        exp['details'] = exp.get('details', [])
        exp['place'] = exp.get('place', '')
        exp['place_url'] = exp.get('place_url', '')
        exp['title'] = exp.get('title', '')
        experiences.append(exp)

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
        pdf_url_esp=data.get('pdf_url_esp', ''),
        cv_url=data.get('cv_url', ''),
    )

def save_html(output_path, html_content):
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

def main():
    common_file = 'data/common.yml'
    eng_file = 'data/content-eng.yml'
    esp_file = 'data/content-esp.yml'
    template_file = 'src/template/resume_template.html'
    output_file = 'docs/index.html'
    output_file_esp = 'docs/index-esp.html'

    common = load_yaml(common_file)
    data_eng = merge_dicts(common, load_yaml(eng_file))
    data_esp = merge_dicts(common, load_yaml(esp_file))
    html_content = render_html(data_eng, template_file)
    html_content_esp = render_html(data_esp, template_file)
    save_html(output_file, html_content)
    save_html(output_file_esp, html_content_esp)

if __name__ == '__main__':
    main()