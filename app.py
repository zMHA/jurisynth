import streamlit as st
import PyPDF2
import re
from transformers import pipeline
from fpdf import FPDF
import os
from wordfreq import word_frequency
from nltk.corpus import wordnet
import nltk

nltk.download('wordnet')
nltk.download('omw-1.4')

# ------------------ App Config ------------------ #
st.set_page_config(page_title="JuriSynth – Legal Analyzer", layout="wide")
st.title("📄 JuriSynth – Legal Document Analyzer")
st.markdown("""
Upload a legal document **PDF** to get a clause-level breakdown, keyword tagging, risk analysis, 
and AI-generated summary. You can also **edit** clauses, **explore difficult words**, and **download a PDF report**.
""")

# ------------------ Load AI Pipelines ------------------ #
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")
risk_labels = ["risky", "safe", "ambiguous"]

# ------------------ PDF Reader ------------------ #
def read_pdf(file):
    reader = PyPDF2.PdfReader(file)
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"
    return full_text

# ------------------ Clause Splitter ------------------ #
def split_into_clauses(text):
    if not text:
        return []
    parts = re.split(r'(?<=[.;])\s+|\n+', text)
    clauses = []
    temp = ""
    for part in parts:
        if part and isinstance(part, str):
            part = part.strip()
            temp += part + " "
            if len(temp.strip()) > 100:
                clauses.append(temp.strip())
                temp = ""
    if temp.strip():
        clauses.append(temp.strip())
    return clauses

# ------------------ Keyword Tagger ------------------ #
def extract_keywords(text):
    words = re.findall(r'\b\w+\b', text.lower())
    keywords = set([word for word in words if len(word) > 6])
    return list(keywords)[:10]

# ------------------ Risk Analyzer ------------------ #
def analyze_clause_risk(clause):
    result = classifier(clause, risk_labels)
    return result['labels'][0], result['scores'][0]

# ------------------ Text Summarizer ------------------ #
def summarize_text(text):
    chunks = [text[i:i+1000] for i in range(0, len(text), 1000)]
    summaries = []
    for chunk in chunks:
        summary = summarizer(chunk, max_length=100, min_length=30, do_sample=False)[0]['summary_text']
        summaries.append(summary)
    return " ".join(summaries)

# ------------------ Difficult Word Finder ------------------ #
def is_difficult(word, threshold=1e-5):
    return word_frequency(word, 'en') < threshold

def get_simple_definition(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return synsets[0].definition()
    return "Definition not available."

def find_difficult_words(text):
    words = re.findall(r'\b\w+\b', text.lower())
    difficult = set()
    for word in words:
        if is_difficult(word):
            definition = get_simple_definition(word)
            difficult.add((word, definition))
    return list(difficult)[:5]  # show max 5

# ------------------ PDF Generator ------------------ #
def generate_pdf(summary, risky_clauses):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    def safe_text(text):
        return text.encode('latin-1', 'replace').decode('latin-1')

    pdf.multi_cell(0, 10, safe_text("📄 JuriSynth – Legal Summary Report"), align="C")
    pdf.ln(5)
    pdf.multi_cell(0, 10, safe_text(summary))
    pdf.ln(10)

    if risky_clauses:
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, safe_text("⚠️ Risky Clauses:"), align="L")
        for idx, clause in enumerate(risky_clauses):
            pdf.set_font("Arial", size=10)
            pdf.multi_cell(0, 8, safe_text(f"{idx+1}. {clause}"))
            pdf.ln(1)

    filepath = "/tmp/jurisynth_summary.pdf"
    pdf.output(filepath)
    return filepath

# ------------------ Main App Flow ------------------ #
uploaded_file = st.file_uploader("📤 Upload PDF file", type=["pdf"])

if uploaded_file:
    raw_text = read_pdf(uploaded_file)
    clauses = split_into_clauses(raw_text)
    summary = summarize_text(raw_text)

    st.success(f"✅ Processed {len(clauses)} clauses.")
    st.markdown("## 📝 AI-Generated Summary")
    st.markdown(summary)
    st.markdown("---")

    # Analyze Clause Risks
    st.markdown("## 🔍 Clause-Level Analysis")
    risky_clauses = []

    for i, clause in enumerate(clauses):
        label, score = analyze_clause_risk(clause)
        if label == "risky":
            risky_clauses.append(clause)

        color = {
            "risky": "#FFD2D2",
            "safe": "#D2FFD2",
            "ambiguous": "#FFFFD2"
        }.get(label, "#FFFFFF")

        with st.container():
            st.markdown(f"### Clause {i+1}")
            edited_clause = st.text_area(f"✏️ Edit Clause {i+1}", value=clause, key=f"edit_{i}")
            st.markdown(
                f"""
                <div style='background-color:{color}; padding:10px; border-radius:5px; color:#000;'>
                    <b>Risk:</b> {label.capitalize()} ({score:.2f})
                </div>
                """,
                unsafe_allow_html=True
            )
            st.markdown(f"🔑 **Keywords**: `{', '.join(extract_keywords(edited_clause))}`")

            difficult_words = find_difficult_words(edited_clause)
            if difficult_words:
                with st.expander("📘 Difficult Words in Simple English"):
                    for word, meaning in difficult_words:
                        st.markdown(f"- **{word.capitalize()}** → _{meaning}_")

            st.markdown("---")

    # PDF Report Download
    st.markdown("## 📥 Export Summary Report")
    if st.button("Generate PDF Report"):
        with st.spinner("Creating PDF..."):
            pdf_path = generate_pdf(summary, risky_clauses)
            with open(pdf_path, "rb") as f:
                st.download_button("📄 Download Report as PDF", f, file_name="JuriSynth_Summary.pdf")
    st.caption("🔐 All processing is done locally using open-source transformers.")
