import base64
from fastapi import FastAPI, UploadFile, File
from typing import List

app = FastAPI()

@app.post("/uploadfiles/")
async def upload_file(files: List[UploadFile] = File(...)):
    contents = []
    for file in files:
        try:
            # Attempt to read and decode as UTF-8 text
            content = await file.read()
            content = content.decode('utf-8')
        except UnicodeDecodeError:
            # If decode fails, handle as binary data
            content = base64.b64encode(await file.read()).decode('utf-8')
        
        contents.append({"filename": file.filename, "content": content})
    return contents
