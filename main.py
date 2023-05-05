import PyPDF2
from helper import Pages, text_correct_sugg
from fastapi import FastAPI, HTTPException, UploadFile, File,Form
import docx
from typing import Annotated
import io
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
import io
import docx

app = FastAPI()
FILE_NAME = ""
# @app.get("/")
# async def root():
#     return {"message": "Hello World"}

@app.post('/page_count')
async def page_count(file: UploadFile = File(...)):
    try:
        global FILE_NAME 
        FILE_NAME = file
        pages, Twords = Pages(file)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": {"pages":pages,
                        
                        "words":Twords}}



@app.post("/make_changes")
async def make_changes():
    doc1, doc2 =  text_correct_sugg(FILE_NAME)
    buffer = io.BytesIO()
    buffer1 = io.BytesIO()

    doc1.save(buffer)
    buffer.seek(0)
    doc2.save(buffer1)
    buffer1.seek(0)
    
    headers = {
        "Content-Disposition": 'attachment; filename="correct.docx"',
    }
    return StreamingResponse(buffer, headers=headers, media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')