# ──────────────────────────────────────────────
# ATS Resume Optimizer — Configuration
# ──────────────────────────────────────────────

# Model fallback chain — tried in order when rate-limited (429)
# Primary: best quality, lowest free-tier RPD (~20/day)
# Fallbacks: slightly lower quality, higher RPD limits
GEMINI_MODELS = [
    "gemini-3.5-flash",        # Primary — best quality
    "gemini-2.5-flash",        # Fallback 1 — still strong
    "gemini-2.5-flash-lite",   # Fallback 2 — lighter but high RPD
]

TEMPERATURE = 0.3          # Precise edits, not creative writing
MAX_OUTPUT_TOKENS = 8192   # Resume is ~180 lines — plenty of headroom
OWNER_NAME = "Vishnu_Kumar"
