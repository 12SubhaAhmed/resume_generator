import streamlit as st
#import fitz
#from dotenv import load_dotenv
import os
#import google.generativeai as genai

# Load environment variables
load_dotenv()
google_api_key = os.getenv("GOOGLE_API_KEY")
if not google_api_key:
    raise ValueError("GOOGLE_API_KEY is not set. Please ensure it is defined in your .env file.")

# Load Gemini model
genai.configure(api_key=google_api_key)
model = genai.GenerativeModel('gemini-2.0-flash')

st.set_page_config(page_title="AI Resume Assistant", layout="centered")
st.markdown("<h1 style='text-align: center;'>💼 AI Resume Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px;'>Analyze and generate resumes with AI 🤖</p>", unsafe_allow_html=True)
st.markdown("---")

# Tabs for switching between analyzer and generator
tab1, tab2 = st.tabs(["📄 Analyze Resume", "📝 Generate Resume"])

#--------------- TAB-1: ANALYZE -----------------
with tab1:
    st.subheader("📄 Analyze your Resume")
    st.markdown("Choose how you want to input your resume:")
    option = st.radio("Select Input Method:", ["Paste Text", "Upload PDF"], key="analyze_method")
    resume_text = ""

    if option == 'Paste Text':
        resume_text = st.text_area("Paste your resume here:", height=300)

    elif option == 'Upload PDF':
        uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])
        if uploaded_file is not None:
            try:
                with fitz.open(stream=uploaded_file.read(), filetype='pdf') as docs:
                    for page in docs:
                        resume_text += page.get_text()
                st.success("✅ Resume text extracted successfully!")
                st.markdown("You can now click **Analyze Resume** to get AI feedback.")
            except Exception as e:
                st.error(f"❌ Failed to read PDF: {str(e)}")

    # Custom CSS for 3D Button inside tab1
    custom_css = """
        <style>
        div.stButton > button:first-child {
            background: linear-gradient(to right, #ff416c, #ff4b2b, #f9d423);
            color: white;
            padding: 12px 28px;
            border: none;
            border-radius: 10px;
            font-size: 16px;
            font-weight: bold
            transition: 0.3s ease-in-out;
        }
        div.stButton > button:first-child:hover {
            box-shadow: 0 8px 16px rgba(0,0,0,0.3);
            transform: scale(1.03);
        }

        div.stButton > button:first-child:active {
            box-shadow: 0 4px 6px rgba (0,0,0,0.2);
            transform: translateY(3px);
        }
        </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    if st.button("Analyze Resume"):
        if not resume_text.strip():
            st.warning("Please provide resume text or upload PDF first!")
        else:
            with st.spinner("Analyzing..."):
                prompt = f"""
You're a professional resume reviewer.

Please analyze the resume below and provide in short:
- Strengths
- Weaknesses
- Suggestions for improvement
- 1-line summary about this candidate

Resume:
{resume_text}
"""
                try:
                    response = model.generate_content(prompt)
                    st.success("✅ Resume Feedback:")
                    st.markdown(response.text.replace("\n", "\n\n"))  # Better spacing
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

#--------------- TAB-2: GENERATE -----------------
with tab2:
    st.subheader("📝 Generate a fresh resume with AI ✨")
    st.markdown("Fill in the details and let Gemini build your resume:")

    job_title = st.text_input("What job are you applying for?", placeholder="e.g. Frontend Developer")
    education = st.text_area("What is your education?", placeholder="e.g. Graduation")
    skills = st.text_area("What are your main skills?", placeholder="e.g. HTML, CSS, React, JavaScript")
    experience = st.text_area("Any experience or certifications?", placeholder="e.g. Internship at XYZ Company")

    if st.button("Generate Resume"):
        if not job_title.strip():
            st.warning("Please enter a job title.")
        else:
            with st.spinner("Generating Resume..."):
                gen_prompt = f"""
You're an expert resume writer.

Create a professional resume based on the details below using **Markdown formatting**. Use:
- `###` for section headings
- bullet points for skills
- bold for section titles

**Job Title** :{job_title}
**Education** : {education}
**Skills** : {skills}
**Experience/Certification** :{experience}

Please format the resume clearly with sections like:
- Objective
- Skills
- Experience
- Education
- Certifications (if any)
"""
                try:
                    response = model.generate_content(gen_prompt)
                    st.success("✅ Resume Generated:")
                    st.text_area("Your AI-Generated Resume:", value=response.text, height=400)
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

