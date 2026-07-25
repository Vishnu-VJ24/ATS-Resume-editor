# ──────────────────────────────────────────────
# ATS Resume Optimizer — Base Resume (LaTeX)
# ──────────────────────────────────────────────
# This is Vishnu's master resume. The AI edits bullet-point
# descriptions but NEVER touches dates, role names, or metrics.

BASE_RESUME_LATEX = r"""%-------------------------
% Resume - Vishnu Jayanth Senthil Kumar
% Ultra-Compact One Page (No Overlap)
%------------------------

\documentclass[letterpaper,10pt]{article}

\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{marvosym}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
\usepackage{tabularx}
\usepackage{fontawesome5}
\input{glyphtounicode}

\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}

% Tight but safe margins
\addtolength{\oddsidemargin}{-0.65in}
\addtolength{\textwidth}{1.3in}
\addtolength{\topmargin}{-0.75in}
\addtolength{\textheight}{1.6in}

\urlstyle{same}
\raggedright
\setlength{\tabcolsep}{0in}
\linespread{0.97}

% Compact section formatting
\titleformat{\section}
  {\scshape\raggedright\large\bfseries}
  {}{0em}{}
  [\titlerule]

\titlespacing*{\section}{0pt}{5pt}{3pt}

% Tight lists
\setlist[itemize]{itemsep=1pt, topsep=2pt}

\renewcommand\labelitemi{$\bullet$}

% Commands
\newcommand{\resumeItem}[1]{\item\small{#1}}

\newcommand{\resumeSubheading}[4]{
  \item
  \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
    \textbf{#1} & \textbf{\small #2} \\
    \textit{\small #3} & \textit{\small #4} \\
  \end{tabular*}
}

\newcommand{\resumeProjectHeading}[2]{
  \item
  \begin{tabular*}{\textwidth}{l@{\extracolsep{\fill}}r}
    #1 & \textbf{\small #2} \\
  \end{tabular*}
}

\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=*]}
\newcommand{\resumeItemListEnd}{\end{itemize}}

\pdfgentounicode=1

%-------------------------------------------
\begin{document}

%----------HEADER----------
\begin{center}
{\LARGE \textbf{Vishnu Jayanth Senthil Kumar}} \\[2 pt]
\small Arizona, USA $\mid$ \faPhone~(602) 807-9922 $\mid$
\href{mailto:vishnujayanth.24@gmail.com}{\faEnvelope~vishnujayanth.24@gmail.com} $\mid$
\href{https://linkedin.com/in/vishnu--vj}{\faLinkedin~linkedin.com/in/vishnu{-}{-}vj} $\mid$
\href{https://github.com/vishnu-vj24}{\faGithub~github.com/vishnu-vj24} $\mid$
\href{https://vishnu-vj24.github.io/Vishnu-Portfolio/}{\faGlobe~vishnu-vj24.github.io/Vishnu-Portfolio}
\end{center}

%-----------EDUCATION-----------
\section{Education}
\resumeSubHeadingListStart
\resumeSubheading
{Arizona State University}{Aug 2024 -- May 2026}
{Master of Science in Data Science, Analytics and Engineering (GPA: 4.0/4.0)}{Arizona, USA}
\resumeSubheading
{Kumaraguru College of Technology}{Aug 2020 -- May 2024}
{Bachelor of Engineering in Computer Science (GPA: 3.56/4.0)}{Tamil Nadu, India}
\resumeSubHeadingListEnd

%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
\small
\textbf{Programming:} Python, SQL \\
\textbf{AI/ML:} PyTorch, TensorFlow, Scikit-learn, LangChain, LangGraph, Hugging Face, Pandas, NumPy \\
\textbf{Data:} SQL, NoSQL, Neo4j, Apache Kafka, Snowflake, BigQuery, Tableau, Power BI \\
\textbf{Cloud/MLOps:} Azure, AWS, GCP, Docker, Kubernetes, Airflow, CI/CD \\
\textbf{Specializations:} Generative AI, RAG, Agentic Systems, LLM Fine-Tuning, NLP, Computer Vision

%-----------PROFESSIONAL EXPERIENCE-----------
\section{Professional Experience}
\resumeSubHeadingListStart

\resumeSubheading
{AI Developer Intern -- Methix}{Jun 2025 -- Present}
{New York, USA (Remote)}{}
\resumeItemListStart
\resumeItem{Orchestrated a \textbf{sovereign multi-agent system} on \textbf{Azure} using \textbf{LangGraph}, optimizing asynchronous state handoffs to enable \textbf{sub-second latency}.}
\resumeItem{Architected a \textbf{hybrid RAG engine} with ``smart fallback'' logic (\textbf{Vector Search} to \textbf{Web Search}), ensuring answer completeness even when internal knowledge bases are insufficient.}
\resumeItem{Executed \textbf{Parameter-Efficient Fine-Tuning (LoRA)} on \textbf{Azure AI Foundry} to specialize models for proprietary datasets, prioritizing domain adherence over generic generalization.}
\resumeItem{Implemented a \textbf{Critic agent} with reflexion patterns to autonomously validate and correct generated outputs, systematically reducing \textbf{hallucination rates} in production.}
\resumeItemListEnd

\resumeSubheading
{Teaching Assistant - CSE 572: Data Mining}{Aug 2025 -- Present}
{Arizona State University, Tempe, AZ}{}
\resumeItemListStart
\resumeItem{Audited \textbf{80+ graduate-level projects} focusing on \textbf{clustering} and \textbf{deep learning pipelines}, while delivering technical lectures on \textbf{feature engineering} and validation strategies.}
\resumeItemListEnd

\resumeSubheading
{Machine Learning Engineer Intern -- Purcell Global Limited}{Jun 2025 -- Aug 2025}
{London, UK (Remote)}{}
\resumeItemListStart
\resumeItem{Engineered a \textbf{multimodal sensor fusion pipeline} combining pressure, acoustic, and imaging data for continuous patient monitoring on \textbf{AWS}.}
\resumeItem{Developed an \textbf{LSTM-based predictive model} to forecast \textbf{COPD exacerbations 48 hours ahead} with \textbf{92\% precision}, supporting proactive care.}
\resumeItem{Automated \textbf{data ingestion and preprocessing} with \textbf{AWS Lambda and S3}, reducing pipeline latency.}
\resumeItemListEnd

\resumeSubHeadingListEnd

%-----------ACADEMIC PROJECTS-----------
\section{Academic Projects}
\resumeSubHeadingListStart

\resumeProjectHeading
{\textbf{AI-Driven Wildfire Prediction System}}{Jan 2025 -- Apr 2025}
\resumeItemListStart
\resumeItem{Developed a spatiotemporal deep learning model (LSTM and Dense) on 470K satellite and meteorological records, achieving 82\% recall and 0.67 AUC for wildfire risk prediction.}
\resumeItem{Integrated spatial attention layers to localize high-risk zones, reducing false positives by 18\%.}
\resumeItemListEnd

\resumeProjectHeading
{\textbf{Real-Time Graph Analytics with Kafka and Neo4j}}{Jan 2025 -- Apr 2025}
\resumeItemListStart
\resumeItem{Implemented a Kafka-to-Neo4j streaming pipeline orchestrated with Kubernetes for NYC taxi data, enabling live graph updates on 1.5K relationships.}
\resumeItem{Applied PageRank and BFS algorithms to identify transit hubs, improving route efficiency analysis by 40\%.}
\resumeItemListEnd

\resumeProjectHeading
{\textbf{Automated Abstract Notes Generator}}{Feb 2024 -- May 2024}
\resumeItemListStart
\resumeItem{Fine-tuned BART and Whisper models for multimodal summarization, improving transcription accuracy by 2.3\% and summary coherence by 14\%.}
\resumeItem{Integrated a lightweight RAG layer for dynamic transcript referencing, enabling context-aware automated note creation.}
\resumeItemListEnd

\resumeSubHeadingListEnd

%-----------VOLUNTEERING & CERTIFICATIONS-----------
\section{Volunteering \& Certifications}
\resumeSubHeadingListStart
\resumeSubheading
{Green Fault Lines: Climate Change \& Political Economy}{Jan 2025 -- Apr 2025}
{Research Project, Arizona State University}{}
\resumeItemListStart
\resumeItem{Applied fixed-effects GLMs and causal inference models on ND-GAIN and QoG datasets across 32 nations to evaluate how governance quality influences climate resilience.}
\resumeItemListEnd
\resumeSubHeadingListEnd

\small
\textbf{Certifications:} Microsoft (Azure AI \& Data Fundamentals), IBM (AI Engineering), Atlassian (Agile with Jira), ASU Ira Fulton (Project Management \& Interpersonal Skills)

\end{document}"""
