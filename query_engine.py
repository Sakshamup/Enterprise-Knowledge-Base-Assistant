from langchain.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from config import GEMINI_API_KEY, CHROMA_DB_PATH

embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GEMINI_API_KEY)
vectordb = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embeddings)

retriever = vectordb.as_retriever(search_kwargs={"k": 5})
llm = GoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=GEMINI_API_KEY)

qa_chain = ConversationalRetrievalChain.from_llm(llm, retriever=retriever)
chat_history = []

def query_knowledge_base(query, user_role):
    docs = retriever.get_relevant_documents(query)
    filtered = [doc.page_content for doc in docs if doc.metadata.get('role') == user_role]

    if not filtered:
        return "No relevant data found for your role."

    context = " ".join(filtered)
    result = qa_chain({
        "question": f"Context: {context}\nQuestion: {query}",
        "chat_history": chat_history
    })
    chat_history.append((query, result['answer']))

    return result['answer']
