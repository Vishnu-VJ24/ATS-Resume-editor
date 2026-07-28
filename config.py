# ──────────────────────────────────────────────
# ATS Resume Optimizer — Configuration
# ──────────────────────────────────────────────

# Model fallback chain — tried in order when rate-limited (429) or unavailable (404)
# Primary: Gemma 4 31B — open-weights, instruction-tuned
# Fallbacks: Gemini 3.x flash series
GEMINI_MODELS = [
    "gemma-4-31b-it",          # Primary — Gemma 4 31B instruction-tuned
    "gemini-3.5-flash",        # Fallback 1 — Gemini 3.5 Flash
    "gemini-3.5-flash-lite",   # Fallback 2 — lighter, higher RPD
]

TEMPERATURE = 0.3          # Precise edits, not creative writing
MAX_OUTPUT_TOKENS = 8192   # Resume is ~180 lines — plenty of headroom
OWNER_NAME = "Vishnu_Kumar"
