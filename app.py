import streamlit as st
import os
from src.helper import load_resume, process_resume, evaluate_resume, save_evaluation, determine_recommendation
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="Resume Screening App", layout="wide")
    
    st.title("📄 Resume Screening Application")
    st.write("Upload resumes in PDF or DOCX format for automated screening and evaluation.")

    # File upload section
    uploaded_files = st.file_uploader(
        "Upload Resumes", 
        type=["pdf", "docx"],
        accept_multiple_files=True,
        help="You can upload multiple resumes in PDF or DOCX format"
    )

    if uploaded_files:
        st.write(f"Number of files uploaded: {len(uploaded_files)}")
        
        # Create directories if they don't exist
        os.makedirs("temp", exist_ok=True)
        os.makedirs("output", exist_ok=True)

        evaluations = []
        progress_bar = st.progress(0)
        status_text = st.empty()

        for idx, uploaded_file in enumerate(uploaded_files):
            # Save uploaded file temporarily
            temp_path = os.path.join("temp", uploaded_file.name)
            try:
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())

                # Process the resume
                status_text.text(f"Processing {uploaded_file.name}...")
                
                # Add a small delay to ensure file is written
                time.sleep(1)
                
                data = load_resume(temp_path)
                resume_text = process_resume(data)
                evaluation = evaluate_resume(resume_text)
                
                recommendation = determine_recommendation(evaluation)
                
                evaluations.append({
                    "resume": uploaded_file.name,
                    "evaluation": evaluation,
                    "recommendation": recommendation
                })

                # Update progress
                progress = (idx + 1) / len(uploaded_files)
                progress_bar.progress(progress)

            except Exception as e:
                st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.remove(temp_path)

        # Clear progress indicators
        progress_bar.empty()
        status_text.empty()

        if evaluations:
            # Display results
            st.subheader("Evaluation Results")
            
            for eval_result in evaluations:
                with st.expander(f"📄 {eval_result['resume']} - {eval_result['recommendation']}"):
                    st.write("**Detailed Evaluation:**")
                    st.write(eval_result['evaluation'])
                    
                    if eval_result['recommendation'] == "Shortlist":
                        st.success(f"Recommendation: {eval_result['recommendation']}")
                    else:
                        st.error(f"Recommendation: {eval_result['recommendation']}")

            # Save results button
            if st.button("💾 Save Results to CSV"):
                try:
                    output_file = "output/evaluations.csv"
                    save_evaluation(output_file, evaluations)
                    st.success(f"Results saved successfully to {output_file}")
                    
                    # Add download button for the CSV
                    with open(output_file, 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="Download CSV",
                            data=f,
                            file_name="resume_evaluations.csv",
                            mime="text/csv"
                        )
                except Exception as e:
                    st.error(f"Error saving results: {str(e)}")

        # Cleanup temp directory
        if os.path.exists("temp"):
            try:
                os.rmdir("temp")
            except:
                pass

if __name__ == "__main__":
    main()