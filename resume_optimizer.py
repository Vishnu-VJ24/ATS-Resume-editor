# ──────────────────────────────────────────────
# ATS Resume Optimizer — Gemini AI Core
# ──────────────────────────────────────────────
# Two-call pipeline:
#   Call 1: Analyze JD → structured JSON (keywords, role, company)
#   Call 2: Rewrite resume LaTeX using the analysis
# ──────────────────────────────────────────────

import json
import re
import google.generativeai as genai
import streamlit as st
from config import GEMINI_MODEL, TEMPERATURE, MAX_OUTPUT_TOKENS
from base_resume import BASE_RESUME_LATEX


def _get_model():
    """Initialize the Gemini model with the API key from Streamlit secrets."""
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    return genai.GenerativeModel(GEMINI_MODEL)


# ═══════════════════════════════════════════════
# CALL 1 — JD ANALYSIS
# ═══════════════════════════════════════════════

JD_ANALYSIS_PROMPT = """You are an expert ATS (Applicant Tracking System) analyst and recruiter.

Analyze the following job description and extract structured information for resume optimization.

Return your response as a VALID JSON object with exactly these keys:
{
  "role_name": "The exact job title (e.g., 'Machine Learning Engineer')",
  "company_name": "The company name (e.g., 'Google')",
  "required_skills": ["list of explicitly required technical skills"],
  "preferred_skills": ["list of nice-to-have / preferred skills"],
  "tools_and_technologies": ["specific tools, frameworks, platforms, services mentioned"],
  "domain_keywords": ["industry-specific or domain-specific terms"],
  "action_verbs": ["strong action verbs used in the JD"],
  "ats_phrases": ["exact multi-word phrases an ATS would likely scan for"],
  "experience_level": "junior / mid / senior / lead",
  "key_responsibilities": ["top 5 responsibilities summarized in 5-8 words each"]
}

RULES:
- Extract ONLY what is explicitly stated or strongly implied in the JD.
- For role_name, use the exact title from the JD. If multiple titles are listed, use the primary one.
- For company_name, use the company name as written. If not found, return "Unknown".
- Be thorough — ATS systems match on exact phrases, so capture them precisely.
- Return ONLY the JSON. No markdown fences, no explanation, no preamble.

JOB DESCRIPTION:
"""


def analyze_job_description(job_description: str) -> dict:
    """
    Call 1: Extract structured ATS keywords from the job description.
    Returns a dict with role_name, company_name, skills, keywords, etc.
    """
    model = _get_model()

    response = model.generate_content(
        JD_ANALYSIS_PROMPT + job_description,
        generation_config=genai.types.GenerationConfig(
            temperature=0.2,  # Even more precise for extraction
            max_output_tokens=4096,
        ),
    )

    raw = response.text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```(?:json)?\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
        analysis = json.loads(raw)
    except json.JSONDecodeError:
        # Retry: try to find JSON object in the response
        match = re.search(r"\{.*\}", raw, re.DOTALL)
        if match:
            analysis = json.loads(match.group())
        else:
            raise ValueError(
                f"Gemini did not return valid JSON for JD analysis.\n"
                f"Raw response:\n{raw[:500]}"
            )

    # Validate required fields
    required_keys = ["role_name", "company_name"]
    for key in required_keys:
        if key not in analysis:
            analysis[key] = "Unknown"

    return analysis


# ═══════════════════════════════════════════════
# CALL 2 — RESUME REWRITE
# ═══════════════════════════════════════════════

RESUME_REWRITE_SYSTEM_PROMPT = r"""You are an elite ATS resume optimization specialist. Your task is to surgically edit a LaTeX resume to maximize its ATS match score against a specific job description, while keeping the resume truthful and natural-sounding.

## YOUR INPUT
1. A structured analysis of the target job description (JSON with keywords, skills, phrases)
2. The complete LaTeX source code of the candidate's current resume

## YOUR OUTPUT
Return the COMPLETE modified LaTeX source code. Nothing else — no explanations, no markdown fences, no preamble, no commentary. Just the raw LaTeX starting with \documentclass and ending with \end{document}.

## IMMUTABLE — NEVER CHANGE THESE:
- Contact information (name, phone, email, LinkedIn, GitHub, portfolio URL)
- Education section (university names, degree names, GPAs, dates)
- Company names and role titles in Professional Experience
- Project names in Academic Projects
- Dates (start date, end date, "Present") for ANY entry
- Location information
- Certification names and issuers
- Numeric metrics and percentages (82% recall, 92% precision, 40%, 2.3%, 14%, etc.)
- The number of bullet points per role — do NOT add or remove bullets
- LaTeX document structure, commands, preamble, and formatting macros
- The \resumeSubheading and \resumeProjectHeading arguments (all 4 or 2 args respectively)

## MUTABLE — YOU CAN EDIT THESE:
- Text INSIDE \resumeItem{...} — the bullet point descriptions (this is your primary target)
- The Technical Skills section — you may reorder items within each category, or add a skill/tool ONLY if it appears in the JD AND is plausible given the candidate's background (MS in Data Science, AI/ML experience)
- The ordering of bullet points within a single role (swap order if it highlights relevance)

## KEYWORD INSERTION TECHNIQUES (use these):
1. **Verb alignment**: Replace action verbs with ones from the JD when they are synonymous
   - "Developed" → "Designed and developed" (if JD says "design")
   - "Built" → "Architected" (if JD says "architect")

2. **Technology insertion**: Add specific tools/frameworks from the JD that fit the context
   - "...on AWS" → "...on AWS (EC2, SageMaker)" if JD mentions these services

3. **Methodology mention**: Weave in methodologies from the JD
   - "Built a pipeline" → "Built an end-to-end ML pipeline following MLOps best practices"

4. **Scope enrichment**: Expand descriptions with JD-relevant scope terms
   - "...for monitoring" → "...for real-time monitoring and observability"

5. **Domain alignment**: Incorporate domain-specific language from the JD
   - "predictive model" → "predictive analytics model" (if JD uses "analytics")

## ANTI-PATTERNS — NEVER DO THESE:
1. Do NOT fabricate metrics, numbers, or results that aren't in the original
2. Do NOT add technologies that are implausible for the described project context
3. Do NOT make any single bullet point longer than ~250 characters (ATS readability)
4. Do NOT add or remove bullet points — keep the exact same count per role
5. Do NOT remove existing impressive metrics to make room for keywords
6. Do NOT keyword-stuff — every insertion must read naturally in context
7. Do NOT change LaTeX commands or formatting — preserve all \textbf{}, \\, \resumeItem{}, etc.
8. Do NOT wrap your output in ```latex``` or any markdown — return raw LaTeX only
9. Do NOT add a blank line before \end{document} or change spacing

## QUALITY CHECKLIST (verify before outputting):
✓ Every \resumeSubheading has identical arguments to the original
✓ Every date is identical to the original
✓ Every metric/percentage is identical to the original
✓ The document compiles (no broken LaTeX commands)
✓ Keywords from the JD appear naturally in at least 60% of bullet points
✓ The Technical Skills section includes JD-relevant skills
✓ The resume still reads as a coherent, professional document
"""


def rewrite_resume(jd_analysis: dict, job_description: str) -> str:
    """
    Call 2: Rewrite the base resume LaTeX to incorporate ATS keywords.
    Returns the complete modified LaTeX source code.
    """
    model = _get_model()

    user_prompt = f"""## JD ANALYSIS (extracted keywords and structure):
{json.dumps(jd_analysis, indent=2)}

## ORIGINAL JOB DESCRIPTION (for full context):
{job_description}

## CURRENT RESUME (LaTeX source — modify this):
{BASE_RESUME_LATEX}

Now rewrite the resume following the rules above. Return ONLY the complete LaTeX source code."""

    response = model.generate_content(
        [
            {"role": "user", "parts": [RESUME_REWRITE_SYSTEM_PROMPT]},
            {"role": "model", "parts": ["Understood. I will surgically edit the resume LaTeX to maximize ATS match score while preserving all dates, names, metrics, and formatting. I will return only raw LaTeX code."]},
            {"role": "user", "parts": [user_prompt]},
        ],
        generation_config=genai.types.GenerationConfig(
            temperature=TEMPERATURE,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        ),
    )

    modified_latex = response.text.strip()

    # ── Post-processing ──────────────────────────
    # Strip markdown code fences if Gemini wraps the output
    modified_latex = re.sub(r"^```(?:latex|tex)?\s*\n?", "", modified_latex)
    modified_latex = re.sub(r"\n?\s*```\s*$", "", modified_latex)

    # Validate critical structure
    _validate_latex(modified_latex)

    return modified_latex


