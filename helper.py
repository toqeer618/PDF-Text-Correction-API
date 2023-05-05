import os
import openai
import PyPDF2
import docx
from tqdm import tqdm
import io


def import_key():
    API_KEY = 'sk-xxxxxx' # you api key here
    openai.api_key = API_KEY

    return openai

def Pages(file):
    file = open(file.filename, 'rb') 
    ReadPDF = PyPDF2.PdfReader(file)
    pages = len(ReadPDF.pages)
    print(pages)
    TWords = 0
    for i in range(pages):
        pageObj = ReadPDF.pages[i]
        text = pageObj.extract_text()
        TWords+=len(text.split(' '))
    return pages, TWords

def write_in_docs(text):
# create document object
    doc = docx.Document()
    doc.add_paragraph(text)
    return doc

def suggest_changes(text, openai):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Please list the changes we should make in the below text each point is suggesting a change we should make\n"+text}
        ]

    )
    return response['choices'][0]['message']['content']

def correction(text, openai):
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Could you please correct the following paragraph?\n"+text}
        ]

    )
    return response['choices'][0]['message']['content']
def text_correct_sugg(file):
    openai = import_key()
    file = open(file.filename, 'rb') 
    ReadPDF = PyPDF2.PdfReader(file)
    pages = len(ReadPDF.pages)
    prev_text = ""
    correct = ""
    suggest = ""
    for i in tqdm(range(pages-15)):
        pageObj = ReadPDF.pages[i]
        text = pageObj.extract_text()
        TEXT = text.split('.')[:-1]
        new_text = prev_text
        for sent in TEXT:
            new_text+=sent+". "
        correct+="Page No. "+str(i)+"\n"+correction(new_text, openai)+"\n"
        suggest+="Page No. "+str(i)+"\n"+suggest_changes(new_text, openai)+"\n"
        prev_text = text.split('.')[-1]
    doc1 = write_in_docs(correct)
    doc2 = write_in_docs(suggest)
    return doc1, doc2
