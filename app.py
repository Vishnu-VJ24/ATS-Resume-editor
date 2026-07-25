# ──────────────────────────────────────────────
# ATS Resume Optimizer — Streamlit App
# ──────────────────────────────────────────────
# Fire-and-forget: paste JD → get tailored PDF → done.
# Each run is completely stateless. No JD confusion.
# ──────────────────────────────────────────────

import re
import streamlit as st
from resume_optimizer import optimize_resume
from latex_compiler import compile_latex
from config import OWNER_NAME


# ═══════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════

st.set_page_config(
    page_title="ATS Resume Optimizer",
    page_icon="📄",
    layout="centered",
)


# ═══════════════════════════════════════════════
# AUTHENTICATION — Password Gate
# ═══════════════════════════════════════════════

def check_auth():
    """Simple password gate. Only Vishnu can use this app."""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown(
            """
            <div style="text-align: center; padding: 60px 20px;">
                <h1>🔒 ATS Resume Optimizer</h1>
                <p style="color: #888;">Personal use only</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pwd = st.text_input("Enter password:", type="password", key="login_pwd")
            if st.button("Login", use_container_width=True):
                if pwd == st.secrets["APP_PASSWORD"]:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("❌ Wrong password.")
        st.stop()


check_auth()


# ═══════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════

def sanitize_filename(text: str) -> str:
    """Convert text to a safe filename component: spaces→underscores, strip special chars."""
    text = text.strip()
    text = re.sub(r"[^\w\s-]", "", text)       # Remove special chars
    text = re.sub(r"[\s-]+", "_", text)         # Spaces/hyphens → underscore
    text = text.strip("_")
    return text


def build_filename(role_name: str, company_name: str) -> str:
    """Build the PDF filename: Vishnu_Kumar_RoleName_CompanyName.pdf"""
    role = sanitize_filename(role_name) if role_name else "Role"
    company = sanitize_filename(company_name) if company_name else "Company"
    return f"{OWNER_NAME}_{role}_{company}.pdf"


def compute_keyword_matches(jd_analysis: dict, modified_latex: str) -> dict:
    """Count how many JD keywords appear in the modified resume."""
    all_keywords = set()
    for key in ["required_skills", "preferred_skills", "tools_and_technologies", "domain_keywords", "ats_phrases"]:
        for item in jd_analysis.get(key, []):
            all_keywords.add(item.lower())

    matched = set()
    missed = set()
    latex_lower = modified_latex.lower()
    for kw in all_keywords:
        if kw.lower() in latex_lower:
            matched.add(kw)
        else:
            missed.add(kw)

    total = len(all_keywords)
    return {
        "matched": sorted(matched),
        "missed": sorted(missed),
        "score": round((len(matched) / total * 100) if total > 0 else 0),
        "total": total,
        "matched_count": len(matched),
    }


# ═══════════════════════════════════════════════
# MAIN APP UI
# ═══════════════════════════════════════════════

# Header
st.markdown(
    """
    <div style="text-align: center;">
        <h1>📄 ATS Resume Optimizer</h1>
        <p style="color: #888; margin-top: -10px;">
            Paste a job description → Get an ATS-optimized PDF → Download and apply
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

# ── JD Input ─────────────────────────────────
job_description = st.text_area(
    "📋 Paste the Job Description",
    height=300,
    placeholder="Paste the full job description here...\n\nInclude the role title, company name, responsibilities, requirements, and preferred qualifications.",
)

# ── Generate Button ──────────────────────────
generate = st.button(
    "🚀 Optimize Resume & Generate PDF",
    type="primary",
    use_container_width=True,
    disabled=len(job_description.strip()) < 50,
)

if len(job_description.strip()) > 0 and len(job_description.strip()) < 50:
    st.caption("⚠️ Job description seems too short. Paste the full JD for best results.")

# ── Processing Pipeline ─────────────────────
if generate and job_description.strip():
    try:
        # Step 1: Analyze JD
        with st.status("🔍 Analyzing job description...", expanded=True) as status:
            st.write("Extracting keywords, skills, and ATS phrases...")
            modified_latex, jd_analysis = optimize_resume(job_description)

            role_name = jd_analysis.get("role_name", "Unknown Role")
            company_name = jd_analysis.get("company_name", "Unknown Company")

            status.update(label=f"✅ Analyzed: **{role_name}** at **{company_name}**", state="complete")

        # Step 2: Compile PDF
        with st.status("📝 Compiling PDF...", expanded=True) as status:
            st.write("Running pdflatex on the optimized resume...")
            pdf_bytes = compile_latex(modified_latex)
            filename = build_filename(role_name, company_name)
            status.update(label=f"✅ PDF compiled: `{filename}`", state="complete")

        # ── SUCCESS ──────────────────────────
        st.success(f"✅ Resume optimized for **{role_name}** at **{company_name}**!")

        # Download button
        st.download_button(
            label=f"📥 Download {filename}",
            data=pdf_bytes,
            file_name=filename,
            mime="application/pdf",
            type="primary",
            use_container_width=True,
        )

        # ── Keyword Match Summary ────────────
        st.divider()
        st.subheader("📊 ATS Keyword Match Report")

        kw_report = compute_keyword_matches(jd_analysis, modified_latex)

        col1, col2, col3 = st.columns(3)
        col1.metric("Match Score", f"{kw_report['score']}%")
        col2.metric("Keywords Matched", f"{kw_report['matched_count']}/{kw_report['total']}")
        col3.metric("Keywords Missed", f"{len(kw_report['missed'])}")

        if kw_report["matched"]:
            with st.expander(f"✅ Matched Keywords ({len(kw_report['matched'])})"):
                st.write(", ".join(f"`{kw}`" for kw in kw_report["matched"]))

        if kw_report["missed"]:
            with st.expander(f"⚠️ Missed Keywords ({len(kw_report['missed'])})"):
                st.write(", ".join(f"`{kw}`" for kw in kw_report["missed"]))
                st.caption(
                    "These keywords from the JD couldn't be naturally incorporated. "
                    "Consider mentioning them in your cover letter."
                )

        # ── JD Analysis Details ──────────────
        with st.expander("🔍 Full JD Analysis"):
            st.json(jd_analysis)

        # ── Modified LaTeX Source ─────────────
        with st.expander("📝 Modified LaTeX Source"):
            st.code(modified_latex, language="latex")

    except ValueError as e:
        st.error(f"⚠️ Validation Error:\n\n{e}")
        st.info("The AI may have altered protected content. Try again — each run is independent.")

    except RuntimeError as e:
        st.error(f"⚠️ PDF Compilation Error:\n\n{e}")
        st.info("There may be a LaTeX syntax issue. Check the modified LaTeX source below.")
        if "modified_latex" in dir():
            with st.expander("📝 Modified LaTeX (for debugging)"):
                st.code(modified_latex, language="latex")

    except Exception as e:
        st.error(f"❌ Unexpected Error: {type(e).__name__}: {e}")
        st.info("Try again with a different JD, or check your Gemini API key in Streamlit secrets.")


# ── Footer ───────────────────────────────────
st.divider()
st.caption(
    "🔒 Personal use only · Each JD is processed independently · No data is stored · "
    "Powered by Google Gemini · Built with Streamlit"
)
