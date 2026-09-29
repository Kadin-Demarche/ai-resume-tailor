# AI Resume Tailoring Agent

An intelligent web application built with **Streamlit** and powered by **Groq** (`openai/gpt-oss-120b`) that analyzes a candidate's master resume against any target job description, calculates a quantitative match percentage, identifies strengths and skill gaps, and generates an ATS-optimized tailored resume.

---

## 🌟 Features

- **Dual-Pane Input**: Easy-to-use input areas for both the target job description and your comprehensive master resume.
- **Groq `openai/gpt-oss-120b` Inference**: High-speed, high-capacity analysis of semantic fit and keyword alignment, with dynamic model selection.
- **Quantitative Match Percentage**: Instant visual alignment scoring (0-100%) and fit classification.
- **Gap & Strength Analysis**: Actionable breakdown of key strengths and missing qualifications.
- **Customized Tailored Resume**: Generates an ATS-friendly, metrics-driven tailored resume in clean GitHub Flavored Markdown.
- **Export Options**: Download tailored resumes directly as `.md` or `.txt`.
- **Zero-Hardcoding Security**: Built to strictly load the Groq API key via Streamlit's secrets manager (`st.secrets["GROQ_API_KEY"]`), with optional session-only sidebar entry.

---

## 📁 Project Structure

```
dazzling-babbage/
├── .streamlit/
│   ├── config.toml             # Streamlit dark theme & server settings
│   └── secrets.toml.example    # Template for Groq API key
├── .gitignore                  # Ignores venv, bytecode, and secrets.toml
├── app.py                      # Main Streamlit application
├── requirements.txt            # Project dependencies (streamlit, groq)
└── README.md                   # Project documentation
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (tested on Python 3.12)
- Groq API Key (get one free at [console.groq.com](https://console.groq.com/keys))

### 2. Setup Virtual Environment & Install Dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Configure Groq API Key (Streamlit Secrets)
Create a `.streamlit/secrets.toml` file in the project root:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
```

*Note: `.streamlit/secrets.toml` is included in `.gitignore` to prevent credentials from ever being committed.*

### 4. Run the Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.
