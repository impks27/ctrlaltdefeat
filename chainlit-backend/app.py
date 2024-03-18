import os
# import uuid
from openai import AsyncOpenAI

from fastapi.responses import JSONResponse
from pydantic import BaseModel

from chainlit.auth import create_jwt
from chainlit.server import app
import chainlit as cl
import esg
import upload

from fastapi import FastAPI, Request, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import (
    HTMLResponse,
)
from typing import List, Optional

# CORS configuration allowing all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

class UploadedDocument(BaseModel):
    documentName: str
    metadata: dict

class RetrieveESGReportsRequest(BaseModel):
    reportYear: str

class RetrieveESGReportsResponse(BaseModel):
    documents: List[UploadedDocument]
    
# Define metadata_cache as an array of UploadedDocument
metadata_cache: List[UploadedDocument] = []

settings = {
    "model": "gpt-3.5-turbo",
    "temperature": 0.7,
    "max_tokens": 500,
    "top_p": 1,
    "frequency_penalty": 0,
    "presence_penalty": 0,
}

@app.get("/custom-auth")
async def custom_auth():
    # Verify the user's identity with custom logic.
    token = create_jwt(cl.User(identifier="Test User"))
    return JSONResponse({"token": token})

@cl.on_chat_start
async def on_chat_start():
    cl.user_session.set(
        "message_history",
        [{"role": "system", "content": "You are a helpful assistant."}],
    )
    await cl.Message(content="Connected to Chainlit!").send()


class Item(BaseModel):
   inputQuestion: str
   reportYear: str

@app.post("/questionnaire/generatefirstdraft/generateAnswer")
async def generateAnswer(item: Item):
    print(item)
    print(dir(item))
    obj = esg.ESGUtil();
    reportYear = item.reportYear
    inputQuestion = item.inputQuestion
    response = obj.generateAnswer(reportYear,inputQuestion)
    return {
  "reportYear": reportYear,
  "questionnireSummary": {
    "response": response,
    "status": "Success",
    "citation": "string",
    "documentReference": "string",
    "accuracy": "string",
    "confidenceScores": "string"
  }
}

@app.get("/esgreports/keepalive/ping")
async def ping(request: Request):
    print(request.headers)
    return {"status": "success", "message": "Ping successful"}


@app.post("/esgreports/retrieve", response_model=RetrieveESGReportsResponse)
async def retrieve_esg_reports(request: RetrieveESGReportsRequest):
    try:
        report_year = request.reportYear
        retrieved_documents = [UploadedDocument(**doc.dict()) for doc in metadata_cache if doc.metadata["reportYear"] == report_year]
        return RetrieveESGReportsResponse(documents=retrieved_documents)
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)}, status_code=500)
    
@app.post("/esgreports/retrievefile")
async def retrieve_esg_reportsfile(request: RetrieveESGReportsRequest):
    print(request.reportYear)
    obj = upload.BlobUtil();
    url = obj.get_blob_url("2021-annual-report")
    print(url)

@app.post("/esgreports/upload")
async def upload_esg_reportsfile(documentName: List[UploadFile] = File(...),
                             DocumentURL: List[str] = "DocumentURL",
                             YearOfReport: str = Form(...) ):
        print("Invoke upload_esg_reportsfile")
        print("YearOfReport: "+ YearOfReport)
        print(documentName)
        # Process each uploaded file
        for file in documentName:
            print("file")
            print(file)
            # Create the 'uploaded_files' directory if it doesn't exist
            os.makedirs("uploaded_files/" + YearOfReport, exist_ok=True)
            # Save the file in the 'uploaded_files' folder
            file_path = os.path.join('uploaded_files/'+ YearOfReport , file.filename)
            with open(file_path, 'wb') as buffer:
                buffer.write(await file.read())
            print("filename: "+ 'uploaded_files/'+ YearOfReport+ "/" + file.filename)
            with open('uploaded_files/'+ YearOfReport + "/" + file.filename, 'rb') as file1:
                # Pass the file object to the function
                obj = upload.BlobUtil()
                url = obj.upload_blob(file1, YearOfReport)
        
        return JSONResponse(content={"status": "Success", "message": "Document(s) Uploaded Successfully", "tracker_id": "uid1001"})
        
