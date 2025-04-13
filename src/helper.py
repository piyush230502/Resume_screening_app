import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, UnstructuredWordDocumentLoader
from langchain.docstore.document import Document
from langchain.text_splitter import TokenTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_groq import ChatGroq
from src.prompt import prompt_template
import csv
import traceback

# Load environment variables
load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def load_resume(file_path):
    """Load resume from PDF or DOCX file"""
    try:
        if file_path.endswith('.pdf'):
            loader = PyPDFLoader(file_path)
        elif file_path.endswith('.docx'):
            loader = UnstructuredWordDocumentLoader(file_path)
        else:
            raise ValueError("Unsupported file format")
        return loader.load()
    except Exception as e:
        raise Exception(f"Error loading file: {str(e)}")

def process_resume(data):
    """Extract and clean text from resume"""
    try:
        text_splitter = TokenTextSplitter(chunk_size=3000, chunk_overlap=200)
        resume_text = ""
        for page in data:
            resume_text += page.page_content + "\n"
        
        # Split text if it's too long
        chunks = text_splitter.split_text(resume_text)
        return " ".join(chunks[:2])  # Use first 6000 tokens approximately
    except Exception as e:
        raise Exception(f"Error processing resume text: {str(e)}")

def evaluate_resume(resume_text):
    """Evaluate resume using Groq LLM"""
    try:
        # Initialize Groq LLM
        llm = ChatGroq(
            groq_api_key=GROQ_API_KEY,
            model_name="gemma2-9b-it",
            temperature=0.5,
            max_tokens=4096,
        )

        # Create prompt template
        prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["text"]
        )

        # Create an LLMChain
        chain = LLMChain(
            llm=llm,
            prompt=prompt,
        )

        # Run the chain
        response = chain.run(text=resume_text)
        return response.strip()
    except Exception as e:
        print(f"Evaluation error: {str(e)}")
        print(traceback.format_exc())
        raise Exception(f"Error in resume evaluation: {str(e)}")

def save_evaluation(output_file, evaluations):
    """Save evaluations to CSV file"""
    try:
        # Create output directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["Resume", "Evaluation", "Recommendation"])
            for evaluation in evaluations:
                csv_writer.writerow([
                    evaluation["resume"], 
                    evaluation["evaluation"], 
                    evaluation["recommendation"]
                ])
    except Exception as e:
        raise Exception(f"Error saving evaluations: {str(e)}")

def determine_recommendation(evaluation_text):
    """Determine recommendation based on evaluation text"""
    evaluation_lower = evaluation_text.lower()
    if any(keyword in evaluation_lower for keyword in ['excellent', 'strong', 'impressive', 'qualified']):
        return "Shortlist"
    elif "strengths" in evaluation_lower and not any(keyword in evaluation_lower for keyword in ['weak', 'lacking', 'insufficient']):
        return "Shortlist"
    else:
        return "Reject"

def screen_resumes(file_paths):
    """Screen multiple resumes"""
    evaluations = []
    for file_path in file_paths:
        try:
            data = load_resume(file_path)
            resume_text = process_resume(data)
            evaluation = evaluate_resume(resume_text)
            
            recommendation = determine_recommendation(evaluation)
            
            evaluations.append({
                "resume": os.path.basename(file_path),
                "evaluation": evaluation,
                "recommendation": recommendation
            })
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    return evaluations

# Example usage
if __name__ == "__main__":
    file_paths = ["path/to/resume1.pdf", "path/to/resume2.docx"]
    evaluations = screen_resumes(file_paths)
    save_evaluation("output/evaluations.csv", evaluations)