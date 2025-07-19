import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Enterprise Knowledge Base Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem 0;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        color: white;
        border-radius: 0 0 20px 20px;
    }
    
    .main-header h1 {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .main-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin: 0;
    }
    
    .section-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border: 1px solid #e1e8ed;
    }
    
    .upload-section {
        background: linear-gradient(135deg, #3bd2f7 0%, #c3cfe2 100%);
        border-left: 5px solid #667eea;
    }
    
    .query-section {
        background: linear-gradient(135deg, #f5a333 0%, #fcb69f 100%);
        border-left: 5px solid #ff6b6b;
    }
    
    .stSelectbox > div > div > div {
        background-color: #6daded;
        border: 2px solid #e9ecef;
        border-radius: 10px;
    }
    
    .stTextInput > div > div > input {
        background-color: #37a4ed;
        border: 2px solid #e9ecef;
        border-radius: 10px;
        padding: 0.75rem;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .upload-button > button {
        background: linear-gradient(90deg, #4CAF50 0%, #45a049 100%);
        box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
    }
    
    .query-button > button {
        background: linear-gradient(90deg, #ff6b6b 0%, #ee5a52 100%);
        box-shadow: 0 4px 15px rgba(255, 107, 107, 0.3);
    }
    
    .role-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin-left: 0.5rem;
    }
    
    .employee-badge {
        background-color: #e3f2fd;
        color: #1976d2;
    }
    
    .manager-badge {
        background-color: #f3e5f5;
        color: #7b1fa2;
    }
    
    .admin-badge {
        background-color: #ffebee;
        color: #c62828;
    }
    
    .answer-box {
        background: linear-gradient(135deg, #e8f5e8 0%, #f0f8f0 100%);
        border-left: 5px solid #4CAF50;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.markdown("""
<div class="main-header">
    <h1>🧠 Enterprise Knowledge Base Assistant</h1>
    <p>Powered by Gemini AI & ChromaDB | Secure Role-Based Access</p>
</div>
""", unsafe_allow_html=True)

# Create two columns for better layout
col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown("""
    <div class="section-card upload-section">
        <h2>📄 Document Upload Center</h2>
        <p>Upload PDF documents to expand the knowledge base</p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a PDF Document", 
        type='pdf',
        help="Upload PDF files to add to the knowledge base"
    )
    
    doc_role = st.selectbox(
        "🔐 Document Access Level:", 
        ["employee", "manager", "admin"],
        help="Set who can access this document"
    )
    
    # Add role badge
    role_colors = {
        "employee": "employee-badge",
        "manager": "manager-badge", 
        "admin": "admin-badge"
    }
    
    st.markdown(f"""
    <div style="margin-top: -1rem; margin-bottom: 1rem;">
        <span class="role-badge {role_colors[doc_role]}">
            {doc_role.upper()} ACCESS
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="upload-button">', unsafe_allow_html=True)
    upload_clicked = st.button("🚀 Upload & Ingest Document", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if upload_clicked:
        if uploaded_file:
            with st.spinner("Processing document... Please wait"):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                data = {"role": doc_role}
                try:
                    res = requests.post("http://localhost:8000/ingest", files=files, data=data)
                    
                    # Check if request was successful
                    if res.status_code == 200:
                        try:
                            response_data = res.json()
                            message = response_data.get("message", "Document uploaded and ingested successfully!")
                            st.success(f"✅ {message}")
                        except requests.exceptions.JSONDecodeError:
                            st.error("❌ Received invalid response from server")
                            st.text(f"Response content: {res.text}")
                    else:
                        st.error(f"❌ Server error: {res.status_code}")
                        st.text(f"Response: {res.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to server. Make sure the backend is running on http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Error uploading document: {str(e)}")
        else:
            st.warning("⚠️ Please upload a PDF document first.")

with col2:
    st.markdown("""
    <div class="section-card query-section">
        <h2>🤖 AI Query Interface</h2>
        <p>Ask questions and get intelligent answers from your knowledge base</p>
    </div>
    """, unsafe_allow_html=True)
    
    user_role = st.selectbox(
        "👤 Your Role:", 
        ["employee", "manager", "admin"],
        help="Select your role to ensure proper access permissions"
    )
    
    # Add role badge for user
    st.markdown(f"""
    <div style="margin-top: -1rem; margin-bottom: 1rem;">
        <span class="role-badge {role_colors[user_role]}">
            LOGGED IN AS {user_role.upper()}
        </span>
    </div>
    """, unsafe_allow_html=True)
    
    question = st.text_input(
        "💬 Enter your question:",
        placeholder="Type your question here...",
        help="Ask anything about the uploaded documents"
    )
    
    st.markdown('<div class="query-button">', unsafe_allow_html=True)
    ask_clicked = st.button("🔍 Ask Knowledge Base", use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    if ask_clicked:
        if question.strip():
            with st.spinner("Thinking... Getting your answer"):
                payload = {"question": question, "user_role": user_role}
                try:
                    res = requests.post("http://localhost:8000/query", json=payload)
                    
                    # Check if request was successful
                    if res.status_code == 200:
                        try:
                            response_data = res.json()
                            answer = response_data.get("answer", "No answer received")
                            
                            st.markdown(f"""
                            <div class="answer-box">
                                <h4>🎯 Answer:</h4>
                                <p>{answer}</p>
                            </div>
                            """, unsafe_allow_html=True)
                        except requests.exceptions.JSONDecodeError:
                            st.error("❌ Received invalid response from server")
                            st.text(f"Response content: {res.text}")
                    else:
                        st.error(f"❌ Server error: {res.status_code}")
                        st.text(f"Response: {res.text}")
                        
                except requests.exceptions.ConnectionError:
                    st.error("❌ Cannot connect to server. Make sure the backend is running on http://localhost:8000")
                except Exception as e:
                    st.error(f"❌ Error getting answer: {str(e)}")
        else:
            st.warning("⚠️ Please enter a question first.")

# Sidebar with additional information
with st.sidebar:
    st.markdown("### 📊 System Status")
    st.info("🟢 Knowledge Base Online")
    st.info("🟢 Gemini AI Connected")
    st.info("🟢 ChromaDB Active")
    
    st.markdown("### 🔒 Access Levels")
    st.markdown("""
    - **Employee**: Basic access
    - **Manager**: Enhanced access
    - **Admin**: Full access
    """)
    
    st.markdown("### 💡 Tips")
    st.markdown("""
    - Upload PDF documents to expand knowledge
    - Use specific questions for better results
    - Check your role permissions
    - Documents are processed automatically
    """)
