import nltk
from spacy.tokens import Token
import pandas as pd

# Define a custom tokenizer exception
Token.set_extension('POS', default='', force=True)

nltk.download('stopwords')
nltk.download('en_core_web_sm')

from pyresparser import ResumeParser
from pdf2docx import Converter

import os
from docx import Document
import datetime


import streamlit as st
import os
import PyPDF2 as pdf


pdf_file = "deepak.pdf"  # Replace with your PDF file path
docx_file = "output.docx"  # Replace with the desired DOCX file path

def scanResume(docs_path):
    data = ResumeParser(docs_path).get_extracted_data()
    return data


nput_prompt= """
Hey Act Like a skilled or very experience ATS(Application Tracking System)
with a deep understanding of tech field,software engineering,data science ,data analyst
and big data engineer. Your task is to evaluate the resume based on the given job description.
You must consider the job market is very competitive and you should provide 
best assistance for improving thr resumes. Assign the percentage Matching based 
on Jd and
the missing keywords with high accuracy
resume:{text}
description:{jd}

I want the response in one single string having the structure
{{"JD Match":"%","MissingKeywords:[]","Profile Summary":""}}
"""

def pdf_to_docx(pdf_path, docx_path):
    # Convert PDF to DOCX
    cv = Converter(pdf_path)
    cv.convert(docx_path, start=0, end=None)
    cv.close()

def input_pdf_text(uploaded_file):
    reader= pdf.PdfReader(uploaded_file)
    teXt=""
    for page in range(len(reader.pages)):
        page=reader.pages[page]
        text=str(page.extract_text())
    return text 


def convert_pdf_to_docx(uploaded_file):
    # Save the uploaded PDF file
    with open("uploaded.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Convert PDF to DOCX
    docx_path = "converted.docx"
    cv = Converter("uploaded.pdf")
    cv.convert(docx_path, start=0, end=None)
    cv.close()

    return docx_path

uploaded_files= st.file_uploader("Upload your resume",type="pdf", help="Please upload the pdf",accept_multiple_files=True)

submit = st.button("Submit")

list = []

if submit:
    for uploaded_file in uploaded_files:
        print(uploaded_file)
        if uploaded_file is not None:
            docx_path = convert_pdf_to_docx(uploaded_file)
            response= scanResume(docx_path)
            list.append(response)
            st.subheader(response)
    pd.DataFrame(list).to_csv('cvList.csv')


    
