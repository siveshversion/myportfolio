import logging
import smtplib
import ssl
import streamlit as st
import portfolio_data as pd
from pathlib import Path
from PIL import Image
from email.message import EmailMessage
from streamlit.errors import StreamlitSecretNotFoundError
from urllib.parse import quote

PROJECT_ROOT = Path(__file__).resolve().parent
LOGGER = logging.getLogger(__name__)

# Page Configuration
st.set_page_config(
    page_title=f"{pd.PORTFOLIO_DATA['name']} - Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Custom CSS
st.markdown(
    f"<style>{(PROJECT_ROOT / 'assets' / 'style.css').read_text(encoding='utf-8')}</style>",
    unsafe_allow_html=True,
)

# Import FontAwesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# Session State for Navigation
if 'section' not in st.session_state:
    st.session_state.section = 'Home'

section_order = ["Home", "Experience", "Projects", "Skills", "Certifications", "Education", "Contact"]

def navigate_by(offset):
    current_index = section_order.index(st.session_state.section)
    next_index = max(0, min(current_index + offset, len(section_order) - 1))
    st.session_state.section = section_order[next_index]

def render_navigation_buttons(position):
    current_index = section_order.index(st.session_state.section)
    with st.container(key=f"section_nav_{position}"):
        col1, col2, col3 = st.columns([1.2, 5, 1.2], vertical_alignment="center")

        with col1:
            st.button(
                "←",
                key=f"prev_{position}",
                help="Previous section",
                on_click=navigate_by,
                args=(-1,),
                disabled=current_index == 0,
                use_container_width=True,
            )

        with col2:
            st.markdown(
                f'<div class="section-nav-progress">'
                f'<span>{current_index + 1:02d} / {len(section_order):02d}</span>'
                f'<strong>{st.session_state.section}</strong>'
                f'</div>',
                unsafe_allow_html=True,
            )

        with col3:
            st.button(
                "→",
                key=f"next_{position}",
                help="Next section",
                on_click=navigate_by,
                args=(1,),
                disabled=current_index == len(section_order) - 1,
                use_container_width=True,
            )

# Sidebar - Profile & Navigation
with st.sidebar:
    # Profile Image
    try:
        image = Image.open(PROJECT_ROOT / "assets" / "profile.jpg")
        st.markdown('<div class="profile-img-container">', unsafe_allow_html=True)
        st.image(image) # CSS handles sizing and glow
        st.markdown('</div>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.markdown('<div class="profile-img-container">', unsafe_allow_html=True)
        st.image("https://placehold.co/150x150?text=Profile", width=150)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='text-align: center; color: white;'>{pd.PORTFOLIO_DATA['name']}</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: #aaaaaa;'>{pd.PORTFOLIO_DATA['title']}</p>", unsafe_allow_html=True)
    
    # Social Links
    st.markdown(f"""
    <div style="display: flex; justify-content: center; gap: 20px; margin-bottom: 20px;">
        <a href="{pd.PORTFOLIO_DATA.get('linkedin', '#')}" target="_blank" style="color: #00d4ff; font-size: 1.5rem;"><i class="fab fa-linkedin"></i></a>
        <a href="{pd.PORTFOLIO_DATA.get('github', '#')}" target="_blank" style="color: #00d4ff; font-size: 1.5rem;"><i class="fab fa-github"></i></a>
        <a href="mailto:{pd.PORTFOLIO_DATA.get('email', '#')}" style="color: #00d4ff; font-size: 1.5rem;"><i class="fas fa-envelope"></i></a>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    
    # Navigation
    selected_section = st.radio(
        "Navigate",
        section_order,
        label_visibility="collapsed",
        key="section"
    )
    
    st.markdown("---")
    resume_path = PROJECT_ROOT / pd.PORTFOLIO_DATA["resume_file"]
    if resume_path.is_file():
        with resume_path.open("rb") as pdf_file:
            st.download_button(
                label="📄 Download Resume",
                data=pdf_file.read(),
                file_name=resume_path.name,
                mime="application/pdf",
                use_container_width=True
            )

# Main Content

def home_section():
    st.markdown(f"<h1 style='font-size: 3.5rem; margin-bottom: 10px;'>Hello, I'm <span style='color: #00d4ff;'>{pd.PORTFOLIO_DATA['name']}</span></h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='color: #e0e0e0;'>{pd.PORTFOLIO_DATA['title']}</h3>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size: 1.2rem; color: #aaaaaa; max-width: 800px;'>{pd.PORTFOLIO_DATA['about_me']}</p>", unsafe_allow_html=True)
    
    st.markdown("###")
    
    # Quick Summary Cards
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="glass-card summary-card">
            <div class="summary-card-title">🚀 Experience</div>
            <p>8+ Years in Software Engineering</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card summary-card">
            <div class="summary-card-title">💡 Innovation</div>
            <p>Automation Expert & AI Enthusiast</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card summary-card">
            <div class="summary-card-title">🎓 Education</div>
            <p>B.E. Computer Science</p>
        </div>
        """, unsafe_allow_html=True)

def experience_section():
    st.markdown('<div class="section-header">Experience</div>', unsafe_allow_html=True)
    
    for job in pd.PORTFOLIO_DATA['experience']:
        responsibilities_html = "".join(
            f"<li>{responsibility}</li>"
            for responsibility in job.get("responsibilities", [])
        )
        tech_stack_html = "".join(
            f"<span class='skill-pill'>{technology}</span>"
            for technology in job.get("tech_stack", [])
        )
        st.markdown(f"""
        <div class="timeline-item">
            <h3 class="role-title">{job['role']}</h3>
            <h4 class="company-name">{job['company']}</h4>
            <p class="duration">{job['duration']}</p>
            <p>{job['location']}</p>
            <ul>{responsibilities_html}</ul>
            <div>{tech_stack_html}</div>
        </div>
        """, unsafe_allow_html=True)

def projects_section():
    st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, project in enumerate(pd.PORTFOLIO_DATA['projects']):
        with cols[i % 2]:
            tech_stack_html = ' '.join([f'<span class="skill-pill" style="font-size: 0.8rem; padding: 4px 8px;">{tech}</span>' for tech in project['tech_stack']])
            project_link_html = (
                f'<div style="margin-top: 15px;"><a href="{project["link"]}" target="_blank" rel="noopener noreferrer">{project.get("link_label", "View Project 🔗")}</a></div>'
                if project.get('link')
                else ''
            )
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: #00d4ff;">{project['title']}</h3>
                <p>{project['description']}</p>
                <div style="margin: 10px 0;">
                    {tech_stack_html}
                </div>
                {project_link_html}
            </div>
            """, unsafe_allow_html=True)

def skills_section():
    st.markdown('<div class="section-header">Skills</div>', unsafe_allow_html=True)
    
    for category, skills in pd.PORTFOLIO_DATA['skills'].items():
        st.markdown(f"<div class='sub-header'>{category}</div>", unsafe_allow_html=True)
        skills_html = "".join([f"<span class='skill-pill'>{skill}</span>" for skill in skills])
        st.markdown(f"{skills_html}", unsafe_allow_html=True)

def certifications_section():
    st.markdown('<div class="section-header">Certifications</div>', unsafe_allow_html=True)

    for cert in pd.PORTFOLIO_DATA.get('certifications', []):
        pdf_name = cert.get('file')
        pdf_path = None
        if pdf_name:
            pdf_path = PROJECT_ROOT / pdf_name

        cert_title = f"<h3 style=\"color: #00d4ff;\">{cert['name']}</h3>"
        if pdf_path and pdf_path.exists():
            static_path = pdf_path.relative_to(PROJECT_ROOT / "static").as_posix()
            certificate_url = f"/app/static/{quote(static_path, safe='/')}"
            cert_title = (
                f'<h3><a href="{certificate_url}" target="_blank" '
                f'rel="noopener noreferrer" style="color: #00d4ff; text-decoration: none;">'
                f'{cert["name"]} <span aria-label="opens certificate in a new tab">↗</span></a></h3>'
            )

        cert_details = cert["issuer"]
        if cert.get("year"):
            cert_details += f" · {cert['year']}"

        st.markdown(f"""
        <div class="glass-card">
            {cert_title}
            <p><strong>{cert_details}</strong></p>
        </div>
        """, unsafe_allow_html=True)

def education_section():
    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
    
    for edu in pd.PORTFOLIO_DATA['education']:
        description_html = (
            f"<p>{edu['description']}</p>"
            if edu.get("description")
            else ""
        )
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: #ffffff;">{edu['institution']}</h3>
            <h4 style="color: #00d4ff;">{edu['degree']}</h4>
            <p style="color: #aaaaaa; font-style: italic;">{edu['year']}</p>
            {description_html}
        </div>
        """, unsafe_allow_html=True)

def send_contact_email(sender_email, sender_password, sender_name, sender_address, message, receiver_email):
    email_message = EmailMessage()
    email_message["From"] = sender_email
    email_message["To"] = receiver_email
    email_message["Reply-To"] = sender_address
    email_message["Subject"] = "New message from your portfolio contact form"
    email_message.set_content(
        f"Name: {sender_name}\n"
        f"Email: {sender_address}\n\n"
        f"Message:\n{message}"
    )

    with smtplib.SMTP("smtp.gmail.com", 587, timeout=15) as server:
        server.starttls(context=ssl.create_default_context())
        server.login(sender_email, sender_password)
        server.send_message(email_message)

def contact_section():
    st.markdown('<div class="section-header">Contact</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="glass-card">
            <h3>Get in Touch</h3>
            <p>📧 <a href="mailto:{pd.PORTFOLIO_DATA['email']}">{pd.PORTFOLIO_DATA['email']}</a></p>
            <p>📞 {pd.PORTFOLIO_DATA['phone']}</p>
            <p>🔗 <a href="{pd.PORTFOLIO_DATA['linkedin']}">LinkedIn</a></p>
            <p>🐙 <a href="{pd.PORTFOLIO_DATA['github']}">GitHub</a></p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>Send a Message</h3>
        </div>
        """, unsafe_allow_html=True)
        # Using native streamlit form for the input fields
        with st.form("contact_form"):
            name = st.text_input("Name")
            sender_address = st.text_input("Email")
            message = st.text_area("Message")
            
            if st.form_submit_button("Send Message"):
                name = name.strip()
                sender_address = sender_address.strip()
                message = message.strip()

                if not name or not sender_address or not message:
                    st.warning("Please fill out all fields.")
                elif (
                    "@" not in sender_address
                    or sender_address.startswith("@")
                    or sender_address.endswith("@")
                    or any(character.isspace() for character in sender_address)
                ):
                    st.warning("Please enter a valid email address.")
                else:
                    try:
                        sender_email = st.secrets.get("EMAIL_USER")
                        sender_password = st.secrets.get("EMAIL_PASS")
                    except StreamlitSecretNotFoundError:
                        sender_email = None
                        sender_password = None
                        
                    if not isinstance(sender_email, str) or not sender_email.strip() or not isinstance(sender_password, str) or not sender_password.strip():
                        st.error("Email secrets (`EMAIL_USER`, `EMAIL_PASS`) are not configured.")
                        st.info("To enable emails, create `.streamlit/secrets.toml` with your Gmail address and App Password.")
                    else:
                        try:
                            receiver_email = pd.PORTFOLIO_DATA.get('email', sender_email)
                            send_contact_email(
                                sender_email.strip(),
                                sender_password.strip(),
                                name,
                                sender_address,
                                message,
                                receiver_email,
                            )
                            st.success("Message sent successfully! I will get back to you soon.")
                        except (OSError, smtplib.SMTPException, ValueError):
                            LOGGER.exception("Portfolio contact form email delivery failed")
                            st.error(
                                "The message could not be sent. Please try again later or contact me "
                                "directly using the email address shown on this page."
                            )

render_navigation_buttons("top")

# Routing
if selected_section == "Home":
    home_section()
elif selected_section == "Experience":
    experience_section()
elif selected_section == "Projects":
    projects_section()
elif selected_section == "Skills":
    skills_section()
elif selected_section == "Certifications":
    certifications_section()
elif selected_section == "Education":
    education_section()
elif selected_section == "Contact":
    contact_section()

# Render Footer Navigation (Bottom of page logic)
st.markdown("---")
render_navigation_buttons("bottom")

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #555; font-size: 0.8rem;'>© 2026 {pd.PORTFOLIO_DATA['name']} | Built with Streamlit</div>", unsafe_allow_html=True)
