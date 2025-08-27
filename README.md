# 🦀 JuriSynth – Legal Document Summarizer with Risk Analyzer

JuriSynth is an **AI-powered legal document analyzer** built using [Streamlit](https://streamlit.io/) and 🤗 [Transformers](https://huggingface.co/transformers/).  
It helps users — especially **startups, freelancers, and non-lawyers** — understand complex legal documents by breaking them down into **actionable insights**.

---

## 🚀 Features
- 📤 Upload legal **PDF documents**  
- 🧠 **AI-generated document summary**  
- ✂️ **Clause-level analysis** and editing  
- ⚠️ **Risk classification**: Safe, Risky, or Ambiguous  
- 🔑 **Keyword extraction**  
- 📘 Difficult word explanations using **WordNet**  
- 📄 **PDF report generator** with highlighted risky clauses  

---

## 📂 How It Works
1. **Upload** a PDF document.  
2. The app:  
   - Extracts the text  
   - Splits it into clauses  
   - Uses AI to summarize the content  
   - Classifies each clause by risk (via zero-shot learning)  
   - Highlights keywords and difficult terms  
3. You can **edit clauses**, view definitions, and **download a summary report**.  

---

## 🛠️ Technologies Used
- [Streamlit](https://streamlit.io/) – User Interface  
- 🤗 [Transformers](https://huggingface.co/transformers/)  
   - `facebook/bart-large-mnli` – zero-shot classification  
   - `sshleifer/distilbart-cnn-12-6` – summarization  
- [PyPDF2](https://pypi.org/project/PyPDF2/) – PDF text extraction  
- [NLTK + WordNet](https://www.nltk.org/) – vocabulary simplification  
- [fpdf](https://pypi.org/project/fpdf/) – PDF report generation  

---

## 🧪 Example Use Cases
- 📄 Non-disclosure agreements (NDAs)  
- 🧾 Service contracts  
- 🏠 Lease agreements  
- 🤝 Partnership terms  
- 🧑‍⚖️ Freelance job contracts  

---

## 🔒 Data Privacy
All processing is done **locally** in your browser or in Hugging Face’s **sandboxed container**.  
➡️ **No data is stored or shared.**

---

## 📎 Citation
If you use this project or find it helpful, please **cite it** or ⭐ the repo on GitHub / Hugging Face!  

---

## 👨‍💻 Developed By
**Muhammad Hasnain**  
MS in Artificial Intelligence  
Researcher | Educator | Developer  

📧 [Email](mailto:hasnainmughal1998@gmail.com)  

---

## 📌 License
This project is open-source and released under the [MIT License](LICENSE).  
