from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel
from ingest import ingest_file_content
from query_engine import query_knowledge_base

app = FastAPI()

class QueryRequest(BaseModel):
    question: str
    user_role: str

@app.post("/ingest")
async def ingest_document_api(file: UploadFile = File(...), role: str = Form(...)):
    content = await file.read()
    chunks_ingested = ingest_file_content(content, file.filename, role)
    return {"message": f"Ingested {chunks_ingested} chunks from {file.filename} as {role}."}

@app.post("/query")
def ask_query(data: QueryRequest):
    answer = query_knowledge_base(data.question, data.user_role)
    return {"answer": answer}
