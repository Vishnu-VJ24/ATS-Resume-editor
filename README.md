# 📄 ATS Resume Optimizer

A personal-use, fire-and-forget resume optimization tool. Paste a job description → get a tailored, ATS-optimized PDF resume → download and apply.

## How It Works

1. **Paste** the full job description into the app
2. **Gemini AI** analyzes the JD — extracts keywords, skills, ATS phrases, role name, and company name
3. **AI rewrites** your resume bullet points to naturally incorporate those keywords (dates, metrics, and role names are NEVER changed)
4. **pdflatex** compiles the modified LaTeX into a professional PDF
5. **Download** as `Vishnu_Kumar_RoleName_CompanyName.pdf`

Each run is completely independent — no state is carried over between JDs.

## Tech Stack

- **Frontend**: Streamlit
- **AI**: Google Gemini 2.0 Flash
- **PDF**: pdflatex (LaTeX → PDF)
- **Deployment**: Streamlit Cloud
- **Auth**: Password gate via Streamlit secrets

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/vishnu-vj24/ats-resume-optimizer.git
cd ats-resume-optimizer
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Install LaTeX (for local dev)

**macOS**: `brew install --cask mactex-no-gui`
**Ubuntu/Debian**: `sudo apt install texlive-latex-base texlive-latex-extra texlive-fonts-recommended`
**Windows**: Install [MiKTeX](https://miktex.org/download)

### 4. Set up secrets

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:
- `GEMINI_API_KEY` — Get from [Google AI Studio](https://aistudio.google.com/apikey)
- `APP_PASSWORD` — Any password you choose

### 5. Run locally

```bash
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repo to GitHub (private repo recommended)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo → select `app.py`
4. Add secrets in **Settings → Secrets**:
   ```toml
   GEMINI_API_KEY = "your-key"
   APP_PASSWORD = "your-password"
   ```
5. Deploy!

## Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit UI — password gate, JD input, download |
| `resume_optimizer.py` | Gemini AI — JD analysis + resume rewriting |
| `latex_compiler.py` | pdflatex subprocess wrapper |
| `base_resume.py` | Hardcoded LaTeX resume (edit to update your base resume) |
| `config.py` | Constants (model, temperature, etc.) |
| `packages.txt` | apt packages for Streamlit Cloud |

## Updating Your Resume

Edit `base_resume.py` and update the `BASE_RESUME_LATEX` string with your new LaTeX source. Push to GitHub and Streamlit Cloud will auto-redeploy.

## License

Personal use only.
