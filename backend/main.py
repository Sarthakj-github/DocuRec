from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
import easyocr
import numpy as np
import re
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()
reader = easyocr.Reader(['en'])  # Initialize OCR reader

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins; replace with your frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class DocumentData(BaseModel):
    name: str
    document_number: str
    expiration_date: str


def find_max_date_from_various_formats(date_list):
    date_formats = [
        "%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%m/%d/%Y", "%d.%m.%Y", "%Y.%m.%d", "%d %b %Y", "%d %B %Y", "%b %d, %Y", "%B %d, %Y"
    ]
    
    def convert_to_dd_mm_yyyy(date_str):
        for date_format in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, date_format)
                return parsed_date.strftime("%d/%m/%Y")
            except ValueError:
                continue
        return None

    valid_dates = [convert_to_dd_mm_yyyy(date) for date in date_list if convert_to_dd_mm_yyyy(date) is not None]

    if valid_dates:
        return max(valid_dates, key=lambda x: datetime.strptime(x, "%d/%m/%Y"))
    return None

def extract_info(text, doc_type):
    # Regex patterns for finding details
    if doc_type == 'passport':
        name_pattern = r"(?:[A-Za-z]<[A-Za-z]{3}<<)?([A-Za-z]+)(<)(<)?(([A-Za-z]+<)+)(?=<+.*)"
        doc_number_pattern = r"\b[A-Za-z][0-9]{7}\b"
        expiry_pattern = r"\b\d{2}[-/]\d{2}[-/]\d{4}\b"
    else:
        name_pattern = r"([A-Z]{4,}\s[A-Z]+)(\s[A-Z]+)?"
        doc_number_pattern = r"([A-Za-z]{2})([-\s]+)?(\d{2})([-\s])?(\d{4})([-\s])?(\d{7})"  
        expiry_pattern = r"\b\d{2}[-/]\d{2}[-/]\d{4}\b"

    name = re.findall(name_pattern, text)
    doc_number = re.findall(doc_number_pattern, text)
    expiration_date = re.findall(expiry_pattern, text)
    
    if name and doc_type=='passport':
        L=''.join(name[0])
        L=L.split('<')
        if L[-1]=='':
            L.pop()
        if L[1]=='':
            L.append(L.pop(0))
        s=set()
        name=''
        for i in L:
            if i not in s:
                name+=i.upper()+' '
                s.add(i)
        name=[tuple(name[:-1],)]
    
    if expiration_date:
        expiration_date=(find_max_date_from_various_formats(expiration_date),)
    
    print(name)
    return {
        # "all":name,
        "name": name[0] if name else "N/A",
        "document_number": doc_number[0] if doc_number else "N/A",
        "expiration_date": expiration_date if expiration_date else "N/A"
    }

@app.post("/upload")
async def upload_file(image: UploadFile = File(...), type: str = Form('passport')):
    content = await image.read()
    with open("temp_image.jpg", "wb") as f:
        f.write(content)
    
    # OCR Extraction on the preprocessed image
    text = reader.readtext("temp_image.jpg", detail=0)
    extracted_text = " ".join(text)

    # Extract information based on document type
    extracted_data = extract_info(extracted_text, type)

    return extracted_data