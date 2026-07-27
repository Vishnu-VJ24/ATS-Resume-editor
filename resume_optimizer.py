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
from google.api_core.exceptions import ResourceExhausted, TooManyRequests
import streamlit as st
from config import GEMINI_MODELS, TEMPERATURE, MAX_OUTPUT_TOKENS
from base_resume import BASE_RESUME_LATEX


def _configure_api():
    """Configure the Gemini API key from Streamlit secrets."""
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])


def _call_with_fallback(generate_fn):
    """
    Try generate_fn(model) with each model in GEMINI_MODELS until one succeeds.
    Falls back to the next model on 429 (rate limit) errors.
    Returns (response, model_name) on success.
    Raises the last error if ALL models are exhausted.
    """
    _configure_api()
    last_error = None

    for model_name in GEMINI_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            response = generate_fn(model)
            # Store which model was used (for UI feedback)
            st.session_state["last_model_used"] = model_name
            return response, model_name
        except (ResourceExhausted, TooManyRequests) as e:
            last_error = e
            st.toast(f"⚠️ {model_name} rate-limited — trying next model...", icon="🔄")
            continue

    # All models exhausted
    raise ResourceExhausted(
        f"All models rate-limited. Tried: {', '.join(GEMINI_MODELS)}.\n"
        f"Last error: {last_error}\n"
        f"Try again tomorrow or upgrade to a paid API tier."
    )


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
    def _generate(model):
        return model.generate_content(
            JD_ANALYSIS_PROMPT + job_description,
            generation_config=genai.types.GenerationConfig(
                temperature=0.2,  # Even more precise for extraction
                max_output_tokens=4096,
            ),
        )

    response, _model_name = _call_with_fallback(_generate)

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

## BOLDING RULES — CRITICAL (follow exactly):
Every bullet point MUST start with a \textbf{...} block containing ONLY a technical skill, tool, framework, technology, methodology, or platform name. NEVER bold action verbs, adjectives, adverbs, or generic words.

### CORRECT bolding (technical skills/tools only):
- \resumeItem{\textbf{LangGraph} on Azure utilized to design...}
- \resumeItem{\textbf{RAG} pipeline with FAISS hybrid retrieval...}
- \resumeItem{\textbf{PyTorch} used to train a transformer model...}
- \resumeItem{\textbf{FastAPI \& Docker} used to build and containerize...}
- \resumeItem{Bidirectional \textbf{LSTM} for COPD exacerbation prediction...}
- \resumeItem{\textbf{AWS} data pipeline using S3 and Lambda...}
- \resumeItem{\textbf{LoRA} fine-tuning on 15GB domain data...}
- \resumeItem{\textbf{Kafka and Neo4j} on Kubernetes: built a streaming...}
- \resumeItem{\textbf{QLoRA} 4-bit fine-tuning applied to a 21B-parameter model...}

### WRONG bolding (NEVER do this):
- \resumeItem{\textbf{Built} a RAG pipeline...}           <- "Built" is a verb, not a tech
- \resumeItem{\textbf{Developed} an ML model...}          <- "Developed" is a verb
- \resumeItem{\textbf{Scalable} microservices...}         <- "Scalable" is an adjective
- \resumeItem{\textbf{Automated} ETL pipelines...}        <- "Automated" is a verb
- \resumeItem{\textbf{End-to-end} pipeline...}            <- generic phrase, not a technology
- \resumeItem{\textbf{Real-time} monitoring...}           <- adjective, not a tech name
- \resumeItem{\textbf{Cross-functional} collaboration...} <- adjective, not a tech name

### The pattern is:
\resumeItem{\textbf{TechName} rest of the bullet describing what was done with it.}
The bolded part is ALWAYS a proper noun — a named technology, tool, framework, library, platform, protocol, or methodology abbreviation (e.g., RAG, LoRA, LSTM, CI/CD). If a bullet cannot naturally lead with a tech name, place \textbf{} around the most relevant tech keyword wherever it appears in the sentence (see the LSTM example above).

