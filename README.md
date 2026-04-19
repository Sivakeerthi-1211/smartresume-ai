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

### 🔹 Input & Processing

<p align="center">
  <img src="https://github.com/user-attachments/assets/a3276192-bea6-41f2-b7ac-928a6957d104" width="45%" />
  <img src="https://github.com/user-attachments/assets/788581e1-abc9-4e4c-8a59-50a5e0a3857a" width="45%" />
</p>


---

### 🔹 Results & Report

<p align="center">
  <img src="https://github.com/user-attachments/assets/36466862-e5f9-4884-8423-e7cf9a867d07" width="45%" />
  <img src="https://github.com/user-attachments/assets/ebbf5c26-730b-49bf-8a1e-686f0da38f92" width="45%" />
</p>



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
