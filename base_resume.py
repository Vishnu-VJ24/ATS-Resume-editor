BASE_RESUME_LATEX = r"""\documentclass[letterpaper,10pt]{article}
 
\usepackage[empty]{fullpage}
\usepackage{titlesec}
\usepackage{enumitem}
\usepackage[hidelinks]{hyperref}
\usepackage{fancyhdr}
\usepackage[english]{babel}
 
\pagestyle{fancy}
\fancyhf{}
\renewcommand{\headrulewidth}{0pt}
\renewcommand{\footrulewidth}{0pt}
\setlength{\footskip}{6pt}
 
\addtolength{\oddsidemargin}{-0.6in}
\addtolength{\textwidth}{1.2in}
\addtolength{\topmargin}{-0.65in}
\addtolength{\textheight}{1.5in}
 
\urlstyle{same}
\raggedright
\setlength{\tabcolsep}{0in}
\linespread{0.95}
 
\titleformat{\section}{\bfseries\normalsize}{}{0em}{\uppercase}
\titlespacing*{\section}{0pt}{7pt}{3pt}
 
\setlist[itemize]{itemsep=1pt, topsep=2pt}
 
\newcommand{\resumeItem}[1]{\item\small{#1}}
 
\newcommand{\resumeSubheading}[4]{
  \item
  \textbf{#3} \hfill \textbf{\small #2} \\
  \textit{\small #1} \hfill \textit{\small #4} \vspace{0pt}
}
 
\newcommand{\resumeExpHeading}[4]{
  \item
  \textbf{#3} $\vert$ \textit{\small #1}, \textit{\small #4} \hfill \textbf{\small #2}
  \vspace{0pt}
}
 
\newcommand{\resumeProjectHeading}[2]{%
  \item
  \textbf{#1} $\mid$ \href{#2}{Project Link} \vspace{0pt}
}
 
\newcommand{\resumeSubHeadingListStart}{\begin{itemize}[leftmargin=0in, label={}]}
\newcommand{\resumeSubHeadingListEnd}{\end{itemize}}
\newcommand{\resumeItemListStart}{\begin{itemize}[leftmargin=0.3in, label={-}]}
\newcommand{\resumeItemListEnd}{\end{itemize}}
 
\begin{document}
 
%----------HEADER----------
\begin{center}
  {\LARGE \textbf{Vishnu Jayanth Senthil Kumar}} \\[2pt]
  \small San Francisco Bay Area, CA $\mid$ (602) 807-9922 $\mid$
  \href{mailto:vishnujayanth.24@gmail.com}{vishnujayanth.24@gmail.com} $\mid$
  \href{https://linkedin.com/in/vishnu--vj}{linkedin.com/in/vishnu\texttt{--}vj} $\mid$
  \href{https://github.com/vishnu-vj24}{github.com/vishnu-vj24} $\mid$
  \href{https://vishnu-vj24.github.io/Vishnu-Portfolio}{https://vishnu-vj24.github.io/Vishnu-Portfolio/} \\[3pt]
\end{center}
\vspace{-12pt}
 
%-----------PROFESSIONAL EXPERIENCE-----------
\section{Professional Experience}
\resumeSubHeadingListStart
 
  \resumeExpHeading
    {QWERX, Inc.}{July 2026 -- Present}
    {Software Engineer, AI}{San Francisco, USA (Remote)}
  \resumeItemListStart
    \resumeItem{\textbf{AI/ML} modeling applied to endpoint audit-log data to characterize anomalous authentication handshakes, powering QWERX's "Extract the Attack" agent capability.}
    \resumeItem{\textbf{Predictive Threat Detection} models integrated into the core endpoint security agent, partnering with engineering to proactively strengthen the network security posture.}
  \resumeItemListEnd
 
  \resumeExpHeading
    {Integrated Travel}{June 2026 -- July 2026}
    {Data Scientist}{Texas, USA (Remote) }
  \resumeItemListStart
    \resumeItem{\textbf{RAG \& FAISS} hybrid search pipeline deployed via Python and Streamlit, utilizing automated GitHub CI/CD to enable instant system redeployment.}
    \resumeItem{\textbf{GeoPandas \& Scikit-learn} used to engineer spatial-economic models, evaluating infrastructure gaps to validate a \$1.15B regional tourism growth projection.}
  \resumeItemListEnd
 
  \resumeExpHeading
    {Methix}{June 2025 -- May 2026}
    {AI Engineer}{New York, USA (Remote)}
  \resumeItemListStart
    \resumeItem{\textbf{LangGraph} on Azure utilized to design and maintain a multi-agent AI platform, processing 5,000 plus user queries daily with zero downtime and no failed searches.}
    \resumeItem{\textbf{RAG} pipeline with FAISS hybrid retrieval: built the search layer so every query returned relevant results, eliminating zero-result failures entirely.}
    \resumeItem{\textbf{LoRA} fine-tuning on 15GB domain data with INT8 quantization via vLLM: improved model accuracy by 24\% over baseline while measurably reducing cloud inference cost.}
    \resumeItem{\textbf{LangChain} LLM-as-judge evaluation pipeline: automated factuality checks that caught and reduced hallucinations by 35\% across sampled production responses.}
    \resumeItem{\textbf{FastAPI} microservices deployed on Azure Container Apps via Docker: enabled auto-scaling endpoints with zero-downtime rolling deploys for new model versions.}
  \resumeItemListEnd
 
  \resumeExpHeading
    {Arizona State University}{August 2025 -- May 2026}
    {Graduate Teaching Assistant}{Tempe, AZ}
  \resumeItemListStart
    \resumeItem{Led weekly lab sessions for 80 plus graduate students for Data Mining Class on ML pipelines, feature engineering, model evaluation, and interpretability, making complex topics practical and hands-on.}
  \resumeItemListEnd
 
  \resumeExpHeading
    {Purcell Global Limited}{June 2025 -- August 2025}
    {Machine Learning Engineer Intern}{London, UK (Remote)}
  \resumeItemListStart
    \resumeItem{Bidirectional \textbf{LSTM} for COPD exacerbation prediction: trained a model that flagged high-risk patients 48 hours before a health event, achieving 92\% precision and 0.88 AUC on a held-out cohort.}
    \resumeItem{\textbf{AWS} data pipeline using S3 and Lambda: automated ETL for 120GB of wearable sensor data and cut pipeline latency by 35\% through parallel execution.}
  \resumeItemListEnd
 
\resumeSubHeadingListEnd
 
%-----------PROJECTS-----------
\section{Projects}
\resumeSubHeadingListStart
 
  \resumeProjectHeading{Legal Risk Sentinel}{https://bored26-legal-sentinel.hf.space/}
  \resumeItemListStart
    \resumeItem{\textbf{QLoRA} 4-bit fine-tuning applied to a 21B-parameter model hosted on a FastAPI and Next.js stack, fitting the full generative AI platform within 24GB VRAM constraints.}
    \resumeItem{\textbf{JSON-Schema} tool calling implemented to guide multi-task legal reasoning, ensuring reliable clause classification and citation retrieval with robust hallucination guardrails.}
  \resumeItemListEnd
 
  \resumeProjectHeading{Wildfire Risk Prediction System}{https://github.com/vishnu-vj24}
  \resumeItemListStart
    \resumeItem{\textbf{Spatial-Temporal LSTM} with attention mechanisms trained on 470K weather records, achieving 82\% recall for early wildfire detection and reducing false-positives by 18\%.}
    \resumeItem{\textbf{FastAPI \& Docker} used to build and containerize a real-time inference API via multi-stage workflows, ensuring scalable and efficient deployment.}
  \resumeItemListEnd
 
  \resumeProjectHeading{Real-Time Knowledge Graph Pipeline}{https://github.com/vishnu-vj24}
  \resumeItemListStart
    \resumeItem{\textbf{Kafka and Neo4j} on Kubernetes: built a streaming ingestion system maintaining 1.5M plus live entity relationships with sub-second write throughput.}
    \resumeItem{PageRank and community detection applied on live graph data, exposed via REST API, improved downstream routing insights by 40\%.}
  \resumeItemListEnd
 
\resumeSubHeadingListEnd
 
%-----------TECHNICAL SKILLS-----------
\section{Technical Skills}
{\small Python, TypeScript, React, Next.js, FastAPI, Docker, Kubernetes, PyTorch, Transformers, FAISS, RAG, LangGraph, LangChain, LangSmith, LLM-as-a-Judge, PEFT, LoRA, QLoRA, vLLM, Hugging Face, Scikit-learn, TensorFlow, LSTM, Spatial Attention, Temporal Attention, Graph-RAG, Apache Kafka, Neo4j, PySpark, SQL, PostgreSQL, MLflow, AWS (S3, Lambda, SageMaker), Azure (Container Apps, AI Foundry), GCP, Microsoft Azure AI Fundamentals (AI-900), Azure Data Fundamentals (DP-900), IBM AI Engineering}
\vspace{0pt}
 
%-----------EDUCATION-----------
\section{Education}
\resumeSubHeadingListStart
  \resumeSubheading
    {Arizona State University, GPA: 4.0/4.0, with Distinction}{August 2024 -- May 2026}
    {Master of Science in Data Science, Analytics and Engineering}{Arizona, USA}
\resumeSubHeadingListEnd
 
\end{document} """
