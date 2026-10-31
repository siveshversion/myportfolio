# Ashok Kumar - Portfolio

A personal portfolio website built with Streamlit. It presents professional experience, projects, technical skills, education, contact details, and the AWS Certified Cloud Practitioner credential.

## Features

- Portfolio sections for Home, Experience, Projects, Skills, Certifications, Education, and Contact
- AWS certification linked to open the certificate PDF in a new tab
- Resume PDF download
- Responsive layout styled with `assets/style.css`
- Contact form email support when SMTP credentials are configured

## Requirements

- Python 3.9 or newer
- pip

## Quick start on Windows

Double-click `launch.bat` or run it from Command Prompt. It creates `.venv` if needed, installs dependencies from `requirements.txt`, and starts the Streamlit app.

To run manually:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Run on macOS or Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

## Configuration

The portfolio's personal details, work history, projects, skills, and certification information are maintained in `portfolio_data.py`.

The contact form sends messages to the portfolio email address using Gmail SMTP with STARTTLS. Configure a Gmail account and its App Password in `.streamlit/secrets.toml`:

```toml
EMAIL_USER = "your-sender@gmail.com"
EMAIL_PASS = "your-gmail-app-password"
```

`EMAIL_USER` is the authenticated sender account, while the visitor's email is set as `Reply-To` so replies go directly to them. The sender account must have 2-Step Verification enabled and use a Google App Password; a regular Gmail password will not work. The form validates required fields and the email format, and reports delivery failures in the app.

Keep `.streamlit/secrets.toml` private and never commit credentials. When deploying, configure `EMAIL_USER` and `EMAIL_PASS` in the hosting platform's secrets settings as well.

## Project files

- `app.py` - Streamlit application and page rendering
- `portfolio_data.py` - Portfolio content
- `assets/style.css` - Application styles
- `assets/profile.jpg` - Profile image
- `static/certificates/` - Certification PDFs served by Streamlit
- `assets/Ashok_Kumar_M_Senior_Java_Developer_Resume_2026.pdf` - Resume PDF
- `launch.bat` - Windows quick-launch script
- `requirements.txt` - Python dependencies