def _validate_latex(latex: str):
    """
    Safety checks to ensure Gemini didn't break the resume structure.
    Raises ValueError with a clear message on failure.
    """
    errors = []

    if r"\begin{document}" not in latex:
        errors.append("Missing \\begin{document}")
    if r"\end{document}" not in latex:
        errors.append("Missing \\end{document}")
    if r"\documentclass" not in latex:
        errors.append("Missing \\documentclass")

    # Verify all original roles are still present (by company name)
    expected_companies = ["Methix", "Purcell Global Limited", "Arizona State University"]
    for company in expected_companies:
        if company not in latex:
            errors.append(f"Missing company/institution: {company}")

    # Verify all original projects are still present
    expected_projects = [
        "Wildfire Prediction",
        "Kafka and Neo4j",
        "Automated Abstract Notes",
    ]
    for project in expected_projects:
        if project not in latex:
            errors.append(f"Missing project: {project}")

    # Verify key dates are unchanged
    expected_dates = [
        "Aug 2024 -- May 2026",
        "Aug 2020 -- May 2024",
        "Jun 2025 -- Present",
        "Aug 2025 -- Present",
        "Jun 2025 -- Aug 2025",
    ]
    for date in expected_dates:
        if date not in latex:
            errors.append(f"Date altered or missing: {date}")

    # Verify metrics are unchanged
    expected_metrics = ["92\\%", "82\\%", "0.67 AUC", "40\\%", "2.3\\%", "14\\%", "80+", "470K", "1.5K"]
    for metric in expected_metrics:
        if metric not in latex:
            # Try without backslash for percentage signs
            alt_metric = metric.replace("\\%", "%")
            if alt_metric not in latex:
                errors.append(f"Metric altered or missing: {metric}")

    if errors:
        raise ValueError(
            "Resume validation failed — AI may have altered protected content:\n"
            + "\n".join(f"  • {e}" for e in errors)
        )


# ═══════════════════════════════════════════════
# PUBLIC API — Single entry point
# ═══════════════════════════════════════════════

def optimize_resume(job_description: str) -> tuple[str, dict]:
    """
    Main entry point. Takes a job description, returns (modified_latex, jd_analysis).

    Args:
        job_description: The full text of the job posting.

    Returns:
        Tuple of (modified_latex_source, jd_analysis_dict).
        jd_analysis_dict contains role_name, company_name, keywords, etc.
    """
    # Step 1: Analyze the JD
    jd_analysis = analyze_job_description(job_description)

    # Step 2: Rewrite the resume
    modified_latex = rewrite_resume(jd_analysis, job_description)

    return modified_latex, jd_analysis