## ACTION VERB RULES — CRITICAL (follow exactly):
1. NEVER use third-person present tense: "Builds", "Deploys", "Develops", "Creates", "Implements", "Designs" are FORBIDDEN.
2. For past roles (end date is a specific month/year): use past tense — "Built", "Deployed", "Developed", "Engineered", "Architected", "Trained", "Integrated", "Automated", "Optimized", "Reduced", "Led", "Implemented".
3. For current roles (end date is "Present"): use past tense for completed work. You may also use present participle phrasing where the tech name leads (e.g., "\textbf{PyTorch} modeling applied to..." or "\textbf{RAG} pipeline deployed via...").
4. VARIETY IS MANDATORY: Within any single role, no two bullet points may start with the same action verb or verb phrase. Across the ENTIRE resume, minimize repetition — use at least 8 distinct action verbs. Choose from a diverse pool:
   Built, Designed, Engineered, Architected, Developed, Deployed, Trained, Integrated, Automated, Optimized, Reduced, Led, Implemented, Orchestrated, Accelerated, Streamlined, Migrated, Established, Launched, Constructed, Delivered, Spearheaded, Pioneered, Consolidated, Refactored, Leveraged, Applied, Utilized, Configured, Instituted.
5. Study the base resume's style: bullets often lead with the tech name in bold, then weave in the action verb after — e.g., "\textbf{LoRA} fine-tuning on 15GB domain data..." or "\textbf{LangGraph} on Azure utilized to design...". This style is PREFERRED over verb-first bullets.

## KEYWORD INSERTION TECHNIQUES (use these):
1. **Technology-led bullets**: Lead with the JD-relevant technology in bold, then describe the action
   - "\textbf{Kubernetes} orchestration configured for auto-scaling inference pods..."
   - "\textbf{MLflow} experiment tracking integrated across the training pipeline..."

2. **Technology insertion**: Add specific tools/frameworks from the JD that fit the context
   - "...on AWS" -> "...on AWS (EC2, SageMaker)" if JD mentions these services

3. **Methodology mention**: Weave in methodologies from the JD
   - "Built a pipeline" -> "Built an end-to-end ML pipeline following MLOps best practices"

4. **Scope enrichment**: Expand descriptions with JD-relevant scope terms
   - "...for monitoring" -> "...for real-time monitoring and observability"

5. **Domain alignment**: Incorporate domain-specific language from the JD
   - "predictive model" -> "predictive analytics model" (if JD uses "analytics")

## ANTI-PATTERNS — NEVER DO THESE:
1. Do NOT fabricate metrics, numbers, or results that aren't in the original
2. Do NOT add technologies that are implausible for the described project context
3. Do NOT make any single bullet point longer than ~250 characters (ATS readability)
4. Do NOT add or remove bullet points — keep the exact same count per role
5. Do NOT remove existing impressive metrics to make room for keywords
6. Do NOT keyword-stuff — every insertion must read naturally in context
7. Do NOT change LaTeX commands or formatting — preserve all \resumeItem{}, etc.
8. Do NOT wrap your output in ```latex``` or any markdown — return raw LaTeX only
9. Do NOT add a blank line before \end{document} or change spacing
10. Do NOT bold action verbs, adjectives, or generic words — \textbf{} is ONLY for technology/tool/framework/platform names (e.g., \textbf{PyTorch}, \textbf{RAG}, \textbf{Kubernetes})
11. Do NOT use third-person present tense verbs anywhere (Builds, Deploys, Creates, Implements, Designs, Configures — ALL FORBIDDEN)
12. Do NOT start two bullet points within the same role with the same action verb or verb phrase — every bullet must open differently

