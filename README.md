# SmartResume AI – Resume Analyzer & Job Matcher

## 📌 Overview
SmartResume AI is a local AI-powered tool that analyzes a candidate’s resume and compares it with a job description.  
It provides a match score, identifies skill gaps, and gives actionable suggestions to improve the resume.

The application runs completely locally using open-source tools.

---

## 🚀 Features

- 📄 Upload Resume (PDF)
- 📝 Enter Job Description
- 🎯 Match Score (Semantic Similarity)
- 🧠 Skill Gap Analysis (Matched & Missing Skills)
- 💡 Strengths & Improvement Suggestions
- 📊 Skill Match Ratio (Evaluation Metric)
- 📥 Downloadable Report (PDF & TXT)
- ⚠️ Edge Case Handling
- 🔄 Retry mechanism

---

## 🖼️ Application Screenshots

### 🔹 Input Section
![Input UI](images/<img width="741" height="705" alt="{B54E670D-2506-4F37-B21A-31F8706C3E99}" src="https://github.com/user-attachments/assets/b06d8f25-e21b-4750-a018-9af67a9d9094" />
)

---

### 🔹 Results Section
![Results UI](images/result_ui.png)

---

### 🔹 Generated Report
![Report Output](images/report_output.png)

---

## 🛠️ Tech Stack

- **Frontend/UI**: Streamlit  
- **PDF Processing**: PyMuPDF  
- **NLP & Embeddings**: sentence-transformers  
- **Model**: all-MiniLM-L6-v2  
- **Report Generation**: ReportLab  

---

## ⚙️ How It Works

1. Extract resume text from PDF  
2. Take job description input  
3. Convert both into embeddings  
4. Compute cosine similarity (match score)  
5. Perform skill matching  
6. Generate strengths & improvements  
7. Create downloadable report  

---

## ▶️ How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
