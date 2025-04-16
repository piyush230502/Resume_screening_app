# 📄 **Project Report: Resume Screening Application with LangChain and Groq**

---

## 🧠 Project Overview

**Resume Screening Application** is an AI-powered, automated resume evaluation tool built using **Streamlit**, **LangChain**, and **Groq’s LLM**. It enables recruiters and HR professionals to upload multiple resumes (PDF or DOCX) and get instant, intelligent evaluations and shortlisting recommendations.

Instead of manually reviewing each resume, the app analyzes content using a prompt-based large language model approach, extracting relevant information about skills, experience, education, certifications, and communication quality, and outputs a recommendation to either **shortlist** or **reject**.

This tool aims to significantly reduce screening time, standardize evaluations, and make the recruitment process more efficient and consistent.

---

## 🎯 Objectives

- Provide a user-friendly interface for uploading multiple resumes.
- Extract and preprocess content from resumes in different formats (PDF, DOCX).
- Evaluate the resumes using a language model with a structured prompt.
- Return a concise summary of each resume along with a recommendation.
- Export results into a CSV format for record-keeping.

---

## 🧩 Key Components & File Description

### 1. `app.py` – **Main Streamlit UI Logic**
- Sets up the web interface for uploading resumes.
- Handles file processing, user interaction, and displays results.
- Uses a progress bar to indicate processing status.
- Calls functions from `helper.py` for core processing logic.
- Allows CSV export of the final evaluation results.

### 2. `helper.py` – **Processing & Evaluation Engine**
Handles core functionality such as:
- Loading resumes using `PyPDFLoader` or `UnstructuredWordDocumentLoader`.
- Text splitting using `TokenTextSplitter` for handling long documents.
- Integrating with **Groq’s gemma2-9b-it model** via LangChain to perform the evaluation.
- Determining if a resume should be "Shortlisted" or "Rejected" using rule-based analysis of model output.
- Saving evaluations to CSV.

### 3. `prompt.py` – **Prompt Template**
- Contains the structured natural language prompt used by the LLM.
- Guides the model to focus on:
  - Relevant skills
  - Experience
  - Education
  - Certifications
  - Projects
  - Communication skills
- Requests a final summary and recommendation from the LLM.

### 4. `requirements.txt` – **Dependencies**
Includes all Python libraries required to run the project:
- Core: `streamlit`, `langchain`, `langchain_groq`
- Resume handling: `pypdf`, `python-docx`, `unstructured`
- Environment setup: `python-dotenv`
- Tokenization, file reading, and utility: `tiktoken`, `faiss-cpu`, `PyPDF2`

---

## 🔁 Workflow Description

### Step 1: User Uploads Resumes
The app supports uploading multiple `.pdf` or `.docx` files. The uploaded files are saved temporarily in a local `temp` directory for processing.

### Step 2: Resume Parsing
Each resume is parsed based on its format:
- PDFs are loaded using `PyPDFLoader`.
- DOCX files are handled with `UnstructuredWordDocumentLoader`.
The text content is split using a token splitter to manage LLM token limits.

### Step 3: Evaluation by Groq LLM
The processed resume text is inserted into a prompt that provides instructions to the LLM. It is sent to the `gemma2-9b-it` model via Groq API using LangChain’s `LLMChain`.

### Step 4: Recommendation Generation
Once the response is received:
- If it contains words like “excellent,” “strong,” or “qualified,” the resume is shortlisted.
- Otherwise, it is marked for rejection.

### Step 5: Display and Save
The evaluations are displayed in the UI, expandable by resume file name, with detailed feedback and a recommendation banner. The results can also be saved into a downloadable `.csv` file.

---

## ⚙️ How to Run the Application

Here’s a complete guide to setting up and running this project on your local machine:

---

### 📁 Step 1: Prepare the Environment
Create a project directory and place the following files inside:
- `app.py`
- `helper.py`
- `prompt.py` (inside a folder named `src`)
- `requirements.txt`

The structure should look like:
```
resume_screening_app/
│
├── app.py
├── requirements.txt
└── src/
    ├── helper.py
    └── prompt.py
```

---

### 🐍 Step 2: Create a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

---

### 📦 Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

### 🔐 Step 4: Set Up Your Environment Variables
Create a `.env` file in the root directory and add your Groq API key:
```
GROQ_API_KEY=your_actual_groq_api_key
```

You can get the API key by signing up at: [https://console.groq.com](https://console.groq.com)

---

### ▶️ Step 5: Run the Streamlit App
From the terminal, run:
```bash
streamlit run app.py
```

This will launch the application in your browser at `http://localhost:8501`.

---

## 📊 Using the Application

1. Click **Upload Resumes** and select one or more `.pdf` or `.docx` files.
2. The app will:
   - Show a progress bar as each resume is evaluated.
   - Display a detailed evaluation summary for each file.
   - Show the AI’s recommendation (`Shortlist` or `Reject`).
3. Optionally, click “💾 Save Results to CSV” to save and download the results.

---

## 🧪 Example Prompt Input to Groq LLM

```text
You are an expert at evaluating resumes...
[text extracted from resume]
Evaluate the resume based on...
Provide a summary of the evaluation...
```

---

## ✅ Advantages

- 🔍 **Objective Evaluation** using AI reduces human bias.
- ⏱️ **Time Efficiency** – evaluate multiple resumes in seconds.
- 📊 **Structured Feedback** for each candidate.
- 💾 **CSV Export** for easy integration with HR tools.

---

## 💡 Future Improvements

- Add support for parsing structured job descriptions and matching them with resumes.
- Introduce scoring metrics for transparency (e.g., 8/10 on skills, 9/10 on experience).
- Enable conversational AI chat with each resume.
- Deploy to **Streamlit Cloud**, **Hugging Face Spaces**, or **AWS Lambda**.

---
