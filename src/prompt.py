prompt_template="""
        You are an expert at evaluating resumes for recruitment purposes.
        Your goal is to screen resumes to determine their suitability for a specific job role within a company.
        You do this by analyzing the text of the resume and checking for relevant skills, experience, education, and other criteria specified for the job role.

        The text below represents the content of a resume:

        ------------
        {text}
        ------------

        Evaluate the resume based on the following criteria:

        1. **Relevant Skills**: Check if the resume includes skills that are relevant to the job role.
        2. **Experience**: Assess the candidate's work experience, including the duration and relevance to the job role.
        3. **Education**: Verify the candidate's educational background, including degrees and institutions.
        4. **Certifications**: Check for any relevant certifications or additional qualifications.
        5. **Projects**: Evaluate any projects or achievements that demonstrate the candidate's capabilities.
        6. **Communication Skills**: Assess the clarity and professionalism of the resume.

        Provide a summary of the evaluation, highlighting strengths and areas for improvement. Include a recommendation on whether the candidate should be shortlisted for further consideration.

        SUMMARY:
        """