## QUALITY CHECKLIST (verify EVERY bullet before outputting):
✓ Every \resumeSubheading has identical arguments to the original
✓ Every date is identical to the original
✓ Every metric/percentage is identical to the original
✓ The document compiles (no broken LaTeX commands)
✓ Keywords from the JD appear naturally in at least 60% of bullet points
✓ The Technical Skills section includes JD-relevant skills
✓ The resume still reads as a coherent, professional document
✓ EVERY \textbf{} in bullet points wraps ONLY a technology, tool, framework, or platform name — never a verb or adjective
✓ NO bullet uses a third-person present tense verb (Builds, Deploys, etc.)
✓ Within each role, every bullet begins with a DIFFERENT action verb or tech-led construction — scan and fix any duplicates
✓ Across the entire resume, at least 8 distinct leading verbs/constructions are used
"""


def rewrite_resume(jd_analysis: dict, job_description: str) -> str:
    """
    Call 2: Rewrite the base resume LaTeX to incorporate ATS keywords.
    Returns the complete modified LaTeX source code.
    """
    user_prompt = f"""## JD ANALYSIS (extracted keywords and structure):
{json.dumps(jd_analysis, indent=2)}

## ORIGINAL JOB DESCRIPTION (for full context):
{job_description}

## CURRENT RESUME (LaTeX source — modify this):
{BASE_RESUME_LATEX}

