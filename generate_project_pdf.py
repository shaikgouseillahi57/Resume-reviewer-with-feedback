import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))
        
        # Header (Pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 750, "AI Resume Reviewer & Feedback Platform — Project Review Documentation")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 742, 558, 742)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(558, 35, page_text)
        self.drawString(54, 35, "CONFIDENTIAL — Academic & Technical Evaluation Document")
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 47, 558, 47)
        self.restoreState()

def build_pdf(filename="AI_Resume_Reviewer_Project_Documentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    primary = colors.HexColor("#1e293b")
    brand = colors.HexColor("#4338ca")
    brand_light = colors.HexColor("#eef2ff")
    accent = colors.HexColor("#0284c7")
    slate_dark = colors.HexColor("#334155")
    slate_light = colors.HexColor("#f8fafc")
    border_color = colors.HexColor("#cbd5e1")
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=22,
        leading=26,
        textColor=brand,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=slate_dark,
        spaceAfter=14
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=18,
        textColor=brand,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        textColor=accent,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=slate_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=slate_dark,
        leftIndent=14,
        spaceAfter=4
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#312e81")
    )
    
    table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=slate_dark
    )
    
    table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []

    # ==========================================
    # COVER / HEADER BLOCK
    # ==========================================
    story.append(Paragraph("AI Resume Reviewer & Feedback Platform", title_style))
    story.append(Paragraph("<b>Comprehensive Project Report & Review Guide</b> | Automated ATS Analysis & Optimization", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=brand, spaceBefore=0, spaceAfter=12))

    # Project Metadata Box
    meta_data = [
        [
            Paragraph("<b>Project Domain:</b> Artificial Intelligence / NLP / Full-Stack Web", table_cell),
            Paragraph("<b>Version:</b> 1.1.0 (Production Ready)", table_cell)
        ],
        [
            Paragraph("<b>Target Audience:</b> Job Seekers, Students, University Career Cells", table_cell),
            Paragraph("<b>Review Phase:</b> First Project Review & Architecture Evaluation", table_cell)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 234])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), brand_light),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#c7d2fe")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e0e7ff")),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # 1. EXECUTIVE SUMMARY & PROBLEM STATEMENT
    # ==========================================
    story.append(Paragraph("1. Executive Summary & Problem Statement", h1_style))
    story.append(Paragraph(
        "<b>The Problem:</b> Over 75% of job applicant resumes are automatically rejected by corporate Applicant Tracking Systems (ATS) "
        "before any human recruiter reads them. Common causes include unparsed document formatting, absent core skill keywords, lack of quantifiable "
        "impact metrics in bullet points, and mismatch against target job descriptions. Furthermore, job seekers receive generic rejection notices "
        "without actionable diagnostic feedback.",
        body_style
    ))
    story.append(Paragraph(
        "<b>The Solution:</b> The <i>AI Resume Reviewer & Career Feedback Platform</i> is a specialized intelligent web platform designed to function as an "
        "automated virtual career mentor. It extracts, audits, scores, and rewrites resumes against 15 industry-standard technology career tracks in real time, "
        "empowering candidates to identify critical skill gaps and optimize their resume prior to actual company submissions.",
        body_style
    ))
    story.append(Spacer(1, 8))

    # ==========================================
    # 2. KEY CAPABILITIES & CORE FEATURES
    # ==========================================
    story.append(Paragraph("2. Core Features & Capabilities", h1_style))
    
    features = [
        ("Explainable ATS Scoring Engine (0-100)", "Generates a composite score based on skill match (40%), target role alignment (30%), resume section completeness (15%), and keyword density (15%)."),
        ("Dual Role Analysis Modes", "Supports 'With Target Role' (evaluates against a chosen career path like Frontend Developer or Data Scientist) and 'Without Target Role' (auto-detects the candidate's optimal tech track using Machine Learning)."),
        ("Rule-Based NLP Skill Extraction", "Audits resumes against 200+ industry technical skills and classifies detected skills versus missing required skills for the role."),
        ("Target Job Description Matcher", "Computes TF-IDF Cosine Similarity between a candidate's resume and any raw job posting text, providing exact match percentages and keyword gap analysis."),
        ("Interactive Real-Time Text Editor", "Allows users to live-edit resume text with real-time recalculation of scores and instant feedback without requiring file re-uploads."),
        ("AI Bullet Point Rewriter", "Transforms passive duty descriptions ('worked on website') into high-impact, quantified XYZ achievement statements ('Engineered responsive UI using React, driving an 18% lift in conversion')."),
        ("ATS Layout & Format Verification", "Validates page count compliance (1-page standard), contact details existence (email, phone, LinkedIn/GitHub), and standard section headings."),
        ("Supabase Cloud Database Persistence", "Stores every review session, extracted text, feedback, and score into Supabase PostgreSQL, enabling historical retrieval and progress tracking.")
    ]

    for title, desc in features:
        story.append(Paragraph(f"• <b>{title}:</b> {desc}", bullet_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # 3. COMPLETE TECHNOLOGY STACK
    # ==========================================
    story.append(Paragraph("3. Complete Technology Stack & Specifications", h1_style))
    
    tech_data = [
        [Paragraph("Layer", table_header), Paragraph("Technology / Framework", table_header), Paragraph("Functional Role & Justification", table_header)],
        [
            Paragraph("<b>Frontend</b>", table_cell),
            Paragraph("React 18, Vite 5, Tailwind CSS 3", table_cell),
            Paragraph("High-performance client UI with Hot Module Replacement, modular component architecture, and responsive styling.", table_cell)
        ],
        [
            Paragraph("<b>Icons & UI</b>", table_cell),
            Paragraph("Lucide React, Axios", table_cell),
            Paragraph("Modern vector iconography and reliable asynchronous HTTP communication with FastAPI backend.", table_cell)
        ],
        [
            Paragraph("<b>Backend API</b>", table_cell),
            Paragraph("FastAPI (Python 3.10+), Uvicorn", table_cell),
            Paragraph("Asynchronous ASGI web framework offering sub-millisecond route execution and automated OpenAPI documentation.", table_cell)
        ],
        [
            Paragraph("<b>Validation & I/O</b>", table_cell),
            Paragraph("Pydantic v2, Python-Multipart, HTTPX", table_cell),
            Paragraph("Strict data schemas, high-speed multipart PDF file uploads, and asynchronous cloud requests.", table_cell)
        ],
        [
            Paragraph("<b>PDF Processing</b>", table_cell),
            Paragraph("PyMuPDF (fitz)", table_cell),
            Paragraph("High-speed C-native PDF text extraction, layout reading, and font/metadata analysis without Java dependencies.", table_cell)
        ],
        [
            Paragraph("<b>Machine Learning</b>", table_cell),
            Paragraph("Scikit-Learn (LinearSVC)", table_cell),
            Paragraph("Support Vector Classification trained on tech resumes for 15 career track domain predictions with low latency.", table_cell)
        ],
        [
            Paragraph("<b>NLP & Vectorization</b>", table_cell),
            Paragraph("TF-IDF Vectorizer, Regex", table_cell),
            Paragraph("Text tokenization, n-gram weighting, cosine similarity matching, and deterministic skill pattern extraction.", table_cell)
        ],
        [
            Paragraph("<b>Database</b>", table_cell),
            Paragraph("Supabase (PostgreSQL)", table_cell),
            Paragraph("Cloud PostgreSQL instance with Row Level Security (RLS) policies for feedback and resume storage.", table_cell)
        ],
        [
            Paragraph("<b>Deployment</b>", table_cell),
            Paragraph("Vercel (Frontend), Render (Backend)", table_cell),
            Paragraph("Global CDN edge delivery for React SPA and dedicated containerized Python runtime with Dockerfile/Procfile.", table_cell)
        ]
    ]

    tech_table = Table(tech_data, colWidths=[80, 160, 264])
    tech_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), brand),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, slate_light]),
        ('GRID', (0,0), (-1,-1), 0.5, border_color),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 14))

    # ==========================================
    # 4. SYSTEM WORKFLOW & ARCHITECTURE
    # ==========================================
    story.append(Paragraph("4. End-to-End System Workflow", h1_style))
    story.append(Paragraph(
        "1. <b>Document Intake:</b> Candidate uploads a PDF resume. The system validates file signature, size (max 10MB), and format.<br/>"
        "2. <b>Text & Structure Parsing:</b> PyMuPDF extracts raw text, page count, and font layout metrics while Regex checks for contact links.<br/>"
        "3. <b>Feature Extraction & Classification:</b> Text is normalized and vectorized using TF-IDF. LinearSVC predicts career domain (or validates candidate target role).<br/>"
        "4. <b>Competency Audit:</b> The rule-based NLP engine scans for technical skills, computing intersection (matched) and set difference (missing).<br/>"
        "5. <b>Score Computation:</b> The composite scoring formula aggregates skill relevance, section presence, and keyword frequency into a 0-100 rating.<br/>"
        "6. <b>Persistence & Display:</b> Results are committed to Supabase PostgreSQL, and the frontend dynamically renders score gauges, feedback cards, and rewrites.",
        body_style
    ))
    story.append(Spacer(1, 10))

    # ==========================================
    # 5. REVIEWER VIVA / EVALUATION Q&A
    # ==========================================
    story.append(Paragraph("5. First Review Q&A Guide (Expected Questions & Answers)", h1_style))

    qas = [
        (
            "Q1: Why did you choose LinearSVC over deep learning models like BERT or LSTM?",
            "<b>Answer:</b> LinearSVC with TF-IDF features is optimized for sparse, high-dimensional text classification. "
            "It trains in seconds, runs inference in under 5 milliseconds, uses less than 2 MB of RAM, and requires zero GPU infrastructure. "
            "For classifying resumes into defined career tracks, it delivers state-of-the-art accuracy without the latency and deployment complexity of large language models."
        ),
        (
            "Q2: How does the system handle resumes with missing or varied section titles?",
            "<b>Answer:</b> The parser implements flexible regular expressions that accommodate industry synonyms (e.g., 'Work Experience', 'Employment History', 'Professional Background'). "
            "If a key section is absent, the section score is penalized, and an actionable recommendation is surfaced to the candidate."
        ),
        (
            "Q3: How is the Job Description Matcher calculated?",
            "<b>Answer:</b> Both the resume text and the job description are transformed into n-gram TF-IDF vector spaces. "
            "We compute the Cosine Similarity between the two vectors, which quantifies semantic and vocabulary alignment on a normalized 0% to 100% scale."
        ),
        (
            "Q4: How does data persistence work?",
            "<b>Answer:</b> Feedback, scores, detected skills, and extracted text are securely saved into a Supabase PostgreSQL database using PostgREST endpoints. "
            "The client frontend connects via a 'Database History' drawer to retrieve and reload previous reviews instantly."
        )
    ]

    for q, a in qas:
        story.append(Paragraph(f"<b>{q}</b>", h2_style))
        story.append(Paragraph(a, body_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 8))
    
    # Concluding Callout Box
    quote_text = (
        "<b>Project Philosophy:</b> <i>\"A resume is more than a document; it is a story of what someone is capable of doing. "
        "Through our AI, we transform those capabilities into something tangible for every candidate striving toward their dream career.\"</i>"
    )
    quote_table = Table([[Paragraph(quote_text, callout_style)]], colWidths=[504])
    quote_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), brand_light),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#818cf8")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 12),
        ('RIGHTPADDING', (0,0), (-1,-1), 12),
    ]))
    story.append(quote_table)

    # Build the PDF using NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Documentation PDF generated successfully at: {os.path.abspath(filename)}")

if __name__ == "__main__":
    build_pdf()

