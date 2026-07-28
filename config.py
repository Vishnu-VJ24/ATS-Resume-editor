# ──────────────────────────────────────────────
# ATS Resume Optimizer — Configuration
# ──────────────────────────────────────────────

# Model fallback chain — tried in order when rate-limited (429) or unavailable (404)
GEMINI_MODELS = [
    "gemini-3.6-flash",        # Primary — Gemini 3.6 Flash (latest)
    "gemini-3.5-flash",        # Fallback 1 — Gemini 3.5 Flash
    "gemini-3.5-flash-lite",   # Fallback 2 — Gemini 3.5 Flash Lite
]

TEMPERATURE = 0.3          # Precise edits, not creative writing
MAX_OUTPUT_TOKENS = 8192   # Resume is ~180 lines — plenty of headroom
OWNER_NAME = "Vishnu_Kumar"