Now rewrite the resume following the rules above. Return ONLY the complete LaTeX source code."""

    def _generate(model):
        return model.generate_content(
            [
                {"role": "user", "parts": [RESUME_REWRITE_SYSTEM_PROMPT]},
                {"role": "model", "parts": ["Understood. I will surgically edit the resume LaTeX to maximize ATS match score while preserving all dates, names, metrics, and formatting. I will bold ONLY technical skills/tools/frameworks — never verbs or adjectives. I will use varied past-tense action verbs with no repeats within any role. I will return only raw LaTeX code."]},
                {"role": "user", "parts": [user_prompt]},
            ],
            generation_config=genai.types.GenerationConfig(
                temperature=TEMPERATURE,
                max_output_tokens=MAX_OUTPUT_TOKENS,
            ),
        )

    response, _model_name = _call_with_fallback(_generate)
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
    Surgically checks that Gemini preserved structural details and metrics.
    Uses dynamic extraction from BASE_RESUME_LATEX so that updating
    the resume on GitHub doesn't break validation.
    """
    errors = []

    # 1. Basic LaTeX block checks
    if r"\begin{document}" not in latex:
        errors.append("Missing \\begin{document}")
    if r"\end{document}" not in latex:
        errors.append("Missing \\end{document}")
    if r"\documentclass" not in latex:
        errors.append("Missing \\documentclass")

    # 2. Dynamic structure verification
    # Extract all \resumeExpHeading definitions
    exp_headings = re.findall(
        r'\\resumeExpHeading\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}',
        BASE_RESUME_LATEX,
        re.DOTALL
    )
    for company, date, role, location in exp_headings:
        company, date, role, location = company.strip(), date.strip(), role.strip(), location.strip()
        # Verify these exist in the output (ignoring extra spaces/newlines)
        if company not in latex:
            errors.append(f"Missing company: '{company}'")
        if date not in latex:
            errors.append(f"Missing or altered date: '{date}'")
        if role not in latex:
            errors.append(f"Missing or altered role: '{role}'")

    # Extract all \resumeProjectHeading definitions
    proj_headings = re.findall(
        r'\\resumeProjectHeading\s*\{([^{}]*)\}\s*\{([^{}]*)\}',
        BASE_RESUME_LATEX,
        re.DOTALL
    )
    for project, link in proj_headings:
        project, link = project.strip(), link.strip()
        if project not in latex:
            errors.append(f"Missing project: '{project}'")

    # Extract all \resumeSubheading definitions (e.g., Education)
    sub_headings = re.findall(
        r'\\resumeSubheading\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}\s*\{([^{}]*)\}',
        BASE_RESUME_LATEX,
        re.DOTALL
    )
    for school, date, degree, location in sub_headings:
        school, date, degree, location = school.strip(), date.strip(), degree.strip(), location.strip()
        if school not in latex:
            errors.append(f"Missing institution: '{school}'")
        if date not in latex:
            errors.append(f"Missing date in education: '{date}'")
        if degree not in latex:
            errors.append(f"Missing degree: '{degree}'")

    # 3. Dynamic metrics verification
    # Find all percentages, metric terms, and specific quantities in BASE_RESUME_LATEX
    metric_regexes = [
        r'\b\d+(?:\.\d+)?\s*(?:\\%|%)',                               # 24%, 35%, 92%
        r'\b\d+(?:\.\d+)?\s*(?:plus|GB|B|M|K|AUC|hours?)\b',          # 15GB, 1.5M, 80 plus
        r'\b\d+(?:\.\d+)?-parameter\b',                               # 21B-parameter
        r'\b\d+\.\d+\s*AUC\b',                                        # 0.88 AUC
        r'\b\d+(?:\.\d+)?\s*plus\b'                                   # 5,000 plus
    ]

    extracted_metrics = set()
    for pattern in metric_regexes:
        matches = re.findall(pattern, BASE_RESUME_LATEX)
        for m in matches:
            # Normalize to compare without spacing and backslash issues
            norm = m.replace("\\", "").replace(" ", "").lower()
            extracted_metrics.add((m, norm))

    for original_metric, normalized_metric in extracted_metrics:
        # Check if normalized metric exists in the normalized output
        normalized_output = latex.replace("\\", "").replace(" ", "").lower()
        if normalized_metric not in normalized_output:
            errors.append(f"Metric altered or missing: '{original_metric}'")

    # 4. Bolding validation — ensure \textbf{} never wraps a plain action verb
    bold_contents = re.findall(r'\\textbf\{([^{}]+)\}', latex)
    # Common action verbs that should NEVER be bolded
    forbidden_bold = {
        "built", "developed", "designed", "deployed", "created", "implemented",
        "automated", "optimized", "integrated", "engineered", "architected",
        "led", "managed", "established", "launched", "delivered", "reduced",
        "improved", "configured", "orchestrated", "streamlined", "migrated",
        "builds", "develops", "designs", "deploys", "creates", "implements",
        "automates", "optimizes", "integrates", "engineers", "leads",
        "scalable", "end-to-end", "real-time", "cross-functional", "advanced",
        "comprehensive", "robust", "efficient", "innovative", "collaborative",
    }
    for bold_text in bold_contents:
        clean = bold_text.strip().lower()
        if clean in forbidden_bold:
            errors.append(f"Bolding violation: '\\textbf{{{bold_text}}}' — only technology/tool names should be bolded, not verbs or adjectives")

    # 5. Third-person present tense verb check
    # Extract text inside \resumeItem{...} and check first word after any \textbf{...}
    resume_items = re.findall(r'\\resumeItem\{(.+?)\}(?:\s*$|\s*\\)', latex, re.MULTILINE)
    third_person_verbs = {
        "builds", "develops", "designs", "deploys", "creates", "implements",
        "automates", "optimizes", "integrates", "engineers", "configures",
        "manages", "establishes", "launches", "delivers", "reduces",
        "improves", "orchestrates", "streamlines", "migrates", "trains",
        "utilizes", "leverages", "architects",
    }
    for item_text in resume_items:
        # Strip any leading \textbf{...} to find the action verb
        stripped = re.sub(r'^\\textbf\{[^{}]*\}\s*', '', item_text).strip()
        first_word = stripped.split()[0].lower().rstrip('.,;:') if stripped.split() else ''
        if first_word in third_person_verbs:
            errors.append(f"Third-person verb violation: bullet starts with '{first_word}' — use past tense instead")

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
