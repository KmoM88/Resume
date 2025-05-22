# Resume Organizer

This project is designed to convert a resume from HTML format into a structured YAML format and then generate an HTML resume from the YAML data. It also includes a GitHub Actions workflow to automate the deployment of the generated HTML to GitHub Pages and update the PDF version of the resume.

## Project Structure

```
resume-organizer
├── src
│   ├── html_to_yaml.py        # Script to parse HTML and convert to YAML
│   ├── yaml_to_html.py        # Script to generate HTML from YAML
│   └── templates
│       └── resume_template.html # HTML template for the resume
├── data
│   └── resume.yaml             # YAML file storing structured resume data
├── .github
│   └── workflows
│       └── deploy.yml          # GitHub Actions workflow for deployment
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/resume-organizer.git
   cd resume-organizer
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

### Convert HTML to YAML

To convert the HTML resume to YAML format, run the following command:

```
python src/html_to_yaml.py
```

This will read the HTML file and generate a `resume.yaml` file in the `data` directory.

### Generate HTML from YAML

To generate the HTML resume from the YAML data, run:

```
python src/yaml_to_html.py
```

This will create an HTML file using the data from `resume.yaml` and the template defined in `src/templates/resume_template.html`.

## GitHub Actions Workflow

The project includes a GitHub Actions workflow defined in `.github/workflows/deploy.yml`. This workflow will:

- Build the HTML from the YAML file.
- Deploy the generated HTML to GitHub Pages.
- Update the PDF version of the resume in the repository.

## License

This project is licensed under the MIT License. See the LICENSE file for details.