import os
import yaml
from bs4 import BeautifulSoup

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def extract_subtitle(soup):
    subtitle_tag = soup.find('span', class_='subtitle')
    return [t.strip() for t in subtitle_tag.stripped_strings] if subtitle_tag else []

def extract_experiences(soup):
    experiences = []
    experience_sections = soup.find_all('section', class_='main-block')[0]
    for block in experience_sections.find_all('section', class_='blocks'):
        date_spans = block.find('div', class_='date').find_all('span')
        if len(date_spans) == 2:
            date = {
                'start': date_spans[1].text.strip(),
                'end': date_spans[0].text.strip()
            }
        elif len(date_spans) == 1:
            date = {
                'year': date_spans[0].text.strip()
            }
        else:
            date = {}
        title = block.find('h3').text.strip() if block.find('h3') else ""
        place_tag = block.find('span', class_='place')
        if place_tag:
            a_tag = place_tag.find('a')
            if a_tag:
                place = a_tag.text.strip()
                place_url = a_tag.get('href', '').strip()
            else:
                place = place_tag.text.strip()
                place_url = ''
        else:
            place = ""
            place_url = ""

        # Extract bullet points (ul > li) inside details
        details = []
        details_div = block.find('div', class_='details')
        if details_div:
            ul = details_div.find('ul')
            if ul:
                for li in ul.find_all('li'):
                    a_tag = li.find('a')
                    if a_tag:
                        details.append({
                            'text': li.get_text(strip=True),
                            'url': a_tag.get('href', '').strip()
                        })
                    else:
                        details.append({'text': li.get_text(strip=True), 'url': ''})

        experiences.append({
            'date': date,
            'title': title,
            'place': place,
            'place_url': place_url,
            'details': details
        })
    return experiences

def extract_projects(soup):
    projects = []
    project_sections = soup.find_all('section', class_='main-block')[1]
    for block in project_sections.find_all('section', class_='blocks'):
        date_spans = block.find('div', class_='date').find_all('span')
        if len(date_spans) == 2:
            date = {
                'start': date_spans[1].text.strip(),
                'end': date_spans[0].text.strip()
            }
        elif len(date_spans) == 1:
            date = {
                'year': date_spans[0].text.strip()
            }
        else:
            date = {}
        title = block.find('h3').text.strip() if block.find('h3') else ""
        place = block.find('span', class_='place').text.strip() if block.find('span', class_='place') else ""
        # Extraer bulletpoints (ul > li) dentro de details
        details = []
        details_div = block.find('div', class_='details')
        if details_div:
            ul = details_div.find('ul')
            if ul:
                details = [li.get_text(strip=True) for li in ul.find_all('li')]
        projects.append({
            'date': date,
            'title': title,
            'place': place,
            'details': details
        })
    return projects

def extract_education(soup):
    education = []
    education_sections = soup.find_all('section', class_='main-block concise')[0]
    for block in education_sections.find_all('section', class_='blocks'):
        date_spans = block.find('div', class_='date').find_all('span')
        if len(date_spans) == 2:
            date = {
                'start': date_spans[1].text.strip(),
                'end': date_spans[0].text.strip()
            }
        elif len(date_spans) == 1:
            date = {
                'year': date_spans[0].text.strip()
            }
        else:
            date = {}
        title = block.find('h3').text.strip() if block.find('h3') else ""
        place_tag = block.find('span', class_='place')
        if place_tag:
            a_tag = place_tag.find('a')
            if a_tag:
                place = a_tag.text.strip()
                place_url = a_tag.get('href', '').strip()
            else:
                place = place_tag.text.strip()
                place_url = ''
        else:
            place = ""
            place_url = ""
        education.append({
            'date': date,
            'title': title,
            'place': place,
            'place_url': place_url
        })
    return education

def extract_contact(soup):
    contact = {}
    contact_section = soup.find('aside', id='sidebar').find('div', id='contact')
    for li in contact_section.find_all('li'):
        i_tag = li.find('i')
        if i_tag:
            icon_class = " ".join(i_tag.get('class', []))  # Ej: 'fa fa-github' o 'fab fa-github'
        else:
            icon_class = ""
        a = li.find('a')
        if a:
            contact[icon_class] = {
                'text': a.text.strip(),
                'url': a.get('href', '').strip(),
                'icon': icon_class
            }
        else:
            contact[icon_class] = {
                'text': li.get_text(strip=True),
                'url': '',
                'icon': icon_class
            }
    return contact

def extract_skills(soup):
    skills = {}
    for side_block in soup.find_all('div', class_='side-block', id='skills'):
        ul = side_block.find('ul')
        if not ul:
            continue
        current_category = None
        for elem in ul.children:
            if elem.name == 'h4':
                current_category = elem.get_text(strip=True)
                skills[current_category] = []
            elif elem.name == 'ul' and current_category:
                for li in elem.find_all('li'):
                    skills[current_category].append(li.get_text(strip=True))
            elif elem.name == 'li' and current_category:
                skills[current_category].append(elem.get_text(strip=True))
    return skills

def parse_html_to_yaml(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    resume_data = {
        'name': soup.find('h1').text.strip(),
        'subtitle': extract_subtitle(soup),
        'experiences': extract_experiences(soup),
        'projects': extract_projects(soup),
        'education': extract_education(soup),
        'contact': extract_contact(soup),
        'skills': extract_skills(soup)
    }
    return resume_data

def write_yaml_file(data, output_path):
    with open(output_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)

def main():
    html_file_path = 'index2.html'  # Update with your HTML file path
    yaml_output_path = 'data/resume.yaml'
    
    html_content = read_html_file(html_file_path)
    resume_data = parse_html_to_yaml(html_content)
    write_yaml_file(resume_data, yaml_output_path)

if __name__ == '__main__':
    main()