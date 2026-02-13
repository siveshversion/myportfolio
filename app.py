import streamlit as st
import portfolio_data as pd
from PIL import Image

# Page Configuration
st.set_page_config(
    page_title=f"{pd.PORTFOLIO_DATA['name']} - Portfolio",
    page_icon="👨‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Load Custom CSS
with open("assets/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Import FontAwesome
st.markdown('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">', unsafe_allow_html=True)

# Session State for Navigation
if 'section' not in st.session_state:
    st.session_state.section = 'Home'

section_order = ["Home", "Experience", "Projects", "Skills", "Education", "Contact"]

def navigate_to(section):
    st.session_state.section = section

def render_navigation_buttons():
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 8, 1])
    
    current_index = section_order.index(st.session_state.section)
    
    with col1:
        if current_index > 0:
            prev_section = section_order[current_index - 1]
            st.button("⬅️ Prev", key="prev_btn", on_click=navigate_to, args=(prev_section,))
                
    with col3:
        if current_index < len(section_order) - 1:
            next_section = section_order[current_index + 1]
            st.button("Next ➡️", key="next_btn", on_click=navigate_to, args=(next_section,))

# Sidebar - Profile & Navigation
with st.sidebar:
    # Profile Image
    try:
        image = Image.open("assets/profile.jpg")
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
    try:
        with open("assets/resume.pdf", "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            st.download_button(
                label="📄 Download Resume",
                data=pdf_bytes,
                file_name="resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    except FileNotFoundError:
        pass

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
        <div class="glass-card">
            <h3>🚀 Experience</h3>
            <p>6+ Years in Full Stack & AI</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="glass-card">
            <h3>💡 Innovation</h3>
            <p>AI-Driven Solutions</p>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="glass-card">
            <h3>🎓 Education</h3>
            <p>B.E. Computer Science</p>
        </div>
        """, unsafe_allow_html=True)

def experience_section():
    st.markdown('<div class="section-header">Experience</div>', unsafe_allow_html=True)
    
    for job in pd.PORTFOLIO_DATA['experience']:
        st.markdown(f"""
        <div class="timeline-item">
            <h3 class="role-title">{job['role']}</h3>
            <h4 class="company-name">{job['company']}</h4>
            <p class="duration">{job['duration']}</p>
            <p>{job['description']}</p>
        </div>
        """, unsafe_allow_html=True)

def projects_section():
    st.markdown('<div class="section-header">Projects</div>', unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, project in enumerate(pd.PORTFOLIO_DATA['projects']):
        with cols[i % 2]:
            tech_stack_html = ' '.join([f'<span class="skill-pill" style="font-size: 0.8rem; padding: 4px 8px;">{tech}</span>' for tech in project['tech_stack']])
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="color: #00d4ff;">{project['title']}</h3>
                <p>{project['description']}</p>
                <div style="margin: 10px 0;">
                    {tech_stack_html}
                </div>
                <div style="margin-top: 15px;">
                    <a href="{project['link']}" target="_blank">View Project 🔗</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

def skills_section():
    st.markdown('<div class="section-header">Skills</div>', unsafe_allow_html=True)
    
    for category, skills in pd.PORTFOLIO_DATA['skills'].items():
        st.markdown(f"<div class='sub-header'>{category}</div>", unsafe_allow_html=True)
        skills_html = "".join([f"<span class='skill-pill'>{skill}</span>" for skill in skills])
        st.markdown(f"{skills_html}", unsafe_allow_html=True)

def education_section():
    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
    
    for edu in pd.PORTFOLIO_DATA['education']:
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color: #ffffff;">{edu['institution']}</h3>
            <h4 style="color: #00d4ff;">{edu['degree']}</h4>
            <p style="color: #aaaaaa; font-style: italic;">{edu['year']}</p>
            <p>{edu['description']}</p>
        </div>
        """, unsafe_allow_html=True)

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
            email = st.text_input("Email")
            message = st.text_area("Message")
            
            if st.form_submit_button("Send Message"):
                st.success("Message sent! (Demo)")

# Routing
if st.session_state.section == "Home":
    home_section()
elif st.session_state.section == "Experience":
    experience_section()
elif st.session_state.section == "Projects":
    projects_section()
elif st.session_state.section == "Skills":
    skills_section()
elif st.session_state.section == "Education":
    education_section()
elif st.session_state.section == "Contact":
    contact_section()

# Render Footer Navigation (Bottom of page logic)
render_navigation_buttons()

# Footer
st.markdown("---")
st.markdown(f"<div style='text-align: center; color: #555; font-size: 0.8rem;'>© 2026 {pd.PORTFOLIO_DATA['name']} | Built with Streamlit</div>", unsafe_allow_html=True)
