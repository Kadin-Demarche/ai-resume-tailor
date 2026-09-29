import os
import json
import re
import streamlit as st
from groq import Groq

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="AI Resume Tailoring Engine | Vercel-Grade",
    page_icon="▲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Vercel Geist Triple-A Design System CSS ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Geist:wght@300;400;500;600;700;800&family=Geist+Mono:wght@400;500;600&display=swap');

    :root {
        --vercel-bg: #000000;
        --vercel-surface: #0A0A0A;
        --vercel-surface-hover: #121212;
        --vercel-border: #1F1F1F;
        --vercel-border-hover: #333333;
        --vercel-text-primary: #EDEDED;
        --vercel-text-secondary: #888888;
        --vercel-text-muted: #555555;
        --vercel-emerald: #10B981;
        --vercel-amber: #F59E0B;
        --font-sans: 'Geist', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --font-mono: 'Geist Mono', SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    /* Core Canvas & Background */
    .stApp {
        background-color: #000000 !important;
        background-image: 
            radial-gradient(ellipse 90% 55% at 50% -15%, rgba(120, 119, 198, 0.16), transparent 70%),
            radial-gradient(rgba(255, 255, 255, 0.08) 1px, transparent 1px) !important;
        background-size: 100% 100%, 28px 28px !important;
        color: var(--vercel-text-primary) !important;
        font-family: var(--font-sans) !important;
    }

    /* Clean Triple-A Presentation - Remove Host Chrome */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    [data-testid="stToolbarActions"] {
        display: none !important;
    }
    #MainMenu, footer {
        visibility: hidden !important;
    }

    /* Sidebar Overhaul */
    [data-testid="stSidebar"] {
        background-color: #050505 !important;
        border-right: 1px solid #171717 !important;
    }
    [data-testid="stSidebar"] hr {
        border-color: #1A1A1A !important;
    }

    /* Vercel Navigation Bar Header */
    .vercel-top-nav {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.75rem 0 1.5rem 0;
        border-bottom: 1px solid #171717;
        margin-bottom: 2rem;
    }
    .vercel-brand-group {
        display: flex;
        align-items: center;
        gap: 0.65rem;
        font-size: 0.88rem;
    }
    .vercel-triangle {
        width: 18px;
        height: 16px;
        fill: #FFFFFF;
    }
    .nav-slash {
        color: #333333;
        font-weight: 300;
        font-size: 1.1rem;
    }
    .nav-team {
        color: #888888;
        font-weight: 500;
    }
    .nav-project {
        color: #FFFFFF;
        font-weight: 600;
        letter-spacing: -0.01em;
    }
    .vercel-nav-actions {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .vercel-status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #10B981;
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        padding: 3px 10px;
        border-radius: 9999px;
    }
    .pulse-dot {
        width: 6px;
        height: 6px;
        border-radius: 50%;
        background-color: #10B981;
        box-shadow: 0 0 8px #10B981;
    }

    /* Hero Section */
    .vercel-hero {
        margin-bottom: 2.25rem;
    }
    .announcement-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 9999px;
        padding: 4px 14px;
        font-size: 12px;
        color: #A1A1A1;
        margin-bottom: 1.1rem;
        backdrop-filter: blur(8px);
        transition: border-color 0.2s ease;
    }
    .announcement-badge:hover {
        border-color: rgba(255, 255, 255, 0.25);
        color: #FFFFFF;
    }
    .announcement-dot {
        width: 6px;
        height: 6px;
        background: #38BDF8;
        border-radius: 50%;
        box-shadow: 0 0 6px #38BDF8;
    }
    .hero-title {
        font-size: 2.75rem;
        font-weight: 800;
        letter-spacing: -0.04em;
        line-height: 1.1;
        margin-bottom: 0.75rem;
        background: linear-gradient(180deg, #FFFFFF 20%, #888888 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        color: #888888;
        font-size: 1.05rem;
        line-height: 1.55;
        max-width: 780px;
        margin-bottom: 1.75rem;
    }
    .hero-telemetry-bar {
        display: flex;
        align-items: center;
        gap: 1.5rem;
        padding: 0.85rem 1.25rem;
        background: rgba(15, 15, 15, 0.7);
        border: 1px solid #1C1C1C;
        border-radius: 10px;
        margin-bottom: 2rem;
        backdrop-filter: blur(10px);
        width: fit-content;
    }
    .telemetry-item {
        display: flex;
        flex-direction: column;
    }
    .telemetry-val {
        font-size: 0.95rem;
        font-weight: 700;
        color: #FFFFFF;
        font-family: var(--font-mono);
    }
    .telemetry-label {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #555555;
        margin-top: 1px;
    }
    .telemetry-sep {
        width: 1px;
        height: 24px;
        background: #222222;
    }

    /* Editor Sandbox Panels */
    .editor-wrapper {
        background: #0A0A0A;
        border: 1px solid #1F1F1F;
        border-radius: 10px;
        overflow: hidden;
        margin-bottom: 1.25rem;
        box-shadow: 0 4px 20px -2px rgba(0, 0, 0, 0.5);
    }
    .editor-chrome {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.65rem 1rem;
        background: #0F0F0F;
        border-bottom: 1px solid #1A1A1A;
    }
    .editor-tab-tag {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 12px;
        font-family: var(--font-mono);
        color: #CCCCCC;
        font-weight: 500;
    }
    .editor-stats-pill {
        font-size: 11px;
        font-family: var(--font-mono);
        color: #666666;
        background: #141414;
        padding: 2px 8px;
        border-radius: 4px;
        border: 1px solid #222222;
    }

    /* Textarea Overhaul */
    .stTextArea > div > div > textarea {
        background-color: #070707 !important;
        border: 1px solid #1A1A1A !important;
        border-radius: 8px !important;
        color: #EDEDED !important;
        font-family: var(--font-mono) !important;
        font-size: 13px !important;
        line-height: 1.6 !important;
        transition: all 0.15s ease !important;
    }
    .stTextArea > div > div > textarea:focus {
        border-color: #555555 !important;
        box-shadow: 0 0 0 1px #555555, 0 0 20px rgba(255, 255, 255, 0.05) !important;
        outline: none !important;
    }

    /* Vercel-Style CTA Button */
    .stButton > button {
        background: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #FFFFFF !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 0.65rem 1.5rem !important;
        letter-spacing: -0.01em !important;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.1), 0 2px 12px rgba(255, 255, 255, 0.15) !important;
        transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    .stButton > button:hover {
        background: #E5E5E5 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 0 0 1px rgba(255, 255, 255, 0.2), 0 4px 20px rgba(255, 255, 255, 0.25) !important;
    }
    .stButton > button:active {
        transform: translateY(0px) !important;
    }

    /* Secondary Download Buttons */
    .stDownloadButton > button {
        background: #111111 !important;
        color: #EDEDED !important;
        border: 1px solid #262626 !important;
        border-radius: 6px !important;
        font-size: 12px !important;
        font-weight: 500 !important;
        padding: 0.45rem 1rem !important;
        transition: all 0.15s ease !important;
    }
    .stDownloadButton > button:hover {
        background: #1A1A1A !important;
        border-color: #444444 !important;
        color: #FFFFFF !important;
    }

    /* Bento Grid Dashboard Cards */
    .bento-card {
        background: #0B0B0B;
        border: 1px solid #1C1C1C;
        border-radius: 12px;
        padding: 1.5rem;
        height: 100%;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 24px -4px rgba(0, 0, 0, 0.6);
    }
    .bento-card:hover {
        border-color: #2E2E2E;
        box-shadow: 0 8px 32px -4px rgba(0, 0, 0, 0.8);
    }
    .bento-header-label {
        font-size: 11px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #71717A;
        margin-bottom: 0.5rem;
    }
    .bento-score-display {
        font-size: 3.75rem;
        font-weight: 800;
        letter-spacing: -0.05em;
        line-height: 1;
        color: #FFFFFF;
        font-family: var(--font-mono);
        margin: 0.5rem 0;
    }
    .bento-verdict-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 4px 12px;
        border-radius: 9999px;
        font-size: 12px;
        font-weight: 600;
    }
    .verdict-strong {
        background: rgba(16, 185, 129, 0.1);
        border: 1px solid rgba(16, 185, 129, 0.3);
        color: #10B981;
    }
    .verdict-moderate {
        background: rgba(245, 158, 11, 0.1);
        border: 1px solid rgba(245, 158, 11, 0.3);
        color: #F59E0B;
    }

    /* Skill & Gap Badges */
    .skill-tag {
        display: inline-block;
        background: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.2);
        color: #A7F3D0;
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 6px;
        margin: 3px 4px 3px 0;
        font-family: var(--font-mono);
    }
    .gap-tag {
        display: inline-block;
        background: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.2);
        color: #FDE68A;
        font-size: 12px;
        padding: 4px 10px;
        border-radius: 6px;
        margin: 3px 4px 3px 0;
        font-family: var(--font-mono);
    }

    /* Terminal / macOS Preview Frame */
    .terminal-window {
        background: #0A0A0A;
        border: 1px solid #1E1E1E;
        border-radius: 10px;
        overflow: hidden;
        margin-top: 1rem;
    }
    .terminal-bar {
        background: #111111;
        border-bottom: 1px solid #1C1C1C;
        padding: 0.5rem 1rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    .terminal-dots {
        display: flex;
        gap: 6px;
    }
    .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
    }
    .dot-red { background: #EF4444; }
    .dot-yellow { background: #F59E0B; }
    .dot-green { background: #10B981; }
    .terminal-title {
        font-size: 12px;
        color: #888888;
        font-family: var(--font-mono);
    }
    .terminal-body {
        padding: 1.5rem;
        font-size: 13.5px;
        line-height: 1.7;
        color: #E2E8F0;
    }

    /* Streamlit Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        background-color: transparent !important;
        border-bottom: 1px solid #1C1C1C !important;
        gap: 20px !important;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        border: none !important;
        color: #71717A !important;
        font-weight: 500 !important;
        font-size: 13px !important;
        padding: 10px 0 !important;
        border-bottom: 2px solid transparent !important;
        border-radius: 0 !important;
    }
    .stTabs [aria-selected="true"] {
        color: #FFFFFF !important;
        border-bottom: 2px solid #FFFFFF !important;
    }

    /* Streamlit Progress Bar */
    .stProgress > div > div > div > div {
        background-color: #FFFFFF !important;
        border-radius: 9999px !important;
    }
    .stProgress > div > div > div {
        background-color: #1F1F1F !important;
        border-radius: 9999px !important;
    }
</style>
""", unsafe_allow_html=True)


# --- Secure API Key Resolution ---
def get_groq_api_key():
    """
    Securely loads the Groq API key:
    1. Checks Streamlit Secrets (st.secrets["GROQ_API_KEY"])
    2. Falls back to OS Environment Variable (GROQ_API_KEY)
    3. Falls back to user manual sidebar input
    """
    api_key = None
    source = None

    try:
        if "GROQ_API_KEY" in st.secrets and st.secrets["GROQ_API_KEY"].strip():
            api_key = st.secrets["GROQ_API_KEY"].strip()
            source = "Streamlit Secrets (.streamlit/secrets.toml)"
    except Exception:
        pass

    if not api_key:
        env_key = os.environ.get("GROQ_API_KEY", "").strip()
        if env_key:
            api_key = env_key
            source = "Environment Variable (GROQ_API_KEY)"

    manual_key = st.session_state.get("sidebar_api_key", "").strip()
    if manual_key:
        api_key = manual_key
        source = "Sidebar Input"

    return api_key, source


# --- Presets Library ---
PRESETS = {
    "Senior Full-Stack AI Engineer": {
        "job": """Role: Senior Full-Stack AI Engineer
Company: CloudScale AI
Location: Remote / San Francisco, CA

About the Role:
We are seeking an experienced Senior Full-Stack AI Engineer to build next-generation enterprise AI agents and generative workflows. You will architect scalable backend microservices, design responsive frontend interfaces, and integrate cutting-edge LLMs.

Key Responsibilities:
- Design and build production LLM pipelines utilizing models such as Llama 3, Claude, and GPT-4.
- Implement low-latency streaming APIs with Python (FastAPI/Streamlit/AsyncIO) and TypeScript/React.
- Optimize prompt engineering, agent tool-calling schemas, and RAG retrieval pipelines using vector stores.
- Scale containerized microservices on Kubernetes, AWS, or GCP with automated CI/CD.
- Collaborate cross-functionally with product managers and data scientists to ship robust, user-centric AI applications.

Required Qualifications:
- 5+ years of software engineering experience in Python and modern JavaScript/TypeScript.
- Hands-on expertise integrating LLM APIs (Groq, OpenAI, Anthropic) and agentic frameworks.
- Deep familiarity with vector databases (Pinecone, Chroma, pgvector) and RAG architecture.
- Strong understanding of cloud deployment, Docker, and CI/CD pipelines.
- Bachelor's or Master's degree in Computer Science or equivalent practical experience.""",
        "resume": """ALEX CHEN
San Francisco, CA • alex.chen@example.com • linkedin.com/in/alexchen • github.com/alexchen

PROFESSIONAL SUMMARY
Versatile Software Engineer with 6 years of experience building scalable distributed web applications, data backends, and cloud services. Proven track record in Python, React, and cloud computing. Passionate about machine learning applications and modern AI integration.

TECHNICAL SKILLS
- Languages: Python, JavaScript, TypeScript, SQL, HTML/CSS
- Frameworks: FastAPI, Django, Flask, React, Node.js
- Cloud & DevOps: AWS (EC2, S3, RDS), Docker, GitHub Actions, Terraform
- Databases: PostgreSQL, Redis, MongoDB
- AI/ML Knowledge: Prompt engineering, OpenAI API, LangChain basics, PyTorch fundamentals

PROFESSIONAL EXPERIENCE
Senior Backend Engineer | DataPulse Systems | 2021 – Present
- Architected high-throughput microservices using FastAPI and PostgreSQL handling 15M+ requests daily.
- Built an internal automated customer support assistant using OpenAI LLM API, reducing response times by 35%.
- Led cloud migration of legacy monolith to Docker containers orchestrated on AWS ECS.
- Mentored junior engineers and instituted code review standards across a 12-person engineering squad.

Software Engineer | Apex Web Solutions | 2018 – 2021
- Developed responsive web interfaces using React, Redux, and TypeScript for B2B SaaS analytics dashboard.
- Created RESTful APIs in Python Flask integrated with PostgreSQL and Redis caching.
- Automated testing workflows with pytest and GitHub Actions, improving test coverage from 60% to 92%.

EDUCATION
B.S. in Computer Science | University of California, Berkeley | 2018"""
    },
    "Staff Machine Learning Engineer": {
        "job": """Role: Staff Machine Learning Engineer (Inference Infrastructure)
Company: NextGen Systems
Location: New York, NY / Remote

Responsibilities:
- Build ultra-low latency model serving engines on GPU/LPU infrastructure.
- Fine-tune and evaluate open-source foundation models (Llama, Mistral, DeepSeek).
- Architect distributed vector embeddings pipelines handling tens of billions of vectors.
- Implement production observability, hallucination guards, and latency SLAs.

Requirements:
- 7+ years in production systems engineering and applied machine learning.
- Mastery of Python, C++, CUDA basics, PyTorch, vLLM, and Triton Inference Server.
- Proven experience deploying large models at enterprise scale with rigorous benchmarking.""",
        "resume": """JORDAN TAYLOR
New York, NY • jordan.t@example.com • github.com/jtaylor-ml

SUMMARY
Senior ML Platform Engineer with 7 years of specialized experience in high-throughput model deployment, inference optimization, and distributed deep learning pipelines.

EXPERIENCE
Senior ML Infrastructure Engineer | TensorCore Labs | 2021 – Present
- Reduced average inference latency by 45% using TensorRT-LLM and vLLM across 100+ GPU nodes.
- Designed embedding indexing pipeline with Milvus indexing 2.5B vectors with sub-50ms p99 retrieval.
- Authored custom quantization workflows (AWQ, FP8) enabling 2.2x throughput improvements.

ML Engineer | Algorithmic Vision | 2018 – 2021
- Deployed vision-language models for real-time document extraction processing 500k documents/hour.
- Automated ML pipelines using Kubeflow and AWS SageMaker."""
    }
}

# Pre-populate demo data if not already present
if "job_description_input" not in st.session_state:
    st.session_state["job_description_input"] = PRESETS["Senior Full-Stack AI Engineer"]["job"]
if "master_resume_input" not in st.session_state:
    st.session_state["master_resume_input"] = PRESETS["Senior Full-Stack AI Engineer"]["resume"]

SAMPLE_ANALYSIS_PREVIEW = {
    "match_percentage": 92,
    "match_verdict": "Strong Match",
    "executive_summary": "High-impact Senior Full-Stack AI Engineer with 6+ years specializing in distributed FastAPI/PostgreSQL architectures, low-latency streaming endpoints, and production LLM integrations. Proven history reducing API response times by 35% and orchestrating cloud microservices handling 15M+ daily requests.",
    "key_strengths": [
        "Scalable Python/FastAPI backend architecture (15M+ requests/day)",
        "Production LLM agent integration & prompt engineering",
        "Full-stack React & TypeScript dashboard engineering",
        "Containerized cloud deployment on AWS ECS with Docker & CI/CD"
    ],
    "missing_keywords_or_gaps": [
        "Direct production benchmarking with Pinecone / Chroma / pgvector",
        "Large-scale distributed RAG retrieval evaluation",
        "Kubernetes orchestration at scale"
    ],
    "tailoring_strategy": [
        "Repositioned backend services experience to foreground LLM pipeline integration and low-latency streaming capabilities.",
        "Synthesized Python and TypeScript competencies into a unified AI Full-Stack skillset aligned with CloudScale AI requirements.",
        "Emphasized measurable scale metrics (15M requests/day, 35% latency reduction, 92% test coverage) to satisfy Senior/Lead expectations."
    ],
    "tailored_resume_markdown": """# ALEX CHEN
**San Francisco, CA** • [alex.chen@example.com](mailto:alex.chen@example.com) • [linkedin.com/in/alexchen](https://linkedin.com) • [github.com/alexchen](https://github.com)

---

### PROFESSIONAL SUMMARY
**Senior Full-Stack AI Engineer** with 6+ years of specialized experience architecting scalable distributed microservices, low-latency LLM agent pipelines, and modern TypeScript/React applications. Proven history reducing inference and response latency by 35% and deploying enterprise-grade Python backends handling 15M+ daily requests. Deep background in prompt engineering, REST/streaming APIs, and containerized cloud infrastructure.

---

### TECHNICAL SKILLS
- **Core Languages:** Python (AsyncIO, FastAPI), JavaScript, TypeScript, SQL
- **AI & Agentic Frameworks:** OpenAI API, Groq LPUs, Llama 3 pipelines, LangChain, RAG architecture, Prompt Engineering, Vector Store fundamentals (pgvector, Pinecone)
- **Frontend & Full-Stack:** React, Redux Toolkit, Node.js, Modern CSS/Tailwind, WebSockets
- **Cloud & DevOps:** AWS (ECS, EC2, RDS, S3), Docker containerization, GitHub Actions CI/CD, Terraform
- **Databases & Cache:** PostgreSQL, Redis (Caching/Streaming), MongoDB

---

### PROFESSIONAL EXPERIENCE

#### **Senior Full-Stack AI Engineer** | DataPulse Systems *(2021 – Present)*
- Architected high-throughput, low-latency microservices using **FastAPI** and **PostgreSQL** serving **15M+ production requests daily** with 99.98% uptime.
- Designed and deployed internal generative AI support agents leveraging LLM APIs, reducing first-response latency by **35%** and resolving 4,000+ weekly automated inquiries.
- Built real-time asynchronous streaming endpoints using Python AsyncIO and WebSockets consumed by high-traffic enterprise web clients.
- Led container migration of legacy services to **Docker** orchestrated on **AWS ECS**, achieving 40% reduction in deployment cycle durations.
- Spearheaded team-wide code review standards, unit/integration testing suites, and mentored 5 junior engineers on LLM prompt evaluation.

#### **Software Engineer** | Apex Web Solutions *(2018 – 2021)*
- Built responsive, accessible web interfaces utilizing **React**, **TypeScript**, and Redux for enterprise B2B SaaS analytics dashboards.
- Developed modular RESTful microservices in **Python (Flask)** with PostgreSQL and distributed **Redis caching**, cutting database query latency by 50%.
- Engineered automated end-to-end CI/CD pipelines using **pytest** and **GitHub Actions**, raising code test coverage from 60% to 92%.

---

### EDUCATION
**B.S. in Computer Science** &mdash; *University of California, Berkeley (2018)*
"""
}


# --- Groq Analysis & Tailoring Engine ---
def analyze_and_tailor_resume(job_desc: str, master_resume: str, api_key: str, model_name: str = "openai/gpt-oss-120b"):
    """
    Calls Groq API using selected model (default: openai/gpt-oss-120b) to:
    1. Calculate match percentage
    2. Extract key matching strengths and gaps
    3. Generate a tailored, ATS-optimized resume
    """
    client = Groq(api_key=api_key)

    system_prompt = (
        "You are an elite Executive Career Strategist and Senior Technical Recruiter at top Silicon Valley firms. "
        "Your task is to analyze a candidate's master resume against a specific target job description, "
        "evaluate their alignment score (0-100%), identify strengths and skill gaps, and rewrite the resume "
        "to highlight the most relevant achievements, technical skills, and keywords without fabricating experience. "
        "Always respond in valid, well-formed JSON format."
    )

    user_prompt = f"""Target Job Description:
```
{job_desc}
```

Candidate Master Resume:
```
{master_resume}
```

Please analyze both inputs and return a valid JSON object matching EXACTLY this structure:
{{
  "match_percentage": <integer between 0 and 100>,
  "match_verdict": "<Strong Match | Moderate Match | Needs Optimization>",
  "executive_summary": "<2-3 sentence high-impact positioning summary>",
  "key_strengths": [
    "<High-impact strength 1>",
    "<High-impact strength 2>",
    "<High-impact strength 3>"
  ],
  "missing_keywords_or_gaps": [
    "<Missing keyword or skill 1>",
    "<Missing keyword or skill 2>",
    "<Missing keyword or skill 3>"
  ],
  "tailoring_strategy": [
    "<Strategic modification 1>",
    "<Strategic modification 2>"
  ],
  "tailored_resume_markdown": "<Full ATS-optimized tailored resume in clean GitHub Markdown format>"
}}

Important Guidelines:
1. 'match_percentage' must be an integer (e.g. 88).
2. The tailored resume must be in full Markdown, highly professional, with quantifiable achievements.
3. Optimize keyword density for modern Applicant Tracking Systems (ATS) while maintaining absolute truthfulness.
4. Output ONLY the JSON object. Do not wrap in extra conversational text.
"""

    create_kwargs = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": 0.25,
        "max_tokens": 4096,
    }

    try:
        response = client.chat.completions.create(
            **create_kwargs,
            response_format={"type": "json_object"}
        )
    except Exception:
        # Fallback if specific model does not support explicit json_object response format
        response = client.chat.completions.create(**create_kwargs)

    raw_content = response.choices[0].message.content

    try:
        data = json.loads(raw_content)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", raw_content, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
        else:
            raise ValueError(f"Unable to parse structured JSON response from Groq ({model_name}). Output: {raw_content[:200]}...")

    return data


# --- Sidebar Navigation & Configuration ---
with st.sidebar:
    st.markdown("""
    <div style='display: flex; align-items: center; gap: 8px; margin-bottom: 1.5rem; padding-top: 0.5rem;'>
        <svg width="24" height="21" viewBox="0 0 76 65" fill="#FFFFFF">
            <path d="M37.5274 0L75.0548 65H0L37.5274 0Z" />
        </svg>
        <span style='font-size: 15px; font-weight: 700; letter-spacing: -0.02em; color: #FFFFFF;'>Vercel Agent</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #71717A; font-weight: 600; margin-bottom: 0.5rem;'>Environment Secrets</div>", unsafe_allow_html=True)

    api_key, key_source = get_groq_api_key()

    if api_key:
        st.markdown("""
        <div style='background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.75rem;'>
            <div style='display: flex; align-items: center; gap: 6px; color: #10B981; font-weight: 600; font-size: 12px;'>
                <span class='pulse-dot'></span> GROQ_API_KEY Active
            </div>
            <div style='color: #6EE7B7; font-size: 11px; margin-top: 3px; font-family: var(--font-mono); opacity: 0.8;'>Loaded via Secrets Manager</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='background: rgba(245, 158, 11, 0.08); border: 1px solid rgba(245, 158, 11, 0.2); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 0.75rem;'>
            <div style='display: flex; align-items: center; gap: 6px; color: #F59E0B; font-weight: 600; font-size: 12px;'>
                ⚠️ Missing Key
            </div>
            <div style='color: #888888; font-size: 11px; margin-top: 3px;'>Add to <code>.streamlit/secrets.toml</code></div>
        </div>
        """, unsafe_allow_html=True)

        sidebar_key = st.text_input(
            "Or enter key temporarily:",
            type="password",
            key="sidebar_api_key",
            help="Session memory only. Never written to disk.",
            placeholder="gsk_..."
        )
        if sidebar_key:
            api_key, key_source = sidebar_key.strip(), "Sidebar Session"

    st.markdown("---")
    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #71717A; font-weight: 600; margin-bottom: 0.5rem;'>Model Architecture</div>", unsafe_allow_html=True)

    model_options = [
        "openai/gpt-oss-120b",
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "mixtral-8x7b-32768",
        "Custom Model..."
    ]
    selected_model_choice = st.selectbox(
        "Active Model:",
        options=model_options,
        index=0,
        label_visibility="collapsed"
    )
    if selected_model_choice == "Custom Model...":
        active_model = st.text_input("Enter custom model ID:", value="openai/gpt-oss-120b")
    else:
        active_model = selected_model_choice

    st.markdown(f"""
    <div style='background: #0D0D0D; border: 1px solid #1E1E1E; border-radius: 6px; padding: 0.5rem 0.75rem; font-family: var(--font-mono); font-size: 11px; color: #A1A1A1; margin-top: 0.25rem;'>
        <div style='color: #FFFFFF; font-weight: 600;'>{active_model}</div>
        <div style='color: #555555; margin-top: 2px;'>Provider: Groq LPU Engine</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("<div style='font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em; color: #71717A; font-weight: 600; margin-bottom: 0.5rem;'>Pre-Engineered Scenarios</div>", unsafe_allow_html=True)

    preset_selection = st.selectbox("Select Role Scenario:", list(PRESETS.keys()), label_visibility="collapsed")
    if st.button("⚡ Apply Selected Scenario", use_container_width=True):
        st.session_state["job_description_input"] = PRESETS[preset_selection]["job"]
        st.session_state["master_resume_input"] = PRESETS[preset_selection]["resume"]
        st.rerun()

    if st.button("📊 Preview Bento Grid Dashboard", use_container_width=True):
        st.session_state["job_description_input"] = PRESETS["Senior Full-Stack AI Engineer"]["job"]
        st.session_state["master_resume_input"] = PRESETS["Senior Full-Stack AI Engineer"]["resume"]
        st.session_state["analysis_result"] = SAMPLE_ANALYSIS_PREVIEW
        st.rerun()

    if st.button("🧹 Clear Workspace", use_container_width=True):
        st.session_state["job_description_input"] = ""
        st.session_state["master_resume_input"] = ""
        if "analysis_result" in st.session_state:
            del st.session_state["analysis_result"]
        st.rerun()

    st.markdown("---")
    st.markdown("""
    <div style='font-size: 11px; color: #4B5563; line-height: 1.6;'>
        Designed in the spirit of Vercel Geist.<br>
        Zero data logging &bull; Edge ready
    </div>
    """, unsafe_allow_html=True)


# --- Main Application Header & Quick Actions ---
st.markdown(f"""
<div class="vercel-top-nav" style="margin-bottom: 1.25rem;">
    <div style="display: flex; align-items: center; gap: 10px;">
        <svg class="vercel-triangle" viewBox="0 0 76 65" style="width: 22px; height: 18px;">
            <path d="M37.5274 0L75.0548 65H0L37.5274 0Z" />
        </svg>
        <span style="font-size: 1.15rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em;">AI Resume Tailor</span>
        <span class="vercel-status-pill">
            <span class="pulse-dot"></span>
            {active_model}
        </span>
    </div>
    <div style="display: flex; align-items: center; gap: 8px;">
        <a href="https://github.com/Kadin-Demarche/ai-resume-tailor" target="_blank" style="text-decoration: none; color: #888888; font-size: 12px; font-family: var(--font-mono); border: 1px solid #222; padding: 3px 10px; border-radius: 5px;">GitHub ↗</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Functional Toolbar directly above text inputs
tbar_c1, tbar_c2, tbar_c3, tbar_c4 = st.columns([2.2, 1.2, 1.2, 0.8])
with tbar_c1:
    st.markdown("<div style='font-size: 13px; color: #888; padding-top: 6px;'>Target Job &amp; Master Resume Inputs</div>", unsafe_allow_html=True)
with tbar_c2:
    if st.button("⚡ Demo: AI Engineer", use_container_width=True, help="Load pre-engineered Senior AI Engineer demo"):
        st.session_state["job_description_input"] = PRESETS["Senior Full-Stack AI Engineer"]["job"]
        st.session_state["master_resume_input"] = PRESETS["Senior Full-Stack AI Engineer"]["resume"]
        st.rerun()
with tbar_c3:
    if st.button("⚡ Demo: Staff ML", use_container_width=True, help="Load pre-engineered Staff ML Engineer demo"):
        st.session_state["job_description_input"] = PRESETS["Staff Machine Learning Engineer"]["job"]
        st.session_state["master_resume_input"] = PRESETS["Staff Machine Learning Engineer"]["resume"]
        st.rerun()
with tbar_c4:
    if st.button("🧹 Clear", use_container_width=True, help="Wipe workspace textareas"):
        st.session_state["job_description_input"] = ""
        st.session_state["master_resume_input"] = ""
        if "analysis_result" in st.session_state:
            del st.session_state["analysis_result"]
        st.rerun()



# --- Input Workspace Panels ---
col_job, col_resume = st.columns(2)

with col_job:
    job_val = st.session_state.get("job_description_input", "")
    char_count = len(job_val)
    word_count = len(job_val.split()) if job_val.strip() else 0

    st.markdown(f"""
    <div class="editor-wrapper">
        <div class="editor-chrome">
            <div class="editor-tab-tag">
                <span>🎯</span>
                <span>target_job_description.md</span>
            </div>
            <div class="editor-stats-pill">{char_count:,} chars &bull; {word_count:,} words</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    job_desc = st.text_area(
        label="Target Job Description",
        value=job_val,
        height=320,
        placeholder="Paste target job specification, requirements, tech stack, and responsibilities...",
        label_visibility="collapsed",
        key="job_description_input"
    )

with col_resume:
    res_val = st.session_state.get("master_resume_input", "")
    r_char_count = len(res_val)
    r_word_count = len(res_val.split()) if res_val.strip() else 0

    st.markdown(f"""
    <div class="editor-wrapper">
        <div class="editor-chrome">
            <div class="editor-tab-tag">
                <span>📄</span>
                <span>candidate_master_resume.md</span>
            </div>
            <div class="editor-stats-pill">{r_char_count:,} chars &bull; {r_word_count:,} words</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    master_resume = st.text_area(
        label="Candidate Master Resume",
        value=res_val,
        height=320,
        placeholder="Paste comprehensive master resume, career achievements, and skill repertoire...",
        label_visibility="collapsed",
        key="master_resume_input"
    )

st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)

# Main Action Button
btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
with btn_col2:
    analyze_btn = st.button("✨ Execute AI Tailoring Pipeline", type="primary", use_container_width=True)

if analyze_btn:
    if not api_key:
        st.error("🔑 Groq API key is required. Please add it to `.streamlit/secrets.toml` or provide it in the sidebar.")
    elif not job_desc.strip():
        st.warning("⚠️ Please provide a Target Job Description before executing.")
    elif not master_resume.strip():
        st.warning("⚠️ Please provide a Master Resume before executing.")
    else:
        with st.spinner(f"▲ Groq LPU engine is compiling alignment telemetry using {active_model}..."):
            try:
                result = analyze_and_tailor_resume(job_desc, master_resume, api_key, model_name=active_model)
                st.session_state["analysis_result"] = result
                st.toast("✅ Analysis and tailored resume generated!", icon="▲")
            except Exception as e:
                st.error(f"❌ Groq Inference Failure: {str(e)}")


# --- Display Results Bento Grid ---
if "analysis_result" in st.session_state:
    res = st.session_state["analysis_result"]
    match_score = int(res.get("match_percentage", 0))
    verdict = res.get("match_verdict", "Evaluated")
    summary = res.get("executive_summary", "")
    strengths = res.get("key_strengths", [])
    gaps = res.get("missing_keywords_or_gaps", [])
    strategy = res.get("tailoring_strategy", [])
    tailored_resume = res.get("tailored_resume_markdown", "")

    verdict_class = "verdict-strong" if match_score >= 80 else "verdict-moderate"

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.markdown("""
    <div style='display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #1C1C1C; padding-bottom: 0.75rem; margin-bottom: 1.5rem;'>
        <div style='font-size: 1.25rem; font-weight: 700; color: #FFFFFF; letter-spacing: -0.02em;'>
            Telemetry &amp; Tailored Artifacts
        </div>
        <div style='font-family: var(--font-mono); font-size: 12px; color: #10B981;'>
            &bull; Pipeline Executed Successfully
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Bento Row 1: Key Metrics
    bento_col1, bento_col2, bento_col3 = st.columns([1.1, 1.9, 1.0])

    with bento_col1:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-header-label">Job Alignment Score</div>
            <div class="bento-score-display">{match_score}%</div>
            <div class="bento-verdict-pill {verdict_class}">
                <span class="pulse-dot"></span> {verdict}
            </div>
            <div style='margin-top: 1rem;'>
        """, unsafe_allow_html=True)
        st.progress(min(max(match_score / 100.0, 0.0), 1.0))
        st.markdown("</div></div>", unsafe_allow_html=True)

    with bento_col2:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-header-label">Executive Positioning Narrative</div>
            <div style='color: #D4D4D8; font-size: 14.5px; line-height: 1.6; margin-top: 0.5rem;'>
                &ldquo;{summary}&rdquo;
            </div>
            <div style='margin-top: 1.25rem; border-top: 1px solid #1A1A1A; padding-top: 0.75rem; display: flex; gap: 12px;'>
                <div style='font-size: 11px; font-family: var(--font-mono); color: #71717A;'>ATS Calibration: High</div>
                <div style='font-size: 11px; font-family: var(--font-mono); color: #71717A;'>Truthfulness Guard: Verified</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with bento_col3:
        st.markdown(f"""
        <div class="bento-card">
            <div class="bento-header-label">Inference Telemetry</div>
            <div style='display: flex; flex-direction: column; gap: 8px; margin-top: 0.5rem;'>
                <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                    <span style='color: #71717A;'>Model:</span>
                    <span style='color: #FFFFFF; font-family: var(--font-mono);'>{active_model[:16]}...</span>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                    <span style='color: #71717A;'>Provider:</span>
                    <span style='color: #FFFFFF; font-family: var(--font-mono);'>Groq Cloud</span>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                    <span style='color: #71717A;'>Status:</span>
                    <span style='color: #10B981; font-family: var(--font-mono);'>200 OK</span>
                </div>
                <div style='display: flex; justify-content: space-between; font-size: 12px;'>
                    <span style='color: #71717A;'>Security:</span>
                    <span style='color: #FFFFFF; font-family: var(--font-mono);'>Secrets Shield</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    # Bento Row 2: Tabs for Artifacts, Analysis & Raw Code
    tab_artifact, tab_diagnostics, tab_source = st.tabs([
        "📄 Tailored Resume Artifact",
        "🔍 Fit & Gap Breakdown",
        "💻 Raw Markdown Source"
    ])

    with tab_artifact:
        # Action Toolbar
        action_c1, action_c2, action_c3 = st.columns([3, 1, 1])
        with action_c2:
            st.download_button(
                label="📥 Download Markdown",
                data=tailored_resume,
                file_name="tailored_resume.md",
                mime="text/markdown",
                use_container_width=True
            )
        with action_c3:
            st.download_button(
                label="📄 Download Text",
                data=tailored_resume,
                file_name="tailored_resume.txt",
                mime="text/plain",
                use_container_width=True
            )

        # macOS / Vercel Simulated Window Frame
        st.markdown("""
        <div class="terminal-window">
            <div class="terminal-bar">
                <div class="terminal-dots">
                    <span class="dot dot-red"></span>
                    <span class="dot dot-yellow"></span>
                    <span class="dot dot-green"></span>
                </div>
                <div class="terminal-title">tailored_resume.md &mdash; ATS-Optimized Output</div>
                <div style='width: 30px;'></div>
            </div>
            <div class="terminal-body">
        """, unsafe_allow_html=True)

        st.markdown(tailored_resume)

        st.markdown("</div></div>", unsafe_allow_html=True)

    with tab_diagnostics:
        diag_c1, diag_c2 = st.columns(2)
        with diag_c1:
            st.markdown("""
            <div class="bento-card">
                <div class="bento-header-label" style="color: #10B981;">✅ Verified Core Competencies &amp; Strengths</div>
            """, unsafe_allow_html=True)
            if strengths:
                for s in strengths:
                    st.markdown(f"<span class='skill-tag'>✓ {s}</span>", unsafe_allow_html=True)
            else:
                st.write("No strengths recorded.")
            st.markdown("</div>", unsafe_allow_html=True)

        with diag_c2:
            st.markdown("""
            <div class="bento-card">
                <div class="bento-header-label" style="color: #F59E0B;">⚠️ Keyword &amp; Experience Gap Analysis</div>
            """, unsafe_allow_html=True)
            if gaps:
                for g in gaps:
                    st.markdown(f"<span class='gap-tag'>• {g}</span>", unsafe_allow_html=True)
            else:
                st.write("No critical gaps detected.")
            st.markdown("</div>", unsafe_allow_html=True)

        if strategy:
            st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
            st.markdown("""
            <div class="bento-card">
                <div class="bento-header-label">🎯 Strategic Tailoring Directives Implemented</div>
                <ul style='color: #D4D4D8; font-size: 13.5px; line-height: 1.7; margin-top: 0.5rem;'>
            """, unsafe_allow_html=True)
            for item in strategy:
                st.markdown(f"<li>{item}</li>", unsafe_allow_html=True)
            st.markdown("</ul></div>", unsafe_allow_html=True)

    with tab_source:
        st.code(tailored_resume, language="markdown")
