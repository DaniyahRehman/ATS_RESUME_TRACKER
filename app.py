from   dotenv import load_dotenv
load_dotenv()
import streamlit as st
import os
import base64
import io
from PIL import Image  # Correct import
import pdf2image
import google.generativeai as genai
print("GOOGLE_API_KEY:", os.getenv("GOOGLE_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
def get_gemini_response(input, pdf_content, prompt):
    if not pdf_content:
        raise ValueError("PDF content is empty")
    
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input, pdf_content[0], prompt])
    
    if response and hasattr(response, "text"):
        return response.text
    else:
        return "Error: No response received"


def input_pdf_setup(uploaded_file):
    if not uploaded_file:
        raise FileNotFoundError("No file uploaded")

    try:
        # Convert PDF to image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        if not images:
            raise ValueError("Could not extract images from PDF")

        first_page = images[0]

        # Convert into bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    except Exception as e:
        print("Error processing PDF:", str(e))
        raise
## Streamlit App
st.set_page_config(page_title="ATS Resume Expert")
st.header("ATS Tracking System")

# Job description input
input_text = st.text_area("Job Description:", key="input")

# File uploader
uploaded_file = st.file_uploader("Upload your resume (PDF)...", type=["pdf"])

# Ensure buttons are defined before using them
submit1 = st.button("Tell me About the Resume")
submit2 = st.button("Percentage Match")

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully")

    input_prompt1 = """
    You are an experienced HR with Tech experience in one of the following roles: Data Science, Full Stack Web Development, Big Data Engineering, DevOps, or Data Analysis.
    Your task is to review the provided resume against the job description and provide a professional evaluation.
    Highlight the candidate's strengths and weaknesses in relation to the specified job role.
    """

    input_prompt2 = """
    You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of job roles in Data Science, Full Stack Web Development, Big Data Engineering, DevOps, and Data Analysis.
    Your task is to evaluate the resume against the provided job description.
    Provide a percentage match score, highlight missing keywords, and offer final thoughts.
    """

    # Check button clicks AFTER defining them
    if submit1:
        if uploaded_file:
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(input_prompt1, pdf_content, input_text)
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")

    elif submit2:
        if uploaded_file:
            try:
                pdf_content = input_pdf_setup(uploaded_file)
                response = get_gemini_response(input_prompt2, pdf_content, input_text)
                st.subheader("The Response is")
                st.write(response)
            except Exception as e:
                st.error(f"Error: {e}")

