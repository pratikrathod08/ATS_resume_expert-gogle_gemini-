from dotenv import load_dotenv

load_dotenv()

import streamlit as st 
import os
import base64
import io
from PIL import Image
import pdf2image   

import google.generativeai as genai

## configure google gemini with api key 
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))


def get_geminy_response(input , pdf_content, prompt):

    model = genai.GenerativeModel("gemini-pro-vision")   ## make generative model 

    response = model.generate_content([input,pdf_content[0],prompt])     ## get response from model 
     ## pdf_content = img_format of pdf 1st page , prompt = output from model what we want.

    return response.text



def input_pdf_setup(uploaded_file):

    """ function for convert pdf to image"""

    if uploaded_file is not None:
        ## convert pdf to image
        images = pdf2image.convert_from_bytes(uploaded_file.read(),poppler_path=r"C:\Program Files\poppler-23.11.0\Library\bin")

        first_page = images[0]  ## get first page of resume

        ## convert to bytes  
        img_byte_arr = io.BytesIO()    ## object of bytes.io
        first_page.save(img_byte_arr, format='JPEG')  ## save first page as bytes
        img_byte_arr = img_byte_arr.getvalue()  ## getting value.

        pdf_parts = [
            {
                "mime_type" : "image/jpeg",
                "data" : base64.b64encode(img_byte_arr).decode()  # encode image data to base64 and decode to string
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError('No file uploaded')

## streamlit app 

# st.set_page_config(page_title = "ATS Resume Expert")
st.header("ATS Tracking System")
input_text = st.text_area("job Description: ", key = "input")                          ## get job description for match ats score

uploaded_file = st.file_uploader("Upload your resume(PDF)...", type=['pdf'])           ## get uploaded resume file.

if uploaded_file is not None:
    st.write("pdf uploaded successfully")

submit1 = st.button("tell me about the resume")

submit2 = st.button("Score and matching from resume")

## prompt for get detail of resume 
input_prompt1 = """
you are an experienced hr with good understanding of resume and technical and people skills of all type of fields.
from provided resume you need to saperate data contents and give to proper format like below in json format
Education/study:
name:
email:
mobileNumber:
Experience:
"""

## prompt for match ats score.
input_prompt2 = """
You are an skilled ATS (Applicant Tracking System) scanner with a deep understanding of data science and ATS functionality, 
your task is to evaluate the resume against the provided job description. give me the percentage of match if the resume matches
the job description. First the output should come as percentage and then keywords missing and last final thoughts.
"""



## final code for process 

if submit1:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_geminy_response(input_prompt1 , pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("please upload the resume")
elif submit2:
    if uploaded_file is not None:
        pdf_content = input_pdf_setup(uploaded_file)
        response = get_geminy_response(input_prompt2 , pdf_content, input_text)
        st.subheader("The response is")
        st.write(response)
    else:
        st.write("please upload the resume")

    


