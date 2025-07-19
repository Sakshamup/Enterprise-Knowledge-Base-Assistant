import tempfile
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import PyPDFLoader
from langchain.vectorstores import Chroma
from config import GEMINI_API_KEY, CHROMA_DB_PATH

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)

def ingest_file_content(file_content, filename, role='employee'):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_content)
        temp_path = tmp.name

    loader = PyPDFLoader(temp_path)
    documents = loader.load()

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(documents)

    vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)

    texts = [chunk.page_content for chunk in chunks]
    metadata = [{'source': filename, 'role': role} for _ in texts]

    vectordb.add_texts(texts, metadatas=metadata)
    vectordb.persist()

    return len(texts)
