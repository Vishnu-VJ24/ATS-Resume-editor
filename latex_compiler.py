# ──────────────────────────────────────────────
# ATS Resume Optimizer — LaTeX Compiler
# ──────────────────────────────────────────────
# Wraps pdflatex in a subprocess with tempdir isolation.
# Returns PDF bytes on success, raises on failure.
# ──────────────────────────────────────────────

import os
import subprocess
import tempfile


def compile_latex(latex_source: str) -> bytes:
    """
    Compile LaTeX source code into a PDF.

    Args:
        latex_source: Complete LaTeX source code as a string.

    Returns:
        The compiled PDF as bytes.

    Raises:
        RuntimeError: If pdflatex fails to compile.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "resume.tex")
        pdf_path = os.path.join(tmpdir, "resume.pdf")
        log_path = os.path.join(tmpdir, "resume.log")

        # Write the LaTeX source
        with open(tex_path, "w", encoding="utf-8") as f:
            f.write(latex_source)

        # Run pdflatex TWICE (for references, TOC, etc.)
        for pass_num in (1, 2):
            result = subprocess.run(
                [
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "-halt-on-error",
                    f"-output-directory={tmpdir}",
                    tex_path,
                ],
                capture_output=True,
                text=True,
                timeout=60,  # 60 second timeout per pass
                cwd=tmpdir,
            )

            # Only check the final pass for errors
            if pass_num == 2 and result.returncode != 0:
                # Read the log for diagnostics
                log_content = ""
                if os.path.exists(log_path):
                    with open(log_path, "r", encoding="utf-8", errors="replace") as f:
                        log_content = f.read()

                # Extract the most useful error lines
                error_lines = [
                    line for line in log_content.split("\n")
                    if line.startswith("!") or "Error" in line or "Undefined" in line
                ]
                error_summary = "\n".join(error_lines[:10]) if error_lines else result.stderr[:500]

                raise RuntimeError(
                    f"pdflatex compilation failed (pass {pass_num}):\n{error_summary}"
                )

        # Read the compiled PDF
        if not os.path.exists(pdf_path):
            raise RuntimeError(
                "pdflatex ran without errors but no PDF was produced. "
                "Check if all LaTeX packages are installed."
            )

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        if len(pdf_bytes) < 100:
            raise RuntimeError("Generated PDF is suspiciously small — compilation may have failed silently.")

        return pdf_bytes
