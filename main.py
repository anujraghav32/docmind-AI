from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pypdf import PdfReader
from agents_logic import run_agentic_process
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.post("/process")
async def process_pdf(file: UploadFile = File(...)):
    try:
        content = await file.read()
        pdf = PdfReader(io.BytesIO(content))
        text = "".join([page.extract_text() for page in pdf.pages])

        result = run_agentic_process(text[:10000])
        return {"result": str(result)}
    except Exception as e:
        return {"error": str(e)}
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
