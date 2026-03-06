import streamlit as st
import requests
import json
import time

# --- Configuration ---
API_BASE_URL = "http://127.0.0.1:8000"
st.set_page_config(
    page_title="Semantic ETL Console", 
    page_icon="✨", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Styling ---
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0px;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        font-weight: bold;
        border-radius: 8px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    }
    .metric-card {
        background-color: #F8FAFC;
        border-radius: 10px;
        padding: 1.5rem;
        border: 1px solid #E2E8F0;
    }
</style>
""", unsafe_allow_html=True)

# --- Application State ---
if 'cleaned_markdown' not in st.session_state:
    st.session_state.cleaned_markdown = None
if 'metadata' not in st.session_state:
    st.session_state.metadata = None
if 'tables' not in st.session_state:
    st.session_state.tables = []
if 'chunks' not in st.session_state:
    st.session_state.chunks = None

# --- API Interaction Functions ---
def check_api_health():
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=2)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def clean_file(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    try:
        response = requests.post(f"{API_BASE_URL}/v1/clean", files=files)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None

def chunk_text(markdown_content):
    payload = {"markdown": markdown_content}
    try:
        response = requests.post(f"{API_BASE_URL}/v1/chunk", json=payload)
        if response.status_code == 200:
            return response.json().get("chunks", [])
        else:
            st.error(f"API Error ({response.status_code}): {response.text}")
            return None
    except Exception as e:
        st.error(f"Failed to connect to API: {str(e)}")
        return None

# --- UI layout ---

# Sidebar for Status
with st.sidebar:
    st.title("⚙️ System Status")
    is_api_up = check_api_health()
    if is_api_up:
        st.success("🟢 API Server Online")
    else:
        st.error("🔴 API Server Offline")
        st.warning("Please run `uvicorn app.main:app` to start the backend.")
    
    st.markdown("---")
    st.markdown("""
    **Semantic ETL capabilities:**
    - Parse heavily structured PDFs
    - Read HTML & DOCX
    - Extract semantic Markdown
    - Isolate Markdown tables
    - Semantic Chunking for LLMs
    """)

# Main Content
st.markdown('<p class="main-header">✨ Semantic ETL Studio</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Transform document noise into pure, LLM-ready markdown signal.</p>', unsafe_allow_html=True)

# Step 1: Upload & Clean
st.subheader("1. Extract & Clean Document")
col1, col2 = st.columns([2, 1])

with col1:
    uploaded_file = st.file_uploader("Upload a file (PDF, DOCX, HTML)", type=["pdf", "docx", "html", "htm"])

with col2:
    st.markdown("<br>", unsafe_allow_html=True) # Spacer
    if st.button("🚀 Process Document", type="primary", disabled=not uploaded_file or not is_api_up):
        with st.spinner('Parsing document and running OCR via Docling...'):
            start_time = time.time()
            result = clean_file(uploaded_file)
            elapsed = time.time() - start_time
            
            if result:
                st.session_state.cleaned_markdown = result['markdown']
                st.session_state.metadata = result['metadata']
                st.session_state.tables = result.get('tables', [])
                st.session_state.chunks = None # Reset chunks on new file
                st.success(f"Processing complete in {elapsed:.2f} seconds!")

# Display Results
if st.session_state.cleaned_markdown:
    st.markdown("---")
    
    # Metadata Dashboard
    st.subheader("📊 Document Telemetry")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("File Type", st.session_state.metadata.get("file_type", "UNKNOWN"))
    m2.metric("Extracted Characters", f"{st.session_state.metadata.get('character_count', 0):,}")
    m3.metric("Estimated Tokens (cl100k)", f"{st.session_state.metadata.get('estimated_tokens', 0):,}")
    m4.metric("Data Tables Extracted", len(st.session_state.tables))

    # Output Tabs
    tab1, tab2, tab3 = st.tabs(["📝 Raw Markdown", "🗓️ Extracted Tables", "🧩 Chunking Studio"])
    
    with tab1:
        st.markdown("### Processed Markdown Output")
        st.text_area("Copy your cleaned data:", st.session_state.cleaned_markdown, height=500)
        
    with tab2:
        if st.session_state.tables:
            st.markdown("### Isolated Markdown Tables")
            for i, tbl in enumerate(st.session_state.tables):
                with st.expander(f"Table {i+1}"):
                    st.markdown(tbl)
        else:
            st.info("No tables detected in the document.")
            
    with tab3:
        st.markdown("### Prepare data for Vector Embeddings")
        st.write("Our chunking algorithm strictly respects markdown headers and guarantees a max token limit of 512, ensuring optimal RAG embedding contexts.")
        
        if st.button("⚡ Generate Semantic Chunks"):
            with st.spinner('Calculating boundaries and token limits...'):
                chunks = chunk_text(st.session_state.cleaned_markdown)
                if chunks:
                    st.session_state.chunks = chunks
                    
        if st.session_state.chunks:
            st.success(f"Generated {len(st.session_state.chunks)} optimal chunks!")
            for i, chunk in enumerate(st.session_state.chunks):
                with st.expander(f"Chunk {i+1} ({len(chunk)} chars)"):
                    st.text(chunk)

