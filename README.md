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
  <img src="images/img2.png" width="45%" />
</p>

---

### 🔹 Results & Report

<p align="center">
  <img src="images/img3.png" width="45%" />
  <img src="images/img4.png" width="45%" />
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




<img width="735" height="702" alt="{349741B5-8196-493C-B39D-EF3D87BABCAE}" src="https://github.com/user-attachments/assets/3a838cfc-6c8b-4609-9403-9999fe410ffd" />

